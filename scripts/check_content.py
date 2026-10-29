"""Verificações objetivas de integridade do conteúdo importado."""
import json, pathlib, re
r=pathlib.Path(__file__).resolve().parents[1]
m=json.loads((r/'src/data/chapters/manifest.json').read_text(encoding='utf8'))
assert len(m)==28 and [x['number'] for x in m]==list(range(1,29))
count=0; images=0; errors=[]
for c in m:
    dat=json.loads((r/f"src/data/chapters/{c['number']:02}.json").read_text(encoding='utf8'))
    assert dat['number']==c['number'] and dat['title']==c['title'] and dat['slug']==c['slug']
    assert dat['content'],f"Sem corpo: {c['number']}"
    for key in ('summary','notes','content','endNotes'):
        for block in dat[key]:
            if block['type']=='image':
                images+=1
                path=r/'public'/block['src'].lstrip('/')
                assert path.exists(),f"Imagem ausente: {path}"
            elif block['type']!='divider':
                count+=1
                markup=block['html']
                for tag in ('em','strong'):
                    assert markup.count(f'<{tag}>')==markup.count(f'</{tag}>'),(c['number'],tag,markup[:200])
                for forbidden in ('<script','<iframe','<img ','onerror=','onclick='):
                    if forbidden in markup.lower():errors.append((c['number'],forbidden))
assert not errors,errors
print(f'OK: {len(m)} capítulos consecutivos, {count} blocos de texto, {images} imagens, marcação HTML controlada.')
