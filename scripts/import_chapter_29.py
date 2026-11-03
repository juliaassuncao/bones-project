"""Importa/valida somente o capítulo 29 a partir do DOCX oficial.

Uso: python scripts/import_chapter_29.py caminho.docx [--check]
Não executa o importador do PDF nem modifica capítulos anteriores.
"""
import argparse
import html
import json
from pathlib import Path
import re
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
W = '{' + NS['w'] + '}'


class StyledText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.characters = []

    def handle_starttag(self, tag, attrs):
        assert not attrs
        if tag == 'br':
            self.characters.append(('\n', tuple(sorted(self.tags))))
        else:
            assert tag in ('em', 'strong')
            self.tags.append(tag)

    def handle_endtag(self, tag):
        if tag == 'br':
            return
        assert self.tags.pop() == tag

    def handle_data(self, data):
        self.characters.extend((c, tuple(sorted(self.tags))) for c in data)


def read_source(path):
    with ZipFile(path) as archive:
        document = ET.fromstring(archive.read('word/document.xml'))
        assert not document.findall('.//w:tbl', NS)
        assert not document.findall('.//w:hyperlink', NS)
        assert not document.findall('.//w:drawing', NS)
        pages = int(ET.fromstring(archive.read('docProps/app.xml')).find(
            '{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Pages').text)
    paragraphs = []
    for paragraph in document.findall('w:body/w:p', NS):
        markup = []
        expected = []
        for run in paragraph.findall('w:r', NS):
            tags = []
            for prop, tag in (('b', 'strong'), ('i', 'em')):
                value = run.find('w:rPr/w:' + prop, NS)
                if value is not None and value.get(W + 'val', '1') not in ('0', 'false', 'off'):
                    tags.append(tag)
            text = ''.join(node.text or '' if node.tag == W + 't' else '\n'
                           for node in run if node.tag in (W + 't', W + 'br'))
            if not text:
                continue
            expected.extend((c, tuple(sorted(tags))) for c in text)
            markup.append(''.join('<' + tag + '>' for tag in tags)
                          + html.escape(text, quote=False).replace('\n', '<br/>')
                          + ''.join('</' + tag + '>' for tag in reversed(tags)))
        paragraphs.append((''.join(c for c, _ in expected), ''.join(markup), expected))
    return pages, paragraphs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('docx', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    pages, paragraphs = read_source(args.docx)
    assert pages == 30
    assert paragraphs[0][0] == 'Capítulo 28 - Internal Partings'
    assert paragraphs[5][0] == '∞'
    assert paragraphs[6][0].strip() == 'Pov Lorena'
    selected = [(i, p) for i, p in enumerate(paragraphs[1:], 1)
                if p[0].strip() and p[0].strip() != '∞']
    notes, content, end_notes = [], [], []
    for index, (text, markup, _) in selected:
        kind = 'paragraph'
        if index > 5:
            if re.fullmatch(r'pov .+', text.strip(), re.I):
                kind = 'pov'
            elif re.match(r'^(Domingo|Terça-feira),', text):
                kind = 'dateline'
            elif text.startswith('Music On:'):
                kind = 'music-cue'
        (notes if index < 5 else end_notes if index >= 362 else content).append({'type': kind, 'html': markup})
    chapter = dict(number=29, title='Internal Partings', slug='29-internal-partings',
                   source=dict(startPage=1, endPage=pages), summary=[], notes=notes,
                   content=content, endNotes=end_notes, images=[])
    target = ROOT / 'src/data/chapters/29.json'
    manifest_path = ROOT / 'src/data/chapters/manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    meta = dict(number=29, title=chapter['title'], slug=chapter['slug'], startPage=1,
                endPage=pages, hasNotes=True, hasImages=False, readingBlocks=len(content))
    if not args.check:
        assert not target.exists(), 'Capítulo já existe; use --check para validar.'
        assert manifest[-1]['number'] == 28
        target.write_text(json.dumps(chapter, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        # Acrescenta ao manifesto sem reformatar os registros anteriores.
        original = manifest_path.read_text(encoding='utf-8').rstrip()
        manifest_path.write_text(original[:-1].rstrip() + ',\n'
                                 + '\n'.join('  ' + line for line in json.dumps(meta, ensure_ascii=False, indent=2).splitlines())
                                 + '\n]\n', encoding='utf-8')
    actual = json.loads(target.read_text(encoding='utf-8'))
    assert actual == chapter
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    assert manifest[-1] == meta
    assert len(actual['notes']) == 4 and len(actual['endNotes']) == 3 and not actual['summary']
    blocks = actual['notes'] + actual['content'] + actual['endNotes']
    assert len(blocks) == len(selected)
    # Compara cada caractere e seu itálico/negrito, inclusive espaços e quebras.
    for block, (index, (_, _, expected)) in zip(blocks, selected):
        parsed = StyledText()
        parsed.feed(block['html'])
        assert not parsed.tags
        assert parsed.characters == expected, f'Divergência no parágrafo {index}'
    assert all('∞' not in b['html'] for b in blocks)
    assert actual['content'][-1]['html'] == paragraphs[360][1]
    assert actual['endNotes'][-1]['html'] == paragraphs[364][1]
    print(f'OK: {pages} páginas; 4 notas iniciais; 3 notas finais; {len(content)} blocos no corpo; '
          f'{len(selected)} parágrafos comparados caractere a caractere e por formatação.')
    for block in content:
        if block['type'] != 'paragraph':
            print(block['type'] + ': ' + block['html'])
    print('Omitidos: título (identificação no site = 29), 2 separadores ∞ e 4 parágrafos vazios finais.')


if __name__ == '__main__':
    main()
