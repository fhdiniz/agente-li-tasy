# 3 - Grupos e Observações - Inpart → Tasy

> **Sequência de entrega/manual:** 3
> **Direção do fluxo:** Inpart → Tasy
> **Módulo:** `authorization-analysis-management` (V2)

## 3.1 – Finalidade

Este endpoint recebe da Inpart a solicitação para **encaminhar** uma análise de auditoria (guia/solicitação de OPME) a outro grupo auditor, registrando observações no histórico, e **encerra** a análise para o grupo atual.

## 3.2 – Endpoint

| | |
|---|---|
| **Método** | `POST` |
| **Path** | `/api/v2/authorization-analysis-audit-groups/{auditId}/forward-close` |
| **Content-Type** | `application/json` |

### Parâmetro de path

| Parâmetro | Tipo | Descrição | Referência no banco |
|---|---|---|---|
| `auditId` | `Long` | Sequência da análise de auditoria (guia/solicitação OPME) | `PLS_AUDITORIA.NR_SEQUENCIA` |

## 3.3 – Exemplo de Request

```json
{
  "groupId": 8,
  "orderId": 1,
  "notes": "Forwarded for specialist review",
  "username": "Integration"
}
```

### 3.3.1 – Campos de envio

| Propriedade | Obrigatório | Descrição | Origem da informação |
|---|---|---|---|
| `groupId` | Sim | Identificador do grupo auditor de destino. | `PLS_GRUPO_AUDITOR.NR_SEQUENCIA` |
| `orderId` | Não | Identificador da ordem do grupo. | `PLS_AUDITORIA_GRUPO.NR_SEQ_ORDEM` |
| `notes` | Condicional (obrigatório quando a configuração da análise/grupo exigir observação) | Observação a ser gravada no histórico. | `PLS_REQUISICAO_HISTORICO.DS_HISTORICO` |
| `username` | Sim | Usuário responsável pela ação (máx. 15 caracteres). | `PLS_AUDITORIA_GRUPO.NM_USUARIO` |

## 3.4 – Exemplo de Response

```json
{
  "auditId": 123456,
  "forwardedToGroupId": 8,
  "status": "SUCCESS",
  "message": "Analysis forwarded and closed successfully."
}
```

### 3.4.1 – Campos da resposta

| Propriedade | Sempre presente | Descrição | Origem da informação |
|---|---|---|---|
| `auditId` | Sim | Identificador da análise de auditoria. | `PLS_AUDITORIA.NR_SEQUENCIA` |
| `forwardedToGroupId` | Sim | Identificador do grupo que recebeu a análise encaminhada. | `PLS_GRUPO_AUDITOR.NR_SEQUENCIA` |
| `status` | Sim | Status da operação (ex.: `SUCCESS`). | — |
| `message` | Sim | Mensagem legível do resultado. | — |

## 3.5 – Regras de negócio e validações

1. `auditId` (path) deve corresponder a uma análise de auditoria existente.
2. `groupId` é obrigatório e deve corresponder a um grupo auditor existente.
3. O grupo de destino deve estar **ativo**; caso contrário, a operação falha.
4. O grupo de destino deve ser de um tipo disponível para análise de autorização; caso contrário, a operação falha.
5. `username` é sempre obrigatório.
6. Se a configuração exigir observação obrigatória para esta análise, a operação falha quando essa exigência não é atendida.
7. Quando executado com sucesso: a análise é encaminhada ao grupo informado (registrando `notes`/`orderId` no histórico) e encerrada para o grupo atual.

## 3.6 – Respostas de erro

| HTTP Status | Código | Situação |
|---|---|---|
| `400` | `REQUIRED_FIELD` | `auditId` ou `groupId` ausentes/vazios. |
| `404` | `RESOURCE_NOT_FOUND` | Análise de auditoria (`auditId`) ou grupo auditor (`groupId`) não encontrados. |
| `409` | `BUSINESS_RULE` | Grupo de destino inativo, grupo de destino não disponível para esta operação (tipo de grupo), ou observação obrigatória não informada. |
| `415` | `INVALID_FORMAT` | Content-Type não suportado (somente `application/json`). |
| `500` | `INTERNAL_ERROR` | Erro interno inesperado. |

### Exemplo de erro (400)

```json
{
  "status": 400,
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v2/authorization-analysis-audit-groups/123456/forward-close",
  "errors": [
    { "code": "REQUIRED_FIELD", "message": "The field groupId must be informed." }
  ]
}
```

### Exemplo de erro (404)

```json
{
  "status": 404,
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v2/authorization-analysis-audit-groups/123456/forward-close",
  "errors": [
    { "code": "RESOURCE_NOT_FOUND", "message": "The entity for the field auditId was not found on Tasy." }
  ]
}
```

### Exemplo de erro (409)

```json
{
  "status": 409,
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v2/authorization-analysis-audit-groups/123456/forward-close",
  "errors": [
    { "code": "BUSINESS_RULE", "message": "The selected group is currently inactive on Tasy: 10 - Group A." }
  ]
}
```

## 3.7 – Observações adicionais

- Este endpoint reaproveita a mesma lógica de encaminhamento/encerramento utilizada internamente pelo ponto 10 – Itens Autorizados, quando o `outcome` informado é `FORWARD`.
- O encerramento da análise para o grupo atual só é efetivado após o encaminhamento ao novo grupo ser concluído com sucesso.
