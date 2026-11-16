---
name: consultar-tasy
description: Responde perguntas sobre a base de conhecimento do Tasy usada nas integrações - APIs padrão (Swagger/OpenAPI), campos e tabelas que cada API expõe, integrações e eventos do catálogo TIE, e procedures PL/SQL. Use quando perguntarem "existe API para X?", "qual API grava a tabela Y?", "tem integração TIE para Z?", "que evento dispara quando...?" ou "o que essa procedure grava?".
---

# Consultar a base do Tasy

Use as ferramentas do servidor MCP `agente-li-tasy`; nunca abra os índices ou Swaggers inteiros.

| Pergunta | Ferramenta |
|---|---|
| Existe API para um assunto? | `buscar_apis` (palavras em inglês, como no Swagger: schedule, encounter, natural person, invoice) |
| Campos de uma API e a tabela/coluna do Tasy de cada um | `detalhar_api` |
| O que existe para uma tabela (APIs, PL/SQL que grava, eventos e integrações TIE) | `consultar_tabela` |
| Existe integração TIE? | `buscar_tie`, depois `detalhar_tie` |
| O que uma procedure grava ou dispara | `consultar_plsql` |
| Tabelas e colunas usadas num SQL | `analisar_sql` |

Ao responder:

- Cite a evidência: método e path da API, arquivo Swagger, arquivo `.bft`, objeto PL/SQL.
- Diga o que a base **não** cobre: SQL dinâmico, colunas sem anotação no Swagger, de-para dos mapeamentos do TIE, versões diferentes da fotografia da base.
- Não confirme que algo "não existe no Tasy" só porque não está nos índices: diga "não encontrado na base de conhecimento".
