# 07 — Plano de QA e publicação

## Validações automáticas realizadas na geração

- 28 capítulos consecutivos no manifesto, do 1 ao 28.
- Arquivo de cada capítulo existe e corresponde ao título/slug do índice.
- Blocos de conteúdo não vazios.
- 7 imagens referenciadas existem fisicamente.
- Paridade de abertura/fechamento de `<em>` e `<strong>` e rejeição de markup interativo.
- `scripts/check_content.py`: **aprovado**.

**Não foi possível executar `npm install`/`npm run build` neste ambiente:** o registro npm não resolveu via DNS. Não há alegação de compilação aprovada; executar no Windows antes de publicar.

## Checklist técnica a executar

```bash
npm install
npm run typecheck
npm run build
npm run preview
python scripts/check_content.py
```

## Casos de teste

| ID | Cenário | Critério de aceite | Status |
| --- | --- | --- | --- |
| CT01 | Home desktop | Mão, título, CTA e seções legíveis | Pendente visual |
| CT02 | Home mobile 360/390/414px | Nenhuma rolagem horizontal indevida | Pendente visual |
| CT03 | Índice | Lista 28 títulos na ordem correta | Estrutura validada / UI pendente |
| CT04 | Busca | Número e título filtram corretamente | Pendente funcional |
| CT05 | Seleção | Dropdown abre capítulo correto | Pendente funcional |
| CT06 | Navegação | Cap. 01 sem anterior; cap. 28 sem próximo | Pendente funcional |
| CT07 | Aparência | Tema, fonte, tamanho, entrelinha funcionam | Pendente funcional |
| CT08 | Persistência | Preferências e lidos sobrevivem ao reload | Pendente funcional |
| CT09 | Conteúdo | Texto e notas fiéis ao PDF/AO3 | Revisão editorial pendente |
| CT10 | Imagens | 7 imagens na posição e proporção corretas | Presença validada / visual pendente |
| CT11 | Música | Playlist abre; nenhuma faixa inicia sozinha | Pendente funcional |
| CT12 | Acessibilidade | Teclado, foco, 200% zoom, leitor de tela | Pendente manual |
| CT13 | URL interna | Reload direto em `/capitulos/:slug` | Pendente deploy |
| CT14 | Performance | Sem bloqueio excessivo no 4G mobile | Pendente medir |

## Publicação Vercel

1. Subir o repositório para o GitHub/GitLab.
2. Importar projeto na Vercel.
3. Framework: Vite; build `npm run build`; output `dist`.
4. Conferir `vercel.json` para rotas SPA.
5. Revisar conteúdo sensível, direitos e créditos com a autora antes de divulgar publicamente.
6. Após deploy, testar ao menos a home, cap. 1, cap. 24 (imagens) e cap. 28 (último capítulo).

## Evidências futuras

Separar screenshots de desktop/mobile, relatórios de Lighthouse, checklist de diferenças do PDF e registro de revisões editoriais por capítulo. Evitar incluir imagens de cenas potencialmente sensíveis em materiais públicos sem contexto.
