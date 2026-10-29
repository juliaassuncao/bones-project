# Bones — Arquivo Vivo

Site literário de leitura para **Bones**, por **marydebones**. Projeto de fãs desenvolvido em React + TypeScript + SCSS Modules a partir de uma cópia em PDF disponibilizada para este trabalho.

> **Estado da entrega:** MVP implementado, com 28 capítulos importados do PDF, índice, navegação, preferências de leitura, 7 imagens internas, fichas introdutórias de personagens e destaque da playlist. A validação local de conteúdo passou. O build com `npm` deve ser executado no computador de desenvolvimento, pois o ambiente de geração não conseguiu acessar o registro de pacotes.

## Requisitos

- Node.js 20.19+ (ou 22.12+)
- npm

## Primeiros passos

```bash
npm install
npm run dev
```

Abra o endereço exibido pelo Vite (normalmente `http://localhost:5173`). Para revisar antes de publicar:

```bash
npm run typecheck
npm run build
npm run preview
```

A aplicação usa **Vite, React 18, TypeScript, React Router e SCSS Modules**. Não exige banco de dados, backend nem chaves de API.

## Páginas

| Caminho | Finalidade |
| --- | --- |
| `/` | Home conceitual, com a capa da playlist |
| `/sobre` | Sinopse original, metadados, avisos e autoria |
| `/personagens` | Introdução sem spoilers aos personagens |
| `/capitulos` | Índice com busca e marcação de lidos |
| `/capitulos/:slug` | Leitor e navegação por anterior/próximo |
| `/trilha-sonora` | Destaques musicais e link da playlist oficial |

## Estrutura

```txt
public/
  images/branding/              # capa da playlist enviada
  images/chapters/              # 7 imagens extraídas do PDF
src/
  components/NomeDoComponente/
    index.tsx
    styles.module.scss
    props.ts                    # se houver props públicas
    constants.ts                # somente quando necessário
  pages/NomeDaPagina/
    index.tsx
    styles.module.scss
  layouts/SiteLayout/
  constants/site.ts
  data/characters.ts
  data/soundtrack.ts
  data/chapters/
    index.ts                    # carregamento assíncrono
    manifest.json              # metadados dos 28 capítulos
    01.json ... 28.json        # conteúdo de cada capítulo
  hooks/
  styles/global.scss           # resets e tokens globais
  types/content.ts
scripts/
  import_bones.py              # importação a partir do PDF
  check_content.py             # auditoria objetiva da importação
docs/                          # especificação do projeto
```

O padrão é **CSS junto do componente**, sem concentrar os estilos de componentes em um `main.scss`. Apenas resets, tipografia, tokens e utilitários realmente globais ficam em `global.scss`.

## Leitura

O leitor inclui: tema marfim/escuro, escolha entre fonte serifada/sem serifa, tamanho de fonte, entrelinha, dropdown para qualquer capítulo, navegação anterior/próximo, progresso visual de scroll e marcação voluntária de capítulos lidos. Preferências e marcações são guardadas no `localStorage` do navegador; não existe conta nem transmissão desses dados.

O conteúdo do PDF foi organizado em blocos estruturados (`paragraph`, `pov`, `dateline`, `music-cue`, `divider`, `image`). Marcas de **negrito** e *itálico* foram preservadas onde reconhecíveis por tipografia da fonte PDF. Notas iniciais/finais estão separadas da narrativa, sem reescrita intencional. A importação de PDF pode produzir pequenas diferenças de espaços, quebras de parágrafo ou formatação, especialmente em blocos de letras de músicas e notas; **conferência editorial com o texto original ainda é obrigatória**.

## Atualizar os capítulos

Coloque o novo PDF em local acessível e, se tiver Python + PyMuPDF + Pillow:

```bash
python scripts/import_bones.py "C:/caminho/para/Bones.pdf"
python scripts/check_content.py
```

**Atenção:** o importador atual espera exatamente 28 capítulos e regrava os JSON de `01` a `28`; antes de importar atualizações futuras (29+), adapte a validação e faça backup dos dados. Para corrigir apenas um parágrafo, altere o `html` do bloco respectivo no `NN.json` com cuidado para manter texto e fechamento de `<em>/<strong>`.

Arquivos que podem ser atualizados sem modificar layout:
- `src/data/characters.ts`: fichas de personagens
- `src/data/soundtrack.ts`: músicas e associação aos capítulos
- `src/constants/site.ts`: sinopse, créditos e links
- `public/images/branding/bones-hand.jpg`: arte principal

## Publicação na Vercel

A configuração `vercel.json` já inclui reescrita SPA. Na Vercel, selecione Vite, use build `npm run build` e diretório de saída `dist`. O site não exige variáveis de ambiente.

**Antes de publicar:** confirmar autorização para reprodução pública integral dos capítulos, das imagens internas e da capa da playlist com a Mary e os demais titulares de direitos aplicáveis. A nota de autoria da versão Camren/coautoria original foi mantida em `/sobre`. A página original no AO3 continua sendo a referência canônica.

## Documentos

Leia `docs/00-INDEX.md` para entrar no projeto pelo documento mais adequado.
