# 0008 — Código-fonte interno: indexar, não versionar

**Status:** Aceita

## Contexto
Foram obtidos três repositórios internos da Philips como referência (`referencias/*.zip`):

| Arquivo | Conteúdo | Uso no agente |
|---|---|---|
| `emr-tasy-plsql-dev.zip` | ~77 mil objetos PL/SQL do Tasy (procedures, functions, packages, triggers, views) por schema | Resolver funções `obter_*` e procedures citadas pelo terceiro; saber quem grava cada tabela |
| `tasy-interfaces-dev.zip` | Código Java das APIs OpenAPI (~150 módulos, ~700 entidades JPA com `@Table`) | De-para tabela → API, inclusive das APIs em Swagger 2.0 sem `Referenced Table` |
| `tie-integrations-master.zip` | Catálogo TIE oficial: 228 integrações, 1.477 arquivos `.bft` (JSON: eventos, rotas Camel, schemas) | Classificação "Via TIE" |

São ~155 MB compactados (~860 MB extraídos) e são código-fonte de repositórios privados da Philips (`philips-internal`).

## Decisão
Não versionar os `.zip` nem o conteúdo extraído. O servidor MCP gera, a partir deles, **índices compactos** (tabela → APIs, tabela → integrações TIE, objeto PL/SQL → tabelas lidas/gravadas), e só os índices são versionados.

Os `.zip` são usados uma vez para gerar os índices e depois apagados. Os índices ficam em `referencias/indices/` (ver o [README](../../referencias/indices/README.md)) e os scripts que os geram em `mcp-server/extratores/`.

## Consequências
- Repositório sem cópia de código-fonte da Philips em conta pessoal: só metadados (nomes, assinaturas, tabelas, endpoints, eventos) e documentação.
- Índices somam ~41 MB, versionáveis.
- Para atualizar os índices é preciso obter de novo os repositórios e rodar os extratores.
- Após a migração para o Git da Philips, avaliar gerar os índices direto dos repositórios originais.
