# 06 — Especificação da experiência de leitura

## Princípio

**Mistério na entrada, acolhimento na leitura.** A pessoa passa da interface escura e técnica para uma página de texto com fundo marfim e linhas mais suaves. O contraste é intencional: a interface representa o método; o texto, a experiência humana.

## Leitor (rota dinâmica)

1. Barra de progresso de rolagem no topo da janela.
2. Retorno ao índice e seleção de capítulos por dropdown.
3. Painel opcional de ajustes (inicialmente fechado).
4. Identificação do registro e título original.
5. Notas da autora antes do texto, se presentes.
6. Conteúdo completo do capítulo com eventuais imagens e mudanças de POV.
7. Notas finais da autora, se presentes.
8. Controle de marcação como lido, anterior/próximo e AO3 original.

## Preferências

| Controle | Valores | Padrão |
| --- | --- | --- |
| Tema | Marfim / noturno | Marfim |
| Fonte | Source Serif 4 / DM Sans | Serifada |
| Tamanho | 16–24px | 19px |
| Entrelinha | 1,50–2,15 | 1,85 |

Preferências guardadas neste navegador. A experiência continua utilizável sem armazenamento.

## Comportamentos importantes

- A mudança de capítulo retorna ao topo.
- A marcação de capítulo lido é **manual**: abrir uma página não é o mesmo que terminar a leitura.
- Música é indicada textualmente quando o próprio corpo do PDF possui marcações; não há autoplay.
- Fotos anexadas respeitam sua posição de leitura e têm alt-text descritivo genérico.
- A barra de progresso indica rolagem aproximada da página, **não uma afirmação de capítulo concluído**.
- O leitor mostra notas originais sem atribuir frases-conceito criadas pelo projeto à Mary.

## Responsividade

- Desktop: largura máxima de 800px no leitor, espaço periférico para controles.
- Tablet: cabeçalho compacto, controle de capítulo sem perda de acesso.
- Mobile: controles ajustáveis, linha de leitura não ultrapassa a viewport, imagens fluidas.
- Nenhuma interação depende exclusivamente de hover.

## Acessibilidade

- HTML com `article`, `nav`, `header` e `main`.
- Botões possuem labels, estado ligado/desligado com `aria-pressed` e menus com `aria-expanded`.
- Foco visível e skip link.
- Animações reduzem com preferência do sistema.
- Necessário revisar manualmente o contraste de elementos secundários, zoom de 200% e navegação completa por teclado.
