---
name: analisar-viabilidade
description: Analisa se os pontos de integração pedidos por um terceiro são atendidos pelo Tasy por API padrão (OpenAPI/Swagger), parcialmente, por integração TIE fora do Open, ou se são gap de produto, e entrega a matriz interna de viabilidade em .xlsx. Use quando pedirem "analise a viabilidade", "dá para fazer por API?", "isso é OpenAPI ou TIE?" ou a matriz de viabilidade, sem gerar a LI completa.
---

# Analisar viabilidade

1. Peça o documento do terceiro (ou a lista de pontos) e a pasta de saída.
2. Extraia os pontos: `extrair_requisitos`; se não se aplicar, leia o documento, chame `formatos` (item 4) e monte o `requisitos.json`. SQL passa por `analisar_sql`.
3. `classificar_viabilidade` gera `classificacao.json` e a matriz `.xlsx`.
4. Revise as linhas de confiança **Baixa** com `buscar_apis` (termos em inglês), `detalhar_api`, `consultar_tabela`, `buscar_tie` e `consultar_plsql`. Corrija `classificacao.json` quando a evidência mostrar outra classe e rode `classificar_viabilidade` de novo só se mudou o `requisitos.json`.
5. Responda com: total por classe, os pontos que mais preocupam (gaps e escritas diretas no banco), as dúvidas para o terceiro e o caminho da matriz.

Classes: **OpenAPI** (API padrão cobre), **Parcial** (API existe, faltam campos), **TIE** (sem API; viável por integração TIE), **Gap** (exige desenvolvimento). Explique sempre a evidência: qual API, qual tabela, quais campos faltam.

A matriz é de **uso interno**: não vai ao cliente. O que estiver em amarelo cabe análise do consultor.
