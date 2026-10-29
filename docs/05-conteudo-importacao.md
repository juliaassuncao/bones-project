# 05 — Conteúdo, extração e governança editorial

## Fonte

- Arquivo recebido: `Bones(2).pdf` (619 páginas).
- Autora no documento: `marydebones`.
- Origem declarada: `https://archiveofourown.org/works/84490006`.
- Dados da cópia: 28 capítulos; publicação indicada em 08/05/2026 e atualização indicada em 02/08/2026.
- Capa da playlist: arquivo de imagem enviado separadamente, usado em `public/images/branding/bones-hand.jpg`.

A fonte não é alterada. Os JSON são **derivações de apresentação**. A fonte original não é incluída no ZIP.

## Preservação

1. Títulos e ordem vêm dos bookmarks TOC do próprio PDF, não de títulos inventados.
2. Prosa é extraída dos blocos do PDF sem edição literária intencional.
3. Notas de autora anteriores/finais são separadas do corpo.
4. Fontes marcadas como itálico/negrito são representadas por `<em>` e `<strong>`.
5. Sete imagens no PDF foram exportadas e vinculadas às posições correspondentes.
6. Separadores `~~`, `[...]` e similares reconhecidos são convertidos em divisores visuais.
7. Cabeçalhos da exportação (“Chapter Notes”, “See the end...”) não fazem parte do conteúdo visível.
8. Linhas artificiais do layout de página são reunidas para evitar quebra a cada linha.

## Limitações relevantes

A extração de um PDF **não é equivalente ao HTML original do AO3**. Pode haver diferenças em:

- quebras de parágrafo quando um bloco atravessa páginas;
- espaços dentro de trechos com tipografia alternada;
- quebras internas de listas e letras de músicas;
- hierarquia de títulos quando o PDF agrupa texto e datas no mesmo bloco;
- URLs quebradas por mudança de linha.

Por isso, não afirmar equivalência editorial perfeita sem conferir os capítulos com o original. Como a fic inclui cenas sensíveis, privilegiar fidelidade à redação da Mary e evitar qualquer correção sem consentimento.

## Tipos de blocos

```ts
type ContentBlock =
  | { type: 'paragraph' | 'pov' | 'dateline' | 'music-cue' | 'aside'; html: string }
  | { type: 'divider' }
  | { type: 'image'; src: string; alt: string };
```

Cada `NN.json` possui `number`, `title`, `slug`, `source`, `summary`, `notes`, `content`, `endNotes`, `images`. `manifest.json` reúne os metadados usados no índice, sem obrigar o download de todos os capítulos ao entrar no site.

## Procedimento de revisão editorial recomendado

1. Conferir o título e o início de cada um dos 28 capítulos.
2. Verificar o parágrafo de transição a cada mudança de página do PDF.
3. Confirmar a posição das sete imagens e se são adequadas para publicação.
4. Comparar notas antes/depois do capítulo com o AO3.
5. Revisar trechos com muitos itálicos e músicas, especialmente 15, 17, 21, 23–28.
6. Revisar marcas de cena, POV e datas narrativas sem padronizar grafias.
7. Confrontar a página de trilha com a playlist da Mary antes de ampliar a lista.
8. Não adicionar fatos de personagem não confirmados pela obra.

## Como atualizar

O script de importação está em `scripts/import_bones.py`. O limite de capítulos importados é deliberadamente 28, para evitar atualizações acidentais sem nova auditoria. Para adicionar capítulos além do 28, adaptar a validação de contagem, conferir títulos, preservar os capítulos existentes e registrar a mudança.

Use `python scripts/check_content.py` após qualquer modificação. O relatório de importação fica em `docs/import-report.json`.
