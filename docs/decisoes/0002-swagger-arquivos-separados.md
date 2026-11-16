# 0002 — Swagger mantido em arquivos separados

**Status:** Aceita

## Contexto
Cada API do OpenAPI do Tasy tem seu próprio arquivo Swagger.

## Decisão
Manter um arquivo por API. O servidor MCP indexa a pasta inteira na inicialização.

## Consequências
- Evita colisão de nomes de schemas (`$ref`) que um merge geraria.
- Atualizar uma API significa trocar um único arquivo.
- O agente consulta o índice, sem carregar os Swaggers inteiros no contexto.
