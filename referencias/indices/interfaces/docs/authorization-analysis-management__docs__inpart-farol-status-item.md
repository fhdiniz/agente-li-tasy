# 4 - Farol de Status do Item - Inpart → Tasy

> **Sequência de entrega/manual:** 4
> **Direção do fluxo:** Inpart → Tasy
> **Módulo:** `authorization-analysis-management` (V2)

## 4.1 – Finalidade

Este endpoint recebe da Inpart a atualização do status de autorização (farol) de um item específico de uma análise de auditoria, permitindo aprovar, negar, colocar em pendência ou cancelar a autorização do item no Tasy.

## 4.2 – Endpoint

| | |
|---|---|
| **Método** | `POST` |
| **Path** | `/api/v2/authorization-analysis-audits/items/{auditItemId}/status` |
| **Content-Type** | `application/json` |

### Parâmetro de path

| Parâmetro | Tipo | Descrição | Referência no banco |
|---|---|---|---|
| `auditItemId` | `Long` | Sequência do item da auditoria | `PLS_AUDITORIA_ITEM.NR_SEQUENCIA` |

## 4.3 – Exemplo de Request

```json
{
  "username": "Integration",
  "itemStatus": "A",
  "releaseReasonCode": 123,
  "denialCode": 123
}
```

### 4.3.1 – Campos de envio

| Propriedade | Obrigatório | Descrição | Origem da informação |
|---|---|---|---|
| `username` | Não | Usuário Tasy utilizado nas validações e registrado como responsável pela alteração. | `PLS_AUDITORIA_ITEM.NM_USUARIO` |
| `itemStatus` | Sim | Status a ser aplicado ao item (domínio Tasy 3544). Valores aceitos: `A` (Aprovado), `N` (Negado), `P` (Pendente), `C` (Cancelado). | `PLS_AUDITORIA_ITEM.IE_STATUS` |
| `releaseReasonCode` | Condicional (obrigatório quando `itemStatus` = `A` ou `N`) | Motivo de liberação da análise. | `PLS_MOTIVO_LIB_ANALISE_AUT.NR_SEQUENCIA` |
| `denialCode` | Condicional (relevante apenas quando `itemStatus` = `N` e o usuário tiver permissão para registrar motivo de glosa) | Código do motivo de glosa TISS. | `TISS_MOTIVO_GLOSA.CD_MOTIVO_TISS` |

## 4.4 – Exemplo de Response

> Retornado com **HTTP 200**, sem corpo de resposta, quando o status do item é atualizado com sucesso.

## 4.5 – Regras de negócio e validações

1. `itemStatus` é sempre obrigatório e aceita somente os valores `A` (Aprovado), `N` (Negado), `P` (Pendente) ou `C` (Cancelado); qualquer outro valor é rejeitado.
2. Quando `itemStatus` = `A` (Aprovado) ou `N` (Negado):
   - `releaseReasonCode` é obrigatório e deve corresponder a um motivo de liberação existente.
   - O item não pode ser alterado se já tiver sido executado (de acordo com a origem da requisição: guia, solicitação ou execução).
   - Se `itemStatus` = `N` (Negado), o usuário tiver permissão para registrar motivo de glosa e `denialCode` for informado, o código deve corresponder a um motivo de glosa TISS existente; após o registro da glosa, é necessário que exista ao menos um motivo de glosa associado ao item, caso contrário a operação falha.
3. Quando `itemStatus` = `P` (Pendente), o item é apenas marcado como pendente, sem exigência de motivo de liberação ou glosa.
4. Quando `itemStatus` = `C` (Cancelado), o item é removido/cancelado da análise de auditoria.

## 4.6 – Respostas de erro

| HTTP Status | Código | Situação |
|---|---|---|
| `400` | `REQUIRED_FIELD` | `itemStatus` não informado, ou `releaseReasonCode` não informado quando obrigatório. |
| `400` | `INVALID_ARGUMENT` | Valor de `itemStatus` não suportado para esta operação. |
| `404` | `RESOURCE_NOT_FOUND` | Item de auditoria, motivo de liberação ou motivo de glosa TISS não encontrados. |
| `409` | `BUSINESS_RULE` | O status do item não pode ser alterado porque já foi executado, ou nenhum motivo de glosa foi registrado para o item quando exigido. |
| `415` | `INVALID_FORMAT` | Content-Type não suportado (somente `application/json`). |
| `500` | `INTERNAL_ERROR` | Erro interno inesperado. |

### Exemplo de erro (400)

```json
{
  "status": 400,
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v2/authorization-analysis-audits/items/789/status",
  "errors": [
    { "code": "REQUIRED_FIELD", "message": "Reason for analysis release not informed." }
  ]
}
```

### Exemplo de erro (404)

```json
{
  "status": 404,
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v2/authorization-analysis-audits/items/789/status",
  "errors": [
    { "code": "RESOURCE_NOT_FOUND", "message": "Audit item not found for the given Id: 789" }
  ]
}
```

### Exemplo de erro (409)

```json
{
  "status": 409,
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v2/authorization-analysis-audits/items/789/status",
  "errors": [
    { "code": "BUSINESS_RULE", "message": "The status of the item cannot be changed because it has already been executed. Please check." }
  ]
}
```

## 4.7 – Observações adicionais

- Este endpoint é a contrapartida, no fluxo **Inpart → Tasy**, do envio do farol de status feito pelo Tasy à Inpart (ponto 5 – Farol de Status do Item, sentido Tasy → Inpart).
- Este mesmo endpoint também é utilizado internamente pelo Tasy ao processar os itens autorizados recebidos da Inpart (ponto 10 – Itens Autorizados), aplicando automaticamente o status `A` (Aprovado) a cada item sincronizado.
