# 0003 — Template da LI em duas camadas

**Status:** Aceita (19/10/2026: `.docx` oficial atual da Bionexo como base visual; tópicos validados em [05-modelo-li](../05-modelo-li.md))

## Contexto
Existem modelos de LI prontos, com variações entre projetos.

## Decisão
Usar os modelos existentes como matéria-prima para um modelo base canônico, separado em estrutura de conteúdo (YAML/JSON) e template visual (.docx).

Primeira versão: estrutura em `templates/li/estrutura.json` (JSON, sem dependências) e template visual `templates/li/Template de levantamento de integração [OFICIAL].docx`. Ver [05-modelo-li](../05-modelo-li.md).

## Consequências
- O agente preenche sempre a mesma estrutura.
- A geração do documento é determinística.
- Novos tipos de documento reaproveitam o mesmo motor.
