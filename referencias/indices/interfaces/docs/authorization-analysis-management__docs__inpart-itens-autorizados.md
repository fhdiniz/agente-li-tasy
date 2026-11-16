# 10 - Itens Autorizados - Inpart → Tasy

> **Sequência de entrega/manual:** 10
> **Direção do fluxo:** Inpart → Tasy
> **Módulo:** `authorization-analysis-management` (V2)

## 10.1 – Finalidade

Este endpoint recebe da Inpart a lista de itens (procedimentos e/ou materiais) **autorizados** para uma análise de auditoria (guia/solicitação de OPME) e sincroniza esses dados no Tasy. Cada item é inserido (se novo) ou atualizado (se já existir) e, ao final, todos os itens da análise são marcados como `APPROVED`. Dependendo do resultado, a análise é encaminhada para outro grupo auditor ou encerrada.

## 10.2 – Endpoint

| | |
|---|---|
| **Método** | `POST` |
| **Path** | `/api/v2/authorization-analysis-audits/{auditId}/approved-items` |
| **Content-Type** | `application/json` |

### Parâmetro de path

| Parâmetro | Tipo | Descrição | Referência no banco |
|---|---|---|---|
| `auditId` | `Long` | Sequência da análise de auditoria (guia/solicitação OPME) | `PLS_AUDITORIA.NR_SEQUENCIA` |

## 10.3 – Exemplo de Request

```json
{
  "items": [
    {
      "procedureCode": 40808,
      "procedureOrigin": "1",
      "procedureQuantity": 1
    },
    {
      "auditItemId": 789,
      "materialId": 45678,
      "materialQuantity": 2,
      "materialValue": 150.00,
      "supplierSeq": 321,
      "price": 150.00
    }
  ],
  "outcome": "FORWARD",
  "groupId": 8,
  "orderId": 1,
  "notes": "Todos os itens autorizados",
  "username": "Integration",
  "releaseReasonCode": 123
}
```

### 10.3.1 – Campos de envio (raiz)

| Propriedade | Obrigatório | Descrição | Origem da informação |
|---|---|---|---|
| `items` | Sim | Lista de itens autorizados a serem sincronizados. Ao menos 1 elemento. | — |
| `outcome` | Sim | Resultado a ser executado após todos os itens serem sincronizados e aprovados. Valores aceitos como entrada: `FORWARD` (encaminha a análise para outro grupo e a encerra para o grupo atual) e `CLOSE` (encerra a análise por completo). `NOT_EXECUTED` **não** é aceito como entrada — é somente de resposta. | — |
| `groupId` | Condicional (obrigatório quando `outcome = FORWARD`) | Identificador do grupo auditor de destino. | `PLS_GRUPO_AUDITOR.NR_SEQUENCIA` |
| `orderId` | Não | Identificador da ordem do grupo. Relevante apenas quando `outcome = FORWARD`. | `PLS_AUDITORIA_GRUPO.NR_SEQ_ORDEM` |
| `notes` | Condicional (obrigatório se o grupo de destino exigir observações) | Observação a ser gravada no histórico. | `PLS_REQUISICAO_HISTORICO.DS_HISTORICO` |
| `username` | Sim | Usuário responsável pela ação (máx. 15 caracteres). | `PLS_AUDITORIA_GRUPO.NM_USUARIO` |
| `releaseReasonCode` | Sim | Motivo de liberação da análise, utilizado sempre que um item precisa ser definido como `APPROVED`. | `PLS_MOTIVO_LIB_ANALISE_AUT.NR_SEQUENCIA` |

### 10.3.2 – Campos de envio (cada item de `items`)

| Propriedade | Obrigatório | Descrição | Origem da informação |
|---|---|---|---|
| `auditItemId` | Não | Sequência do item da auditoria. Quando informado, o item é **atualizado**; quando ausente, é **inserido**. | `PLS_AUDITORIA_ITEM.NR_SEQUENCIA` |
| `procedureCode` | Condicional (obrigatório se o item for um procedimento; não pode ser informado junto com `materialId`) | Código do procedimento. A presença deste campo marca o item como procedimento (mutuamente exclusivo com `materialId`). | `PLS_AUDITORIA_ITEM.CD_PROCEDIMENTO` |
| `procedureOrigin` | Condicional (obrigatório quando o item é procedimento) | Origem do procedimento (domínio 30). | `PLS_AUDITORIA_ITEM.IE_ORIGEM_PROCED` |
| `procedureQuantity` | Condicional (obrigatório quando o item é procedimento) | Quantidade do procedimento (> 0). | `PLS_AUDITORIA_ITEM.QT_ITEM_PROC` |
| `materialId` | Condicional (obrigatório se o item for um material; não pode ser informado junto com `procedureCode`) | Sequência do material. A presença deste campo marca o item como material (mutuamente exclusivo com `procedureCode`) e é a chave para buscar dados adicionais do cadastro de materiais. | `PLS_AUDITORIA_ITEM.NR_SEQ_MATERIAL` |
| `materialQuantity` | Condicional (obrigatório quando o item é material) | Quantidade do material (> 0). | `PLS_AUDITORIA_ITEM.QT_ITEM_MAT` |
| `materialValue` | Não | Valor do material na auditoria. | `PLS_AUDITORIA_ITEM.VL_MATERIAL` |
| `initialValue` | Não | Valor inicial (utilizado somente na inserção). | `PLS_AUDITORIA_ITEM.VL_INICIAL` |
| `anvisaRegistration` | Não | Registro ANVISA do material. | `PLS_AUDITORIA_ITEM.NR_REGISTRO_ANVISA` |
| `manufacturerReference` | Não | Referência do fabricante do material. | `PLS_AUDITORIA_ITEM.CD_REF_FABRICANTE_IMP` |
| `supplierSeq` | Não | Sequência do fornecedor do material. | `PLS_AUDITORIA_ITEM.NR_SEQ_FORNEC` |
| `providerCode` | Não | Código do prestador/fornecedor. | `PLS_AUDITORIA_ITEM.CD_PREST_FORNEC` |
| `price` | Não | Preço (cenário de federação de convênios). | `PLS_AUDITORIA_ITEM.VL_PRECO` |

> Regra: cada item deve conter **exatamente um** entre `procedureCode` e `materialId`.

## 10.4 – Exemplo de Response

```json
{
  "items": [
    {
      "auditItemId": 456789,
      "status": "SUCCESS",
      "operation": "INSERTED",
      "message": null
    },
    {
      "auditItemId": 789,
      "status": "SUCCESS",
      "operation": "UPDATED",
      "message": null
    }
  ],
  "outcome": {
    "type": "FORWARD",
    "groupId": 8,
    "closedAt": "2026-04-02T14:35:00Z",
    "reason": null,
    "message": "Analysis forwarded and closed successfully."
  }
}
```

### 10.4.1 – Campos da resposta (`items[]`)

| Propriedade | Sempre presente | Descrição | Origem da informação |
|---|---|---|---|
| `auditItemId` | Condicional (pode ser nulo em falhas de inserção) | Sequência do item da auditoria. Presente em caso de sucesso (inserido ou atualizado) e em falhas de atualização; pode ser nulo em falhas de inserção. | `PLS_AUDITORIA_ITEM.NR_SEQUENCIA` |
| `status` | Sim | Resultado do processamento do item: `SUCCESS` ou `FAILED`. | — |
| `operation` | Condicional (somente em caso de sucesso) | Operação aplicada ao item em caso de sucesso: `INSERTED` ou `UPDATED`; nulo quando o item falhou. | — |
| `message` | Condicional (somente em caso de falha) | Mensagem de falha, quando o item não pôde ser processado; nulo em caso de sucesso. | — |

### 10.4.2 – Campos da resposta (`outcome`)

| Propriedade | Sempre presente | Descrição | Origem da informação |
|---|---|---|---|
| `type` | Sim | Resultado executado: `FORWARD`, `CLOSE` ou `NOT_EXECUTED` (quando ao menos um item falhou ao sincronizar ou ao ser aprovado). | — |
| `groupId` | Condicional (somente quando `type = FORWARD`) | Identificador do grupo que recebeu a análise encaminhada. | `PLS_AUDITORIA_GRUPO.NR_SEQUENCIA` (grupo destino) |
| `closedAt` | Condicional (somente quando `type = FORWARD` ou `CLOSE`) | Momento em que a análise foi encaminhada/encerrada. | Data/hora atual do sistema |
| `reason` | Condicional (somente quando `type = NOT_EXECUTED`) | Explica quais itens falharam e por que o `outcome` não foi executado. | — |
| `message` | Sim | Mensagem legível do resultado. | — |

## 10.5 – Regras de negócio e validações

1. O corpo da requisição não pode ser vazio e deve conter ao menos 1 item em `items`.
2. Cada item deve conter exatamente um entre `procedureCode` e `materialId` — nunca os dois, nunca nenhum.
3. Se o item for procedimento: `procedureOrigin` é obrigatório e `procedureQuantity` deve ser maior que zero.
4. Se o item for material: `materialQuantity` deve ser maior que zero.
5. `outcome` é obrigatório; o valor `NOT_EXECUTED` não é aceito como entrada (é somente de resposta).
6. Quando `outcome = FORWARD`, `groupId` é obrigatório.
7. `username` e `releaseReasonCode` são sempre obrigatórios.
8. Os itens são processados **sequencialmente** e cada um é persistido (commit) conforme processado — a operação **não é atômica**: se um item falhar, os itens já processados permanecem persistidos.
9. Após sincronizar os itens informados, o serviço garante que **todos** os itens da auditoria (inclusive os que não vieram nesta requisição) fiquem com status `APPROVED`, usando o `releaseReasonCode` informado.
10. O `outcome` (`FORWARD`/`CLOSE`) só é executado se **todos** os itens da auditoria estiverem sincronizados e aprovados com sucesso; caso contrário, a resposta reporta `NOT_EXECUTED` e nenhum encaminhamento/encerramento é realizado.
11. Em `FORWARD`, a análise é encaminhada ao grupo (`groupId`/`orderId`) e encerrada para o grupo atual. Em `CLOSE`, a análise é encerrada por completo (libera o master da auditoria e encerra para o grupo atual).
12. Se o grupo de destino exigir observações obrigatórias e `notes` não for informado, a operação falha com `BUSINESS_RULE`.

## 10.6 – Respostas de erro

| HTTP Status | Código | Situação |
|---|---|---|
| `400` | `REQUIRED_FIELD` / `INVALID_ARGUMENT` | Requisição inválida (corpo vazio, lista de itens vazia, campo obrigatório ausente, `groupId` ausente quando `outcome = FORWARD`, item com `procedureCode` e `materialId` juntos ou nenhum dos dois). |
| `404` | `RESOURCE_NOT_FOUND` | Análise de auditoria (`auditId`), item de auditoria, grupo auditor ou motivo de liberação não encontrados. |
| `409` | `INCONSISTENT_DATA` | O item de auditoria informado pertence a outra análise (`auditId` divergente). |
| `409` | `BUSINESS_RULE` | Grupo de destino inativo/indisponível para a operação, observações obrigatórias não informadas, ou item já executado e não pode ser alterado. |
| `415` | `INVALID_FORMAT` | Content-Type não suportado (somente `application/json`). |
| `500` | `INTERNAL_ERROR` | Erro interno inesperado. |

### Exemplo de erro (400)

```json
{
  "status": 400,
  "timestamp": "2026-04-02T14:30:00Z",
  "path": "/api/v2/authorization-analysis-audits/123456/approved-items",
  "errors": [
    { "code": "REQUIRED_FIELD", "message": "The field items must contain at least one element." }
  ]
}
```

## 10.7 – Observações adicionais

- Este endpoint é a contrapartida, no fluxo **Inpart → Tasy**, do envio de itens cotados feito pela Inpart (ponto 9 – Itens Cotados); a diferença é que aqui os itens já vêm com o resultado de autorização e o objetivo final é aprovar e encerrar/encaminhar a análise.
- Ao inserir um item novo vinculado a uma solicitação/guia de cuidado inter-operadora, o sistema também gera o mapeamento inter-operadora (procedimento/material) correspondente.
