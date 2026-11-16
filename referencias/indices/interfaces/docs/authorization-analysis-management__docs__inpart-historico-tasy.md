# 6 - Histórico TASY - Inpart → Tasy

> **Sequência de entrega/manual:** 6
> **Direção do fluxo:** Inpart → Tasy
> **Módulo:** `authorization-analysis-management` (V2)

## 6.1 – Finalidade

Este endpoint recebe da Inpart um novo registro de **histórico** para uma requisição de análise de auditoria (guia/solicitação de OPME), permitindo registrar no Tasy eventos como autorizações, liberações, mensagens e alterações de status ocorridos durante o processamento da requisição.

## 6.2 – Endpoint

| | |
|---|---|
| **Método** | `POST` |
| **Path** | `/api/v2/authorization-analysis-historical-requests` |
| **Content-Type** | `application/json` |

## 6.3 – Exemplo de Request

```json
{
  "requestId": 100,
  "historicalType": "AP",
  "historical": "Histórico da requisição",
  "historicalDate": "2024-01-15T10:30:00Z",
  "userName": "tasy",
  "idInsured": 200,
  "historicalOrigin": "A",
  "historicalRequestId": 10,
  "idItem": 1,
  "statusAnalysis": "A",
  "idGroup": 5,
  "reasonReleaseId": 3,
  "executionId": 7,
  "auditorFinalizes": "N",
  "timezone": "America/Sao_Paulo"
}
```

### 6.3.1 – Campos de envio

| Propriedade | Obrigatório | Descrição | Origem da informação |
|---|---|---|---|
| `requestId` | Sim | Identificador da requisição à qual o histórico pertence. Deve existir previamente. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_REQUISICAO` |
| `historicalType` | Sim | Tipo do histórico. Valores aceitos: `AM`, `AP`, `J`, `L`, `M`, `R`, `RGA`, `SGA`. | `PLS_REQUISICAO_HISTORICO.IE_TIPO_HISTORICO` |
| `historical` | Sim | Descrição/texto do histórico (até 4000 caracteres). | `PLS_REQUISICAO_HISTORICO.DS_HISTORICO` |
| `historicalDate` | Sim | Data e hora do evento registrado no histórico. | `PLS_REQUISICAO_HISTORICO.DT_HISTORICO` |
| `userName` | Sim | Usuário responsável pelo registro (máx. 15 caracteres). | `PLS_REQUISICAO_HISTORICO.NM_USUARIO` |
| `idInsured` | Não | Identificador do segurado relacionado ao histórico. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_SEGURADO` |
| `historicalOrigin` | Sim | Origem do histórico. Valores aceitos: `A` (Auditor) ou `M` (Médico/Manual). | `PLS_REQUISICAO_HISTORICO.IE_ORIGEM_HISTORICO` |
| `historicalRequestId` | Condicional (se informado, deve existir) | Histórico pai/relacionado, quando este registro é um desdobramento de outro histórico. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_HISTORICO` |
| `idItem` | Não | Identificador do item da auditoria relacionado ao histórico. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_ITEM` |
| `statusAnalysis` | Não | Status da análise no momento do registro (até 10 caracteres). | `PLS_REQUISICAO_HISTORICO.IE_STATUS_ANALISE` |
| `idGroup` | Não | Identificador do grupo auditor relacionado ao histórico. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_GRUPO` |
| `reasonReleaseId` | Condicional (se informado, deve existir) | Motivo de liberação relacionado ao histórico. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_MOTIVO_LIB` |
| `executionId` | Condicional (se informado, deve existir) | Identificador da execução relacionada ao histórico. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_EXECUCAO` |
| `auditorFinalizes` | Não | Indica se o auditor finaliza a análise neste evento (1 caractere). | `PLS_REQUISICAO_HISTORICO.IE_AUDITOR_FINALIZA` |
| `timezone` | Não | Fuso horário de referência do evento (até 40 caracteres). | `PLS_REQUISICAO_HISTORICO.DS_TIMEZONE` |

## 6.4 – Exemplo de Response

> Retornado com **HTTP 201 (Created)** quando o histórico é criado com sucesso.

```json
{
  "id": 1,
  "requestId": 100,
  "historicalType": "AP",
  "historical": "Histórico da requisição",
  "historicalDate": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T11:00:00Z",
  "userName": "tasy",
  "idInsured": 200,
  "historicalOrigin": "A",
  "historicalRequestId": 10,
  "idItem": 1,
  "statusAnalysis": "A",
  "idGroup": 5,
  "reasonReleaseId": 3,
  "executionId": 7,
  "auditorFinalizes": "N",
  "timezone": "America/Sao_Paulo"
}
```

### 6.4.1 – Campos da resposta

| Propriedade | Sempre presente | Descrição | Origem da informação |
|---|---|---|---|
| `id` | Sim | Identificador do histórico criado. | `PLS_REQUISICAO_HISTORICO.NR_SEQUENCIA` |
| `requestId` | Sim | Identificador da requisição à qual o histórico pertence. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_REQUISICAO` |
| `historicalType` | Sim | Tipo do histórico. | `PLS_REQUISICAO_HISTORICO.IE_TIPO_HISTORICO` |
| `historical` | Sim | Descrição/texto do histórico. | `PLS_REQUISICAO_HISTORICO.DS_HISTORICO` |
| `historicalDate` | Sim | Data e hora do evento registrado no histórico. | `PLS_REQUISICAO_HISTORICO.DT_HISTORICO` |
| `updatedAt` | Sim | Data e hora da última atualização do registro. | `PLS_REQUISICAO_HISTORICO.DT_ATUALIZACAO` |
| `userName` | Sim | Usuário responsável pelo registro. | `PLS_REQUISICAO_HISTORICO.NM_USUARIO` |
| `idInsured` | Condicional (somente se informado na requisição) | Identificador do segurado relacionado ao histórico. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_SEGURADO` |
| `historicalOrigin` | Sim | Origem do histórico (`A` ou `M`). | `PLS_REQUISICAO_HISTORICO.IE_ORIGEM_HISTORICO` |
| `historicalRequestId` | Condicional (somente se informado na requisição) | Histórico pai/relacionado. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_HISTORICO` |
| `idItem` | Condicional (somente se informado na requisição) | Identificador do item da auditoria relacionado ao histórico. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_ITEM` |
| `statusAnalysis` | Condicional (somente se informado na requisição) | Status da análise no momento do registro. | `PLS_REQUISICAO_HISTORICO.IE_STATUS_ANALISE` |
| `idGroup` | Condicional (somente se informado na requisição) | Identificador do grupo auditor relacionado ao histórico. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_GRUPO` |
| `reasonReleaseId` | Condicional (somente se informado na requisição) | Motivo de liberação relacionado ao histórico. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_MOTIVO_LIB` |
| `executionId` | Condicional (somente se informado na requisição) | Identificador da execução relacionada ao histórico. | `PLS_REQUISICAO_HISTORICO.NR_SEQ_EXECUCAO` |
| `auditorFinalizes` | Condicional (somente se informado na requisição) | Indica se o auditor finaliza a análise neste evento. | `PLS_REQUISICAO_HISTORICO.IE_AUDITOR_FINALIZA` |
| `timezone` | Condicional (somente se informado na requisição) | Fuso horário de referência do evento. | `PLS_REQUISICAO_HISTORICO.DS_TIMEZONE` |

## 6.5 – Regras de negócio e validações

1. `requestId`, `historicalType`, `historical`, `historicalDate`, `userName` e `historicalOrigin` são sempre obrigatórios.
2. `historicalType` aceita apenas os valores `AM`, `AP`, `J`, `L`, `M`, `R`, `RGA` ou `SGA`.
3. `historicalOrigin` aceita apenas os valores `A` (Auditor) ou `M` (Médico/Manual).
4. `requestId` deve corresponder a uma requisição existente; caso contrário, a criação falha.
5. Quando informados, `historicalRequestId`, `reasonReleaseId` e `executionId` também devem corresponder a registros existentes; caso contrário, a criação falha.
6. Em caso de sucesso, o histórico é criado e a resposta é retornada com status `201 (Created)`.

## 6.6 – Respostas de erro

| HTTP Status | Código | Situação |
|---|---|---|
| `400` | `REQUIRED_FIELD` | Requisição inválida (campo obrigatório ausente, ou valor inválido para `historicalType`/`historicalOrigin`). |
| `404` | `RESOURCE_NOT_FOUND` | Atributo referenciado não encontrado (`requestId`, `historicalRequestId`, `reasonReleaseId` ou `executionId`). |
| `415` | `INVALID_FORMAT` | Content-Type não suportado (somente `application/json`). |
| `500` | `DATABASE_ERROR` | Erro ao persistir o histórico no banco de dados. |
| `500` | `INTERNAL_ERROR` | Erro interno inesperado. |

### Exemplo de erro (400)

```json
{
  "status": 400,
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v2/authorization-analysis-historical-requests",
  "errors": [
    { "code": "REQUIRED_FIELD", "message": "The field requestId is mandatory." }
  ]
}
```

### Exemplo de erro (404)

```json
{
  "status": 404,
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v2/authorization-analysis-historical-requests",
  "errors": [
    { "code": "RESOURCE_NOT_FOUND", "message": "requestId not found for Id: 999999" }
  ]
}
```

## 6.7 – Observações adicionais

- Este endpoint é a contrapartida, no fluxo **Inpart → Tasy**, do envio de histórico feito pelo Tasy à Inpart (ponto 7 – Histórico TASY, sentido Tasy → Inpart).
- O histórico é sempre criado como um novo registro; não há operação de atualização ou exclusão de histórico neste endpoint.
