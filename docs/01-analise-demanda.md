# Análise da demanda

## Contexto

Projeto interno de automação de documentação. Objetivo amplo: automatizar documentação de forma escalável para a empresa (desenvolvimento, aderência e outras). Primeiros entregáveis: **LI (Levantamento de Integração)** e **Manual de Operação**.

Primeiro passo combinado: definir o padrão de LI (tópicos, fluxos, imagens) e enviar a lista de tópicos ao grupo para validação.

## Missão

Concluir uma LI baseada em 1 documento de terceiro em no máximo 8h, utilizando IA.

**Adicional:** o agente deve varrer a base de APIs documentada em Swagger e/ou as integrações padrão TIE e cruzar as informações, determinando a viabilidade por OpenAPI x fora do Open, via TIE.

## Documento de terceiro analisado: Evya — Portal 4uHub

- 111 páginas, PDF com texto selecionável (gerado pelo Google Docs); a extração de texto funciona sem OCR.
- Cada endpoint segue o padrão **Resumo / Filtros / SQL**, o que facilita a extração automática.
- **68 endpoints em 12 grupos**, coerente com as "12 áreas de atuação" declaradas no documento. Inconsistência a sinalizar na LI: o índice lista só 11 grupos (falta **HioAuthorization**, 1 endpoint).
- Concentração em Agenda (Calendar and Schedule): 33 endpoints de consulta e exame.
- **Escritas diretas no Oracle do Tasy** (`{database}`): 9 INSERTs (`pessoa_fisica`, `compl_pessoa_fisica` ×2, `pessoa_juridica`, `atendimento_paciente`, `atend_paciente_unidade`, `atend_categoria_convenio`, `pls_conta`, `pls_protocolo_conta`) e 7 UPDATEs (`pessoa_fisica`, `compl_pessoa_fisica`, `agenda_consulta` ×2, `agenda_paciente` ×2, `laudo_paciente`).
- **Escritas no banco do próprio 4uHub** (`forubus`): 14 INSERTs e 3 UPDATEs em tabelas de controle (`CALENDAR*_XL`, `FORUBUSSCHEDCTRL`, `forubus_encounter`). Não são escritas no Tasy e não entram na análise de viabilidade.
- Cerca de 136 objetos distintos do Tasy referenciados, incluindo 31 funções `obter_*` distintas (28 localizadas no repositório PL/SQL do Tasy).
- Mistura escopo hospitalar e OPS (`pls_*`: beneficiário, mensalidade, coparticipação, reembolso).

## Natureza do trabalho

Traduzir acesso SQL direto em contratos suportados do Tasy. Para cada endpoint:

1. Identificar tabelas, colunas e tipo de operação (leitura/escrita).
2. Procurar operação equivalente no OpenAPI.
3. Se não houver, procurar integração padrão no TIE.
4. Se não houver, registrar como gap de desenvolvimento.

As escritas diretas no banco são o ponto mais sensível da análise.

## Classificação de viabilidade (proposta)

| Classe | Significado |
|---|---|
| Coberto por OpenAPI | Existe operação equivalente com os campos necessários |
| Parcial | Existe operação, mas faltam campos ou regras |
| Via TIE | Atendido por integração padrão TIE |
| Gap | Exige desenvolvimento ou customização |
