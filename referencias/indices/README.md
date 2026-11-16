# Índices de referência

Gerados a partir de três repositórios internos da Philips (recebidos como `.zip` em 12/10/2026 e depois descartados, ver [decisão 0008](../../docs/decisoes/0008-codigo-fonte-indexar-nao-versionar.md)). Os scripts que geram cada índice estão em [`mcp-server/extratores/`](../../mcp-server/extratores/).

O agente usa estes arquivos para responder, para cada tabela ou operação do terceiro: **existe API padrão? existe integração TIE? quem grava isso no Tasy?**

## Comece por aqui

**`tabelas.json`** — índice único por tabela do Tasy (~11 mil tabelas), cruzando todas as fontes:

| Chave | Significado |
|---|---|
| `openapi` | Operações dos Swaggers (`referencias/openapi`) que citam a tabela em `Referenced Table` |
| `interfaces_escrita` | Endpoints do tasy-interfaces cujo código grava a tabela em SQL (INSERT/UPDATE/DELETE/MERGE) |
| `interfaces_jpa` | Endpoints que alcançam uma entidade JPA mapeada para a tabela (leitura **ou** escrita) |
| `entidades_jpa` | Classes Java mapeadas para a tabela |
| `plsql_escrita` | Procedures, functions, triggers e packages que gravam na tabela |
| `tie_eventos` | Eventos TIE disparados por triggers da tabela |
| `tie_integracoes` | Integrações TIE ligadas à tabela (pelo evento ou pela API do Tasy que chamam) |

Cada chave traz `total` e até 40 `itens`. Para a lista completa, use os índices de origem abaixo.

## Índices de origem

| Arquivo | Origem | Conteúdo |
|---|---|---|
| `interfaces/endpoints.json` | tasy-interfaces (Java) | 2.105 endpoints REST: método, path, módulo, classe, resumo, tabelas gravadas/lidas em SQL, entidades JPA e procedures chamadas |
| `interfaces/entidades.json` | tasy-interfaces | 698 tabelas mapeadas em JPA, com as colunas usadas pela API |
| `interfaces/docs/` | tasy-interfaces | Documentação Markdown que estava no código |
| `plsql/objetos.jsonl` | emr-tasy-plsql | ~73 mil objetos PL/SQL, um por linha: `s` schema, `t` tipo, `n` nome, `sig` assinatura, `desc` comentário inicial, `w` tabelas gravadas, `r` tabelas lidas, `on` tabela do trigger, `ev` eventos TIE disparados, `ag` códigos de `gravar_agend_integracao` |
| `plsql/tabelas_escrita.json` | emr-tasy-plsql | Tabela → objetos que gravam nela |
| `plsql/eventos_tie.json` | emr-tasy-plsql | Evento TIE → objeto que dispara (`call_bifrost_content`), tabela do trigger e função que monta o payload |
| `plsql/agend_integracao.json` | emr-tasy-plsql | Código de `gravar_agend_integracao` (integrações HL7 legadas) → objetos que disparam |
| `tie/catalogo.json` | tie-integrations | 1.477 arquivos `.bft` de 228 integrações: integrações, eventos, rotas, conectores, fluxos (URIs, APIs do Tasy chamadas, métodos HTTP) e mapeamentos |
| `tie/eventos.json` | tie-integrations | Evento → arquivos `.bft` que o tratam |
| `tie/apis.json` | tie-integrations | Path de API do Tasy → integrações que a chamam |
| `tie/readmes/` | tie-integrations | README de cada integração (existe em poucas) |
| `tie/manuais/` | tie-integrations | 13 manuais de integração convertidos para Markdown (inclui o modelo oficial "MI - API Atendimentos") |

## Limites conhecidos

- **Ligação endpoint → tabela é heurística**: segue as referências entre classes do mesmo módulo (Resource → Service → Repository → Entity/SQL). Pode trazer tabelas apenas consultadas; `interfaces_jpa` não distingue leitura de escrita.
- **PL/SQL**: tabelas extraídas por padrão de texto (`INSERT INTO`, `UPDATE`, `FROM`...). SQL dinâmico (`EXECUTE IMMEDIATE` com texto montado) não é capturado. Scripts (`.scr`, `.bac`) não foram indexados.
- **Não há dicionário de dados completo**: o repositório PL/SQL não traz DDL de tabelas. Colunas conhecidas vêm das entidades JPA e dos Swaggers.
- **TIE**: os schemas de evento quase sempre estão vazios no `.bft`; os campos reais estão nos mapeamentos e nas APIs chamadas. Endereços de host e credenciais foram removidos de propósito.
- **Versão**: fotografia de 12/10/2026 (branches `dev`/`master`). Para atualizar, rode os extratores com os repositórios novos.
