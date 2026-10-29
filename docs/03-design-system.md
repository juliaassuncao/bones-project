# 03 — Design system inicial

## Tokens de identidade

| Token | Hex | Uso |
| --- | --- | --- |
| Background | `#071316` | Base escura global |
| Background deep | `#04090a` | Hero e rodapé |
| Surface | `#0e2024` | Cards |
| Surface 2 | `#12343b` | Acentos e controles |
| Accent | `#20d8d2` | Marca ciano, CTA, foco |
| Accent light | `#8cebea` | Hover |
| Bone | `#e6e0d6` | Títulos claros e leitor diurno |
| Muted | `#a2b2b0` | Metadados e texto secundário |
| Reader paper | `#ece7dc` | Fundo do conteúdo em modo diurno |
| Reader ink | `#253336` | Texto no modo diurno |
| Reader dark | `#112428` | Fundo do conteúdo noturno |

Tokens compartilhados em `src/styles/global.scss`. Ajustes específicos ficam nos respectivos módulos SCSS.

## Tipografia

- Interface, metadados e botões: **DM Sans** (fallback sans-serif).
- Títulos, citações conceituais e números: **Cormorant Garamond** (fallback Georgia).
- Narrativa: **Source Serif 4** (fallback Georgia); opcionalmente DM Sans.
- Fontes vêm do Google Fonts; o site possui fallback para funcionamento sem CDN.

## Grid e espaços

- `.container`: 1160px máximos, gutters de 24px (16px em celular).
- Home seccionada com intervalos grandes; leitor com conteúdo limitado a 800px.
- Breakpoints de layout: ~950px menu, ~850px grids intermediários, ~650px mobile.
- Evitar margens negativas grandes e larguras fixas nas imagens.

## Componentes

| Componente | Responsabilidade |
| --- | --- |
| `SiteHeader` / `SiteFooter` | Shell global e navegação |
| `ArchiveLabel` | Microtítulo e identificação do arquivo |
| `SectionHeading` | Título de seção com ação opcional |
| `CharacterCard` | Ficha visual sem spoilers |
| `ChapterCard` | Item de índice de capítulo |
| `ChapterBody` | Apresentação dos blocos do PDF |
| `ReadingControls` | Tema, tipo, tamanho, entrelinha |
| `ChapterNavigator` | Anterior/próximo |
| `ScrollProgress` | Progresso visual da rolagem |

## Acessibilidade

- Contraste principal entre texto e fundos; ciano usado com moderação.
- Controles nativos, labels e estados `aria-pressed` / `aria-expanded`.
- `prefers-reduced-motion` reduz animações e transições.
- `focus-visible`, skip link e landmarks semânticos.
- Metadados e avisos de conteúdo acessíveis antes da leitura.
- Verificar contrastes de textos menores em revisão visual manual.

## Regras de interação

- Nunca iniciar áudio automaticamente.
- Não colocar animações sobre conteúdo longo.
- Hover discreto com realce ciano e deslocamento mínimo.
- Evitar mudança de layout ao trocar controles do leitor.
