# 11 — Auditoria das notas e do conteúdo original

Data: 29/10/2026. Fontes locais: `Bones.pdf` (619 páginas) e `Bones.epub`, por marydebones. Os hashes SHA-256 e os resultados individuais dos 28 capítulos estão em [source-audit.json](source-audit.json).

O texto completo do EPUB foi confrontado com o PDF em cada capítulo, incluindo cabeçalhos, resumos e notas. A sequência de caracteres corresponde integralmente ao desconsiderar os espaços de paginação, com quatro glifos não extraíveis no capítulo 20. O EPUB correspondente permitiu recuperar parágrafos, quebras explícitas e esses quatro emojis. Não houve reescrita, resumo ou correção literária.

## Divergências corrigidas

| Local | Evidência e correção |
| --- | --- |
| Sobre · nota da obra (PDF p. 3) | Separados os dois primeiros parágrafos que estavam unidos; restaurados o aviso de atualizações aos domingos e a assinatura. Os quatro parágrafos são literais. Somente `@marydebones` virou link; nota editorial e estilos mantidos. |
| Cap. 19 (p. 296) | A epígrafe de Hélène Cixous aparecia nas notas iniciais. Voltou ao início do corpo, antes do POV. A nota musical permaneceu nas notas. |
| Cap. 21 (pp. 362–363) | Data e nove mensagens de WhatsApp estavam em `notes`. Os dez blocos voltaram ao corpo antes do POV, com quebras entre remetente, horário e mensagem. As duas notas finais foram preservadas. |
| Cap. 24 (pp. 445–446) | A apresentação das roupas e as duas imagens voltaram ao início do corpo, onde aparecem na fonte. Os cinco parágrafos do resumo e as notas finais foram preservados. |
| Cap. 26 (p. 510) | O alerta ao leitor voltou ao início do corpo, após as notas de abertura, mantendo integralmente texto, destaque e posição anterior ao POV. |
| Caps. 24 e 25 (pp. 445 e 462) | Recompostas as URLs originais do Spotify, cujos parâmetros `?si=…` estavam separados por um espaço de quebra de linha do PDF. Não foram substituídas por URLs inventadas. |
| Cap. 20 (pp. 326–361) | Recuperados quatro emojis `🙄` que haviam sido importados como caracteres nulos, usando o EPUB correspondente no mesmo ponto da sequência textual. |
| Parágrafos e linhas | Removidas 21 divisões artificiais de parágrafo; restaurada uma divisão original que havia sido perdida e 216 quebras explícitas em conversas, letras, listas musicais e notas. Espaços artificiais da extração, como `terça- feira`, foram recompostos conforme a fonte. |

Todos os resumos, notas de abertura, notas finais e referências musicais dos 28 capítulos foram conferidos. As sete imagens foram preservadas. Os capítulos 03, 08 e 13 já correspondiam à apresentação original e não tiveram seus JSON alterados. Os outros 25 receberam correções comprovadas de estrutura, espaçamento de extração ou marcação. Marcação equivalente existente foi reaproveitada para reduzir alterações.

## Prevenção de regressões

- `scripts/import_bones.py` reconhece o link editorial do AO3 como término das notas de abertura, sem depender de um marcador de POV.
- `scripts/audit_source.py` compara as duas fontes completas antes de qualquer escrita; a opção `--fix` restaura a apresentação e atualiza o manifesto e as contagens.
- `scripts/check_content.py` verifica também quebras HTML seguras, ordem das tags, ausência de caracteres de controle, URLs partidas e consistência das contagens do manifesto.
- Nenhum PDF ou EPUB foi adicionado ao repositório; nenhuma dependência de execução foi adicionada ao site.

## Verificação

```bash
python scripts/audit_source.py "C:/caminho/Bones.pdf" "C:/caminho/Bones.epub"
python scripts/check_content.py
npm run build
```

As contagens atualizadas por capítulo estão em [10 — Índice da fonte](10-indice-fonte.md) e [import-report.json](import-report.json).

Resultados: a auditoria das fontes passou sem divergências pendentes; a validação de conteúdo passou com 4.416 blocos de texto e sete imagens. Uma comparação independente com os JSON anteriores preservou toda a sequência textual, com a única substituição dos quatro caracteres nulos pelos emojis originais. A página Sobre e o capítulo 21 foram conferidos no Chrome em 1440, 768, 390 e 320 px, incluindo os quatro parágrafos, o foco de teclado e a posição da conversa no corpo.

A compilação isolada do Vite passou. `npm run build` continua bloqueado pelo erro preexistente TS2367 em `src/components/ChapterBody/index.tsx:12`, que não foi alterado nesta correção. O projeto não possui comando de lint. Nenhum commit foi realizado.

## Arquivos desta correção

- `src/constants/site.ts` e `src/pages/About/index.tsx`.
- JSON dos capítulos 01, 02, 04–07, 09–12 e 14–28 em `src/data/chapters/`, além de `manifest.json`.
- `scripts/import_bones.py`, `scripts/check_content.py` e o novo `scripts/audit_source.py`.
- `docs/00-INDEX.md`, `docs/05-conteudo-importacao.md`, `docs/10-indice-fonte.md` e `docs/import-report.json`.
- Novos `docs/11-auditoria-fonte.md` e `docs/source-audit.json`.

Os estilos existentes de Sobre foram reutilizados sem alterações nesta tarefa. As alterações anteriores da home, dos créditos, do rodapé e da página de personagens foram preservadas.
