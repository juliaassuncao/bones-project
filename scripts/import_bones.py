#!/usr/bin/env python3
"""Extrai capítulos do PDF AO3/Calibre sem reformular o texto. Necessita pymupdf.
Uso: python scripts/import_bones.py '/caminho/Bones.pdf'
"""
from __future__ import annotations
import fitz, json, html, re, sys, unicodedata
from pathlib import Path
from io import BytesIO
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
PDF=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/mnt/data/Bones(2).pdf')
DOC=fitz.open(PDF)
chapters=[(int(m.group(1)),m.group(2),p-1) for l,t,p in DOC.get_toc() if (m:=re.match(r'Chapter (\d+):\s*(.+)',t))]
assert len(chapters)==28,f'Esperados 28 capítulos, encontrados {len(chapters)}'

def norm_html(l):
    """Conserva marcas tipográficas de spans originais; elimina quebras de linha do PDF."""
    pieces=[]
    for i,s in enumerate(l):
        t=s['text']
        if not t.strip():
            if pieces: pieces.append(' ')
            continue
        t=html.escape(t,quote=False)
        flags=s.get('flags',0); font=s.get('font','').lower()
        is_ital= bool(flags & 2) or 'italic' in font or 'oblique' in font
        is_bold= bool(flags & 16) or 'bold' in font
        if is_ital and is_bold: t=f'<strong><em>{t}</em></strong>'
        elif is_ital: t=f'<em>{t}</em>'
        elif is_bold: t=f'<strong>{t}</strong>'
        pieces.append(t)
    return ''.join(pieces)

def block_to_item(b):
    if b['type']==1: return {'kind':'image','image':b}
    lines=[]
    for l in b.get('lines',[]):
        pieces=norm_html(l['spans']).strip()
        if pieces: lines.append(pieces)
    if not lines: return None
    # Espaços apenas nas quebras artificiais da página; conserva pontuação e ênfase.
    s=' '.join(lines)
    plain=html.unescape(re.sub(r'<[^>]+>','',s))
    return {'kind':'paragraph','html':s,'plain':plain,'bbox':b['bbox']}

def slug(s):
    s=''.join(c for c in unicodedata.normalize('NFD',s) if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

chapter_manifest=[]
stats={'imageCount':0,'emCount':0,'strongCount':0,'paragraphs':0,'sceneBreaks':0,'chapterCount':len(chapters),'chapterChecks':[]}
for index,(number,title,start) in enumerate(chapters):
    end=chapters[index+1][2] if index+1<len(chapters) else 618 # page 619 afterword excluded
    raw=[]
    for page_index in range(start,end):
        page=DOC[page_index]
        items=[]
        for b in page.get_text('dict')['blocks']:
            i=block_to_item(b)
            if i: items.append(i)
        # Alguns parágrafos atravessam páginas. Se a página anterior terminou com
        # uma linha até o rodapé e a primeira desta continua com minúscula,
        # concatenar em vez de inventar novo parágrafo.
        if raw and items and raw[-1]['kind']=='paragraph' and items[0]['kind']=='paragraph':
            a=raw[-1]; b=items[0]
            # Só concatena quando a quebra e continuação são evidentes.
            if a.get('bbox') and a['bbox'][3]>665 and b['bbox'][1]<90 and b['plain'][:1].islower():
                a['html']=a['html'].rstrip()+' '+b['html'].lstrip()
                a['plain']=a['plain'].rstrip()+' '+b['plain'].lstrip()
                items.pop(0)
        raw.extend(items)

    intro=[]; notes=[]; endnotes=[]; content=[]
    state='body'; seen_body=False
    images=[]
    for item in raw:
        if item['kind']=='image':
            b=item['image']; im=b['image']; ext=b.get('ext','png')
            count=len(images)+1; name=f'chapter-{number:02d}-{count:02d}.png'
            # Imagens em blocos: o Pixmap direto conserva a ordem e evite XREF duplicado.
            target=ROOT/'public/images/chapters'/name
            with Image.open(BytesIO(im)) as photo:
                photo.convert('RGB').save(target,optimize=True)
            images.append(name); stats['imageCount']+=1
            dest= endnotes if state=='endnotes' else (intro if state=='intro' else (notes if state=='notes' else content))
            dest.append({'type':'image','src':'/images/chapters/'+name,'alt':f'Imagem incluída pela autora no capítulo {number}'})
            continue
        plain=item['plain'].strip(); h=item['html'].strip()
        if not plain: continue
        if re.match(r'^Chapter\s+\d+:',plain): continue
        # Em títulos longos, o PDF quebra o cabeçalho em dois blocos: remover
        # a continuação, pois o nome integral já vem do índice PDF.
        if not content and not notes and not intro and not endnotes and len(plain)<55 and title.endswith(plain): continue
        if plain=='Chapter Summary': state='intro';continue
        if plain=='Chapter Notes': state='notes';continue
        if plain=='Chapter End Notes': state='endnotes';continue
        if plain in ('See the end of the chapter for notes','See the end of the chapter for more notes'):
            continue
        if plain.strip() in ('[...]','[ ... ]','* * *','***','~~','~ ~','* *','— — —') or re.match(r'^\*\s*\*\s*\*$',plain):
            dest=endnotes if state=='endnotes' else content
            dest.append({'type':'divider'});stats['sceneBreaks']+=1;continue
        if state in ['intro','notes']:
            # O primeiro marcador de POV sinaliza começo do texto; cabeçalhos e
            # datas começam no corpo e não nas notas da autora.
            if re.match(r'^(POV\s|\d{1,2}\s+de\s+\w+|(?:Segunda|Terça|Quarta|Quinta|Sexta|Sábado|Domingo)-feira,)',plain,re.I):
                state='body'
        dest=content if state=='body' else intro if state=='intro' else notes if state=='notes' else endnotes
        typ='paragraph'
        if state=='body':
            if re.match(r'^POV\s+(Lorena|Eduarda|Narrador|Paulo|Angélica|Cristine|Júnior|Viviane)',plain,re.I):typ='pov'
            elif re.match(r'^(?:Segunda|Terça|Quarta|Quinta|Sexta|Sábado|Domingo)-feira,\s*\d|^\d{1,2} de [A-Za-zçãé]+ de 20\d\d',plain,re.I):typ='dateline'
            elif re.match(r'^Music (?:On|Off):|^Música (?:On|Off):',plain,re.I):typ='music-cue'
            elif re.match(r'^~?OPA[,!]|^ATENÇÃO',plain,re.I):typ='aside'
        dest.append({'type':typ,'html':h})
        stats['paragraphs']+=1
        stats['emCount']+=h.count('<em>');stats['strongCount']+=h.count('<strong>')
    # Safety: algumas introduções sem POV explícito não têm demarcador e podem
    # acabar absorvidas como notes. Aqui, só classificar como notas se capítulo
    # tem POV; caso contrário preservar no corpo.
    if not content and notes:content=notes;notes=[]
    if not content and intro:content=intro;intro=[]
    result={'number':number,'title':title,'slug':f'{number:02d}-{slug(title)}', 'source':{'startPage':start+1,'endPage':end},'summary':intro,'notes':notes,'content':content,'endNotes':endnotes,'images':images}
    out=ROOT/'src/data/chapters'/f'{number:02d}.json';out.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    chapter_manifest.append({'number':number,'title':title,'slug':result['slug'],'startPage':start+1,'endPage':end,'hasNotes':bool(intro or notes or endnotes),'hasImages':bool(images),'readingBlocks':len(content)})
    stats['chapterChecks'].append([number,len(intro),len(notes),len(content),len(endnotes),len(images)])

(ROOT/'src/data/chapters/manifest.json').write_text(json.dumps(chapter_manifest,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'docs/import-report.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
print('PDF:',PDF.name,'CHAPTERS',len(chapters),'IMAGES',stats['imageCount'],'ITALIC',stats['emCount'],'BOLD',stats['strongCount'],'PARAGRAPHS',stats['paragraphs'],'SCENE BREAKS',stats['sceneBreaks'])
for n,a,b,c,d,imgs in stats['chapterChecks']:print(f'{n:02} summary={a:02} note={b:02} body={c:03} end={d:02} images={imgs}')
