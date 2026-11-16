# 0006 — Material de referência interno versionado

**Status:** Aceita (substitui a regra anterior de manter `referencias/` fora do Git)

## Contexto
Os usuários do plugin são da própria Philips. Swaggers, catálogo TIE e LIs de referência são material interno, e o repositório é privado e será migrado para o Git da Philips.

## Decisão
Versionar `referencias/openapi/`, `referencias/tie/` e `referencias/lis-referencia/` no repositório. Documentos de terceiros (`referencias/documentos-terceiros/`) continuam fora do Git.

## Consequências
- Quem instala o plugin já recebe o material de referência; não é preciso distribuir pasta à parte.
- O repositório deve permanecer privado, inclusive após a migração.
- Atualizar um Swagger ou o catálogo TIE vira um commit, com histórico.
