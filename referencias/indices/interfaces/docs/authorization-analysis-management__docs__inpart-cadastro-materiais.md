# 2 - Cadastro de Materiais - Inpart ⇄ Tasy

> **Sequência de entrega/manual:** 2
> **Direção do fluxo:** bidirecional (Inpart consulta, Tasy responde)
> **Módulo:** `authorization-analysis-management` (V2)

## 2.1 – Finalidade

Este endpoint permite à Inpart consultar, de forma paginada, o cadastro de materiais OPME do Tasy, filtrando por registro ANVISA e/ou código do fabricante (part number), incluindo os prestadores/fornecedores vinculados a cada material.

## 2.2 – Endpoint

| | |
|---|---|
| **Método** | `GET` |
| **Path** | `/api/v2/authorization-analysis-materials` |
| **Content-Type** | `application/json` |

### Parâmetro de query

| Parâmetro | Tipo | Obrigatório | Descrição | Referência no banco |
|---|---|---|---|---|
| `anvisaRegistrationNumber` | `String` | Sim | Número de registro ANVISA do material (até 60 caracteres). | `PLS_MATERIAL.NR_REGISTRO_ANVISA` |
| `partNumber` | `String` | Sim | Código do fabricante do produto (até 80 caracteres). | `MATERIAL.CD_FABRICANTE` |
| `page` | `Integer` | Não (padrão: `1`) | Página atual do resultado paginado (inicia em 1). | — |
| `size` | `Integer` | Não (padrão: `50`, máximo: `500`) | Quantidade máxima de registros por página. | — |

## 2.3 – Exemplo de Request

```
GET /api/v2/authorization-analysis-materials?anvisaRegistrationNumber=80291810008&partNumber=EXT-12345&page=1&size=50
```

Este endpoint não possui corpo de requisição (`GET`); os filtros são enviados via parâmetros de query, conforme tabela do item 2.2.

## 2.4 – Exemplo de Response

```json
{
  "content": [
    {
      "materialId": "12345",
      "materialOpsCode": "79969801",
      "materialCode": 44414,
      "material": "Hip prosthesis",
      "inclusionDate": "2024-01-15T10:30:00Z",
      "anvisaRegistrationNumber": "80291810008",
      "partNumber": "EXT-12345",
      "materialStructure": "OPSM - Orthosis - Orthopedics",
      "providers": [
        {
          "providerCode": 321,
          "providerName": "Example Supplier"
        }
      ]
    }
  ],
  "page": 1,
  "size": 50,
  "total": 1,
  "totalPages": 1
}
```

> Quando a busca é executada com sucesso e não há resultados, a resposta é **HTTP 204 (No Content)**, sem corpo.

### 2.4.1 – Campos da resposta (raiz)

| Propriedade | Sempre presente | Descrição | Origem da informação |
|---|---|---|---|
| `content` | Sim | Lista de materiais retornados para a página atual. | — |
| `page` | Sim | Número da página atual (inicia em 1). | — |
| `size` | Sim | Quantidade de registros por página. | — |
| `total` | Sim | Total de registros encontrados em todas as páginas. | — |
| `totalPages` | Sim | Total de páginas disponíveis. | — |

### 2.4.2 – Campos da resposta (cada item de `content`)

| Propriedade | Sempre presente | Descrição | Origem da informação |
|---|---|---|---|
| `materialId` | Sim | Identificador único do material. | `PLS_MATERIAL.NR_SEQUENCIA` |
| `materialOpsCode` | Sim | Código do material OPS. | `PLS_MATERIAL.CD_MATERIAL_OPS` |
| `materialCode` | Sim | Código do material. | `PLS_MATERIAL.CD_MATERIAL` |
| `material` | Sim | Descrição do material. | `PLS_MATERIAL.DS_MATERIAL` |
| `inclusionDate` | Sim | Data de início de utilização do material. | `PLS_MATERIAL.DT_INCLUSAO` |
| `anvisaRegistrationNumber` | Sim | Número de registro ANVISA do material. | `PLS_MATERIAL.NR_REGISTRO_ANVISA` |
| `partNumber` | Sim | Código do fabricante do produto. | `MATERIAL.CD_FABRICANTE` |
| `materialStructure` | Condicional (depende do cadastro do material) | Descrição da estrutura de materiais à qual o material pertence. | `PLS_ESTRUTURA_MATERIAL.DS_ESTRUTURA` |
| `providers` | Condicional (lista vazia quando não há prestadores vinculados) | Lista de prestadores/fornecedores vinculados ao material. | `PLS_PRESTADOR_MAT.NR_SEQ_PRESTADOR` |

#### Campos de cada item de `providers`

| Propriedade | Sempre presente | Descrição | Origem da informação |
|---|---|---|---|
| `providerCode` | Sim | Código do prestador/fornecedor do material. | `PLS_PRESTADOR_MAT.NR_SEQ_PRESTADOR` |
| `providerName` | Sim | Nome do prestador/fornecedor do material. | `PESSOA_JURIDICA.NM_FANTASIA` |

## 2.5 – Regras de negócio e validações

1. `anvisaRegistrationNumber` e `partNumber` são sempre obrigatórios — a busca não pode ser feita sem ambos os filtros.
2. `size` não pode exceder 500 registros por página.
3. Quando a busca é executada com sucesso mas não retorna resultados, a resposta é `204 (No Content)`.
4. Quando há resultados, cada material retornado inclui a lista de prestadores/fornecedores vinculados (lista vazia quando não há nenhum).

## 2.6 – Respostas de erro

| HTTP Status | Código | Situação |
|---|---|---|
| `400` | `REQUIRED_FIELD` | `anvisaRegistrationNumber` ou `partNumber` não informados. |
| `400` | `INVALID_PAGINATION` | Parâmetros de paginação inválidos (ex.: `size` maior que 500). |
| `500` | `INTERNAL_ERROR` | Erro interno inesperado. |

### Exemplo de erro (400 – campo obrigatório)

```json
{
  "status": 400,
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v2/authorization-analysis-materials",
  "errors": [
    { "code": "REQUIRED_FIELD", "message": "anvisaRegistrationNumber: must be provided" }
  ]
}
```

### Exemplo de erro (400 – paginação inválida)

```json
{
  "status": 400,
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v2/authorization-analysis-materials",
  "errors": [
    { "code": "INVALID_PAGINATION", "message": "Invalid size parameter: size must not exceed 500" }
  ]
}
```

## 2.7 – Observações adicionais

- Este é o único ponto da lista com fluxo **bidirecional**: a Inpart realiza a consulta (requisição) e o Tasy responde com os dados do cadastro de materiais (resposta), sem necessidade de um endpoint de envio separado em cada sentido.
- Não há paginação por cursor — a paginação é feita por número de página (`page`) e tamanho (`size`), com o total de registros e de páginas informado na resposta.
