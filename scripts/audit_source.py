"""Audita o PDF e restaura a estrutura do EPUB correspondente, sem reescrita.

Uso: python scripts/audit_source.py Bones.pdf Bones.epub [--fix]
Requer PyMuPDF apenas como ferramenta local; não adiciona dependências ao site.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET
import zipfile

import fitz

ROOT = Path(__file__).resolve().parents[1]
NS = {'h': 'http://www.w3.org/1999/xhtml', 'o': 'http://www.idpf.org/2007/opf'}
FIELDS = ('summary', 'notes', 'content', 'endNotes')
SEPARATORS = {'[...]', '[ ... ]', '* * *', '***', '~~', '~ ~', '* *', '— — —'}


def compact(text):
    return re.sub(r'\s+', '', text)


def plain(markup):
    return html.unescape(re.sub(r'<[^>]+>', '', markup))


def inline(node):
    """Somente texto e marcação de ênfase/quebra presentes na fonte local."""
    def text(value):
        return html.escape(re.sub(r'[\t\r\n ]+', ' ', value or ''), quote=False)

    result = text(node.text)
    for child in node:
        tag = child.tag.rsplit('}', 1)[-1]
        if tag == 'br':
            result += '<br/>'
        else:
            value = inline(child)
            mapped = {'b': 'strong', 'strong': 'strong', 'i': 'em', 'em': 'em'}.get(tag)
            result += f'<{mapped}>{value}</{mapped}>' if mapped and value else value
        result += text(child.tail)
    return result


def block_type(text, section):
    if text.strip() in SEPARATORS:
        return 'divider'
    if section != 'content':
        return 'paragraph'
    if re.match(r'^POV\s+', text, re.I):
        return 'pov'
    if re.match(r'^\(?\d{1,2} de \w+ de 20\d\d|^\(?(?:Segunda|Terça|Quarta|Quinta|Sexta|Sábado|Domingo)(?:-feira)?,', text, re.I):
        return 'dateline'
    if re.match(r'^(?:Music|Música) (?:On|Off):', text, re.I):
        return 'music-cue'
    if re.match(r'^~?OPA[,!]|^ATENÇÃO', text, re.I):
        return 'aside'
    return 'paragraph'


def source_blocks(container, section, images):
    result = []
    for node in container:
        tag = node.tag.rsplit('}', 1)[-1]
        if tag == 'p':
            if ''.join(node.itertext()).strip():
                markup = inline(node).strip()
                kind = block_type(plain(markup), section)
                result.append({'type': kind} if kind == 'divider' else {'type': kind, 'html': markup})
            for image in node.findall('.//h:img', NS):
                result.append(next(images))
        elif tag == 'hr':
            result.append({'type': 'divider'})
        else:
            result.extend(source_blocks(node, section, images))
    return result


def chapter_sections(node, old):
    images = iter([block for field in FIELDS for block in old[field] if block['type'] == 'image'])
    result = {field: [] for field in FIELDS}
    for child in node:
        if child.get('class') == 'userstuff2':
            result['content'].extend(source_blocks(child, 'content', images))
        elif child.get('id', '').startswith('endnotes'):
            for container in child:
                if container.tag.rsplit('}', 1)[-1] in ('div', 'blockquote'):
                    result['endNotes'].extend(source_blocks(container, 'endNotes', images))
        else:
            section = None
            for item in child:
                text = ''.join(item.itertext()).strip()
                if text in ('Chapter Summary', 'Chapter Notes'):
                    section = 'summary' if text == 'Chapter Summary' else 'notes'
                elif item.tag.endswith('blockquote'):
                    assert section, 'Bloco sem seção de origem'
                    result[section].extend(source_blocks(item, section, images))
    assert next(images, None) is None, 'Imagem importada sem posição na fonte'
    return result


def canonical_sections(sections):
    return compact(''.join(plain(b.get('html', '')) for field in FIELDS for b in sections[field]))


def presentation(markup):
    """Compara texto, ênfase e quebras, ignorando só tags redundantes e espaços externos."""
    class Parser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.tokens = []
            self.bold = self.italic = 0

        def handle_starttag(self, tag, attrs):
            self.bold += tag == 'strong'
            self.italic += tag == 'em'
            if tag == 'br':
                if self.tokens and self.tokens[-1][0] == ' ':
                    self.tokens.pop()
                self.tokens.append(('\n', False, False))

        def handle_endtag(self, tag):
            self.bold -= tag == 'strong'
            self.italic -= tag == 'em'

        def handle_data(self, data):
            for character in data:
                if character.isspace():
                    if self.tokens and self.tokens[-1][0] not in (' ', '\n'):
                        self.tokens.append((' ', False, False))
                else:
                    self.tokens.append((character, self.bold > 0, self.italic > 0))

    parser = Parser()
    parser.feed(markup)
    if parser.tokens and parser.tokens[-1][0] == ' ':
        parser.tokens.pop()
    return parser.tokens


def retain_equivalent_markup(old, sections):
    # Não regrava marcação existente que já produz o mesmo texto e formatação.
    position = 0
    existing = {}
    for field in FIELDS:
        for block in old[field]:
            if 'html' in block:
                end = position + len(compact(plain(block['html'])))
                existing[position, end] = block['html']
                position = end
    position = 0
    for field in FIELDS:
        for block in sections[field]:
            if 'html' in block:
                end = position + len(compact(plain(block['html'])))
                candidate = existing.get((position, end))
                if candidate is not None and presentation(candidate) == presentation(block['html']):
                    block['html'] = candidate
                position = end


def boundaries(sections):
    position = 0
    result = set()
    for field in FIELDS:
        for block in sections[field]:
            if 'html' in block:
                position += len(compact(plain(block['html'])))
                result.add(position)
    return result


def source_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(pdf_path, epub_path, fix=False):
    doc = fitz.open(pdf_path)
    toc = [(int(m[1]), m[2], page - 1) for _, title, page in doc.get_toc()
           if (m := re.match(r'Chapter (\d+):\s*(.+)', title))]
    assert len(doc) == 619 and [n for n, _, _ in toc] == list(range(1, 29))
    manifest = json.loads((ROOT / 'src/data/chapters/manifest.json').read_text(encoding='utf-8'))
    changes = []
    staged = []
    with zipfile.ZipFile(epub_path) as archive:
        package = ET.fromstring(archive.read('content.opf'))
        files = {e.get('id'): e.get('href') for e in package.findall('o:manifest/o:item', NS)}
        chapter_nodes = {}
        for ref in package.findall('o:spine/o:itemref', NS):
            root = ET.fromstring(archive.read(files[ref.get('idref')]))
            node = root.find('.//h:div[@id="chapters"]', NS)
            if node is None:
                continue
            heading = node.find('.//h:h2', NS)
            if heading is not None:
                match = re.match(r'Chapter (\d+):', ''.join(heading.itertext()).strip())
                assert match, 'Cabeçalho não reconhecido'
                chapter_nodes[int(match[1])] = node
        assert sorted(chapter_nodes) == list(range(1, 29))

        # Confere também a nota da obra na página 3, antes de qualquer escrita.
        preface = ET.fromstring(archive.read('Bones_split_001.xhtml'))
        note = preface.findall('.//h:blockquote', NS)[1]
        origin_note = [''.join(p.itertext()).strip() for p in note.findall('h:p', NS)]
        assert len(origin_note) == 4
        assert compact(''.join(origin_note)) in compact(doc[2].get_text())

        for index, (number, title, start) in enumerate(toc):
            end = toc[index + 1][2] if index + 1 < len(toc) else len(doc) - 1
            node = chapter_nodes[number]
            epub_text = compact(''.join(node.itertext()))
            pdf_text = compact(''.join(doc[p].get_text() for p in range(start, end)))
            assert len(pdf_text) == len(epub_text), f'PDF/EPUB com tamanho diferente no capítulo {number}'
            missing_glyphs = [(i, a) for i, (a, b) in enumerate(zip(epub_text, pdf_text)) if a != b]
            assert all(pdf_text[i] == '\x00' for i, _ in missing_glyphs), f'PDF/EPUB divergentes: {number}'

            path = ROOT / f'src/data/chapters/{number:02}.json'
            old = json.loads(path.read_text(encoding='utf-8'))
            assert old['title'] == title and old['source'] == {'startPage': start + 1, 'endPage': end}
            sections = chapter_sections(node, old)
            before, after = canonical_sections(old), canonical_sections(sections)
            assert len(before) == len(after) and all(a == b or a == '\x00' for a, b in zip(before, after)), f'Texto alterado: {number}'
            assert after and sections['content']
            retain_equivalent_markup(old, sections)
            old_urls = re.findall(r'https?://[^\s<>]+', ' '.join(b.get('html', '') for field in FIELDS for b in old[field]))
            new_urls = re.findall(r'https?://[^\s<>]+', ' '.join(b.get('html', '') for field in FIELDS for b in sections[field]))
            old_bounds, new_bounds = boundaries(old), boundaries(sections)
            changes.append({
                'chapter': number,
                'pages': [start + 1, end],
                'pdfEpubTextMatch': True,
                'before': {field: len(old[field]) for field in FIELDS},
                'after': {field: len(sections[field]) for field in FIELDS},
                'artificialParagraphBreaksRemoved': len(old_bounds - new_bounds),
                'originalParagraphBreaksRestored': len(new_bounds - old_bounds),
                'explicitLineBreaksRestored': sum(b.get('html', '').count('<br/>') for field in FIELDS for b in sections[field]) - sum(b.get('html', '').count('<br/>') for field in FIELDS for b in old[field]),
                'recoveredGlyphs': [glyph for _, glyph in missing_glyphs],
                'urlsBefore': old_urls,
                'urlsAfter': new_urls,
                'changed': any(old[field] != sections[field] for field in FIELDS),
            })
            staged.append((path, {**old, **sections}))

    # Só escreve após conferir a fonte e a sequência completa dos 28 capítulos.
    report = {'pdf': {'name': pdf_path.name, 'pages': len(doc), 'sha256': source_hash(pdf_path)},
              'epub': {'name': epub_path.name, 'sha256': source_hash(epub_path)},
              'originNote': origin_note, 'chapters': changes}
    if fix:
        for path, data in staged:
            serialized = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
            if path.read_text(encoding='utf-8') != serialized:
                path.write_text(serialized, encoding='utf-8')
        for meta, (_, data) in zip(manifest, staged):
            assert meta['number'] == data['number']
            meta['hasNotes'] = any(data[field] for field in ('summary', 'notes', 'endNotes'))
            meta['readingBlocks'] = len(data['content'])
        (ROOT / 'src/data/chapters/manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        counts = Counter()
        checks = []
        for _, data in staged:
            for field in FIELDS:
                for block in data[field]:
                    counts['imageCount'] += block['type'] == 'image'
                    counts['sceneBreaks'] += block['type'] == 'divider'
                    counts['paragraphs'] += 'html' in block
                    counts['emCount'] += block.get('html', '').count('<em>')
                    counts['strongCount'] += block.get('html', '').count('<strong>')
            checks.append([data['number'], *(len(data[field]) for field in FIELDS), len(data['images'])])
        (ROOT / 'docs/import-report.json').write_text(json.dumps({**counts, 'chapterCount': 28, 'chapterChecks': checks}, ensure_ascii=False, indent=2), encoding='utf-8')
        (ROOT / 'docs/source-audit.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf', type=Path)
    parser.add_argument('epub', type=Path)
    parser.add_argument('--fix', action='store_true', help='Aplica somente após validar integralmente as duas fontes.')
    args = parser.parse_args()
    report = audit(args.pdf, args.epub, args.fix)
    for chapter in report['chapters']:
        print(json.dumps(chapter, ensure_ascii=False))
    print('OK: PDF e EPUB conferidos nos 28 capítulos; sequência textual preservada.')
    if not args.fix and any(chapter['changed'] for chapter in report['chapters']):
        parser.exit(1, 'Foram encontradas divergências de apresentação. Revise o relatório antes de aplicar --fix.\n')
