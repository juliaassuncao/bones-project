# 02 — Produto, sitemap e escopo

## Públicos

- Leitoras que já acompanham a Mary e desejam uma experiência organizada.
- Pessoas que descobriram a fic por recomendação, playlist ou rede social.
- A autora/equipe do projeto, que precisa atualizar os capítulos com segurança.

## Jornadas principais

**Primeira visita:** home → sinopse e avisos → índice → capítulo 1 → próximo.

**Retorno:** índice → pesquisar número ou título → abrir capítulo → ajustar leitor → marcar como lido.

**Trilha:** home/reader → página de trilha → Spotify oficial → retornar à leitura voluntariamente.

## Rotas

| Rota | Conteúdo | Interações |
| --- | --- | --- |
| `/` | Hero da mão, conceito, personagens, primeiros capítulos, música | CTAs |
| `/sobre` | Sinopse original, classificação, avisos, nota da autora | AO3/índice |
| `/personagens` | Fichas iniciais de Eduarda, Lorena, Angélica, Cristine etc. | Navegação |
| `/capitulos` | 28 registros | Busca, status de lidos |
| `/capitulos/:slug` | Leitor do capítulo, imagens, notas | Dropdown, ajustes, anterior/próximo, marcar lido |
| `/trilha-sonora` | Faixas verificadas e playlist oficial | Acesso ao Spotify e aos capítulos |
| `*` | Estado 404 | Voltar ao início |

## Funcionalidades implementadas no MVP

- Conteúdo dividido em 28 JSON carregados de forma assíncrona por capítulo.
- Índice completo e busca por número ou título.
- Leitor com tema marfim/escuro, serif/sans, tamanho/entrelinha.
- Navegação e marcação voluntária de capítulo lido (`localStorage`).
- 7 imagens incluídas nos capítulos onde aparecem no PDF.
- Personagens em níveis sem spoilers e soundtrack inicial verificada.
- Links para arquivo original da fic e playlist da Mary.
- Página não encontrada, skip link, labels e estados básicos de acessibilidade.

## Fora de escopo inicial

- Login, perfil, banco de dados, sincronização entre dispositivos.
- Comentários próprios, likes/kudos, sistema de recomendação.
- Reprodução automática de músicas ou hospedagem de faixas comerciais.
- Wiki completa com spoilers, rede de relações secreta e linha do tempo profunda.
- Publicação automática no AO3, integração OAuth ou alteração da fic original.
- Figma e CMS externo.

## Riscos

- **Direitos:** reprodução pública da obra depende de autorização apropriada.
- **Extração PDF:** texto e tipografia podem exigir revisão editorial pontual.
- **Atualizações:** importador atual valida 28 capítulos; crescimento exige adaptação.
- **Performance:** imagens de capítulo devem manter carregamento preguiçoso, e conteúdo JSON vem por rota.
