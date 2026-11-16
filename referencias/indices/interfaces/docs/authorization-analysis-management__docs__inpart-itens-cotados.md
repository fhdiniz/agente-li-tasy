# 9 - Itens Cotados - Inpart → Tasy

> **Sequência de entrega/manual:** 9
> **Direção do fluxo:** Inpart → Tasy
> **Módulo:** `authorization-analysis-management` (V2)

## 9.1 – Finalidade

Este endpoint recebe da Inpart a lista de itens (procedimentos e/ou materiais) **cotados** para uma análise de auditoria (guia/solicitação de OPME) e sincroniza esses dados no Tasy, inserindo os itens novos e atualizando os já existentes.

## 9.2 – Endpoint

| | |
|---|---|
| **Método** | `POST` |
| **Path** | `/api/v2/authorization-analysis-audits/{auditId}/items` |
| **Content-Type** | `application/json` |

### Parâmetro de path

| Parâmetro | Tipo | Descrição | Referência no banco |
|---|---|---|---|
| `auditId` | `Long` | Sequência da análise de auditoria (guia/solicitação OPME) | `PLS_AUDITORIA.NR_SEQUENCIA` |

## 9.3 – Exemplo de Request

```json
{
  "items": [
    {
      "procedureCode": 10101012,
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
  "username": "Integration"
}
```

### 9.3.1 – Campos de envio (raiz)

| Propriedade | Obrigatório | Descrição | Origem da informação |
|---|---|---|---|
| `items` | Sim | Lista de itens cotados a serem sincronizados. Ao menos 1 elemento. | — |
| `username` | Sim | Usuário responsável pela ação, utilizado para persistir os itens sincronizados. | `PLS_AUDITORIA_ITEM.NM_USUARIO` |

### 9.3.2 – Campos de envio (cada item de `items`)

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

## 9.4 – Exemplo de Response

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
  ]
}
```

### 9.4.1 – Campos da resposta (`items[]`)

| Propriedade | Sempre presente | Descrição | Origem da informação |
|---|---|---|---|
| `auditItemId` | Condicional (pode ser nulo em falhas de inserção) | Sequência do item da auditoria. Presente em caso de sucesso (inserido ou atualizado) e em falhas de atualização; pode ser nulo em falhas de inserção. | `PLS_AUDITORIA_ITEM.NR_SEQUENCIA` |
| `status` | Sim | Resultado do processamento do item: `SUCCESS` ou `FAILED`. | — |
| `operation` | Condicional (somente em caso de sucesso) | Operação aplicada ao item em caso de sucesso: `INSERTED` ou `UPDATED`; nulo quando o item falhou. | — |
| `message` | Condicional (somente em caso de falha) | Mensagem de falha, quando o item não pôde ser processado; nulo em caso de sucesso. | — |

## 9.5 – Regras de negócio e validações

1. O corpo da requisição não pode ser vazio e deve conter ao menos 1 item em `items`.
2. `username` é obrigatório.
3. Cada item deve conter exatamente um entre `procedureCode` e `materialId` — nunca os dois, nunca nenhum.
4. Se o item for procedimento: `procedureOrigin` é obrigatório e `procedureQuantity` deve ser maior que zero.
5. Se o item for material: `materialQuantity` deve ser maior que zero.
6. Quando `auditItemId` é informado, o item é atualizado; quando ausente, é inserido.
7. Os itens são processados **sequencialmente** e cada um é persistido (commit) conforme processado — a operação **não é atômica**: se um item falhar, os itens já processados permanecem persistidos.
8. Ao inserir um item novo vinculado a uma solicitação/guia de cuidado inter-operadora, o sistema também gera o mapeamento inter-operadora (procedimento/material) correspondente.

## 9.6 – Respostas de erro

| HTTP Status | Código | Situação |
|---|---|---|
| `400` | `REQUIRED_FIELD` / `INVALID_ARGUMENT` | Requisição inválida (corpo vazio, lista de itens vazia, campo obrigatório ausente, item com `procedureCode` e `materialId` juntos ou nenhum dos dois). |
| `404` | `RESOURCE_NOT_FOUND` | Análise de auditoria (`auditId`) ou item de auditoria não encontrados. |
| `409` | `INCONSISTENT_DATA` | O item de auditoria informado pertence a outra análise (`auditId` divergente). |
| `415` | `INVALID_FORMAT` | Content-Type não suportado (somente `application/json`). |
| `500` | `INTERNAL_ERROR` | Erro interno inesperado. |

### Exemplo de erro (400)

```json
{
  "status": 400,
  "timestamp": "2026-04-02T14:30:00Z",
  "path": "/api/v2/authorization-analysis-audits/123456/items",
  "errors": [
    { "code": "REQUIRED_FIELD", "message": "The field items must contain at least one element." }
  ]
}
```

## 9.7 – Observações adicionais

- Este endpoint é o ponto de partida, no fluxo **Inpart → Tasy**, do recebimento dos itens cotados pela Inpart; após a análise, os itens já autorizados são enviados por meio do ponto 10 – Itens Autorizados, que reaproveita a mesma estrutura de item, acrescentando a definição do status de aprovação e o encaminhamento/encerramento da análise.
- Diferente do ponto 10, este endpoint não altera o status de aprovação dos itens nem encaminha/encerra a análise — apenas sincroniza os dados cotados.
