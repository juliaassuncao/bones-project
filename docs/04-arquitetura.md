# 04 — Arquitetura técnica

## Stack

- Vite 6, React 18, TypeScript em modo estrito.
- React Router 6, navegação SPA (rewrite na Vercel).
- `*.module.scss` junto a cada componente e página.
- Conteúdo de fic em JSON independente do JSX.
- Sem backend ou banco de dados.

## Convenção de componentes (Linha Tênue)

```txt
NomeDoComponente/
├─ index.tsx
├─ styles.module.scss
├─ props.ts             # quando o componente recebe props
└─ constants.ts         # só se houver constantes próprias
```

**Não** criar arquivos artificiais vazios para cumprir convenção. Usar `props.ts` e `constants.ts` somente onde trazem separação real de responsabilidades. Os estilos devem ser importados no componente: `import styles from './styles.module.scss'`.

## Camadas

- `constants/`: textos e links de configuração global.
- `data/`: dados editoriais (personagens, músicas, JSON de capítulos).
- `types/`: contratos compartilhados.
- `components/`: visualizações reutilizáveis sem conhecimento desnecessário de rota.
- `pages/`: composição e estados das rotas.
- `hooks/`: leitura/persistência de preferências.
- `scripts/`: extração e verificação fora da aplicação.

## Pipeline de capítulo

```txt
PDF AO3/Calibre
  └─ scripts/import_bones.py
       ├─ src/data/chapters/manifest.json
       ├─ src/data/chapters/01.json ... 28.json
       └─ public/images/chapters/chapter-NN-XX.png

React /capitulos/:slug
  └─ Reader → getChapter(number) via import.meta.glob
       └─ ChapterBody (blocos tipados, notas/imagens)
```

JSON carrega **por demanda** pela rota atual para reduzir transferência inicial.

## Roteamento e acesso direto

O React Router mantém slugs com número e título (`25-say-yes-to-heaven-part-ii`). A Vercel encaminha rotas internas para `index.html`. O leitor deriva anterior/próximo do índice ordenado.

## Segurança do conteúdo HTML

A função de extração escapa todos os caracteres especiais do texto original e reintroduz apenas `<em>` e `<strong>` de fontes tipográficas. `ChapterBody` usa `dangerouslySetInnerHTML` exclusivamente para esse conteúdo transformado e validado, não para HTML recebido de uma API ou de pessoas visitantes. Alterações manuais devem manter essa condição. Antes de adicionar um CMS externo, introduzir sanitização apropriada.

## Estado e persistência

- Configuração de leitura: `bones:reading-preferences:v1`.
- Capítulos marcados como lidos: `bones:finished:v1`.
- Nunca armazenar texto da fic, informações pessoais ou dados de autenticação.
- Funciona sem `localStorage`, com perda apenas da persistência.

## Evolução técnica

- Ao receber novos capítulos, atualizar importação e manifestação de conteúdo.
- Se o acervo aumentar substancialmente, considerar geração estática de HTML para indexação.
- Imagens dos personagens poderão ser inseridas em `data/characters.ts` e `CharacterCard` sem refatoração das páginas.
