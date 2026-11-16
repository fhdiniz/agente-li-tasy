# Bionexo360 Outbound

Documentação técnica do serviço **Outbound** do projeto Bionexo360 no `tasy-interfaces`.

> **Escopo analisado:** arquivos presentes em `outbound/` e componentes compartilhados em `common/`. O ZIP analisado não contém `pom.xml`, arquivo de propriedades, configuração do servidor, rotas Camel/TIE, workers, filas ou código de autenticação/autorização. Quando alguma informação não aparece no código, ela é descrita como **não identificada no código analisado**.

## 1. Visão geral do serviço Outbound

O serviço Outbound possui dois fluxos técnicos principais:

1. **Callback de montagem do payload outbound**, usado para montar o corpo de envio a partir de um `nrSeqEvento` e/ou de um documento recebido como string JSON.
2. **Receive de retorno outbound**, usado para receber o resultado do envio externo, persistir resposta/consistência no Oracle e acionar o processamento final da resposta no banco.

A regra final de negócio não está concentrada no Java. O Java faz validação técnica, persistência de retorno e chamada de rotinas Oracle, principalmente da package `INTB_PCK`.

## 2. Objetivo do serviço

O objetivo do Outbound é viabilizar o envio de documentos/eventos do TASY para a Bionexo360 e tratar posteriormente o retorno desse envio.

Pelo código analisado, o outbound:

- busca o payload de um evento no banco quando recebe `nrSeqEvento`;
- permite complementar/mesclar o payload com o campo `document` recebido no callback;
- expõe um endpoint de disponibilidade (`ping`) para o receive;
- recebe retorno técnico/de negócio do envio;
- atualiza `INTB_DOCUMENTO_JSON` com `JSON_RESPONSE`, `IE_STATUS_HTTP` e `IE_TIPO_JSON = 'RT'`;
- registra consistências em `INTB_EVENTO_CONSISTENCIA`, quando informadas;
- executa `INTB_PCK.processar_response` ao final do receive.

## 3. Responsabilidades principais

| Responsabilidade | Componente |
|---|---|
| Expor endpoint de callback outbound | `Bionexo360OutboundCallbackResource` |
| Validar argumentos do callback | `Bionexo360OutboundCallback` |
| Buscar payload de evento no Oracle | `Bionexo360OutboundCallbackService.getJsonPayload` |
| Converter JSON de CLOB/string para `Map` | `Bionexo360OutboundCallbackService.parseJson` |
| Montar o body final do callback | `Bionexo360OutboundCallbackService.buildOutboundRequest` |
| Expor endpoint de disponibilidade do receive | `Bionexo360OutboundReceive.ping` |
| Receber retorno outbound | `Bionexo360OutboundReceive.receive` |
| Validar retorno outbound | `Bionexo360OutboundReceiveService.validate` |
| Atualizar resposta em `INTB_DOCUMENTO_JSON` | `Bionexo360OutboundRepository.updateResponse` |
| Inserir consistência em `INTB_EVENTO_CONSISTENCIA` | `Bionexo360OutboundRepository.insertConsistency` |
| Executar processamento final da resposta | `Bionexo360OutboundProcedureExecutor.processResponse` |
| Registrar histórico técnico em erro | `Bionexo360OutboundHistoryService` e `Bionexo360HistoryService` |

## 4. Como o fluxo outbound funciona

O outbound é dividido em dois subfluxos.

### 4.1 Fluxo de callback para montagem do payload

```text
TIE / mecanismo de callback / camada chamadora
    |
    | POST /bionexo360/outbound/callback/execute
    | Body: { nrSeqEvento, document? }
    v
Bionexo360OutboundCallbackResource.execute
    |
    v
Bionexo360OutboundCallback.execute
    |-- valida argumentos não nulos
    v
Bionexo360OutboundCallbackService.buildOutboundRequest
    |
    | 1) Se nrSeqEvento foi informado:
    |      chama INTB_PCK.get_evento_payload(:NR_SEQ_EVENTO_P)
    |      lê o CLOB JSON_PAYLOAD_OUT_P
    |      converte o JSON para Map
    |      adiciona os campos ao body final
    |
    | 2) Se document foi informado:
    |      interpreta document como string contendo JSON válido
    |      converte para Map
    |      adiciona/mescla os campos ao body final
    |
    | 3) Garante o campo nrSeqEvento no retorno
    v
Retorna Map<String, Object> serializado como JSON
```

Quando o mesmo campo existir no payload buscado do banco e no `document`, o `document` é aplicado depois e pode substituir o valor anterior no `Map` final. Depois disso, o `nrSeqEvento` informado no argumento é aplicado no retorno.

### 4.2 Fluxo de receive do retorno outbound

```text
TIE / Bionexo360 / camada chamadora
    |
    | POST /bionexo360/outbound/receive
    | Body: retorno técnico e/ou consistência
    v
Bionexo360OutboundReceive.receive
    |
    v
Bionexo360OutboundReceiveService.receiveOutboundReturn
    |-- valida request não nulo
    |-- valida nrSeqEvento obrigatório
    |-- exige jsonResponse ou dsConsistencia
    |-- valida cdStatusHttp obrigatório entre 100 e 599
    |
    | Se jsonResponse foi informado:
    |   UPDATE INTB_DOCUMENTO_JSON
    |      SET IE_TIPO_JSON   = 'RT',
    |          IE_STATUS_HTTP = :IE_STATUS_HTTP_P,
    |          JSON_RESPONSE  = :JSON_RESPONSE_P
    |    WHERE último registro pendente do evento:
    |      NR_SEQ_EVENTO = :NR_SEQ_EVENTO_P
    |      IE_TIPO_JSON = 'P'
    |      NR_SEQ_DOCUMENTO IS NULL
    |
    | Se houver dados de consistência:
    |   INSERT INTO INTB_EVENTO_CONSISTENCIA (...)
    |
    | Sempre ao final:
    |   INTB_PCK.processar_response(:NR_SEQ_EVENTO_P)
    v
Retorna {"status":"OK"}
```

## 5. Principais arquivos, pastas e componentes envolvidos

```text
bionexo360/
├── common/
│   ├── config/
│   │   └── Bionexo360CommonDatabaseConfig.java
│   └── service/history/
│       ├── Bionexo360HistoryContext.java
│       ├── Bionexo360HistoryMessageBuilder.java
│       └── Bionexo360HistoryService.java
└── outbound/
    ├── callback/
    │   └── Bionexo360OutboundCallback.java
    ├── config/
    │   └── Bionexo360DatabaseConfig.java
    ├── integration/
    │   ├── callback/
    │   │   └── Bionexo360OutboundCallbackResource.java
    │   └── receive/
    │       └── Bionexo360OutboundReceive.java
    ├── pojo/
    │   ├── callback/
    │   │   └── Bionexo360OutboundCallbackRequest.java
    │   └── receive/
    │       └── Bionexo360OutboundReceiveRequest.java
    ├── service/
    │   ├── callback/
    │   │   └── Bionexo360OutboundCallbackService.java
    │   ├── enums/
    │   │   └── Bionexo360OutboundServiceQuery.java
    │   └── receive/
    │       ├── Bionexo360OutboundHistoryService.java
    │       ├── Bionexo360OutboundProcedureExecutor.java
    │       ├── Bionexo360OutboundReceiveService.java
    │       └── Bionexo360OutboundRepository.java
    └── README.md
```

## 6. Endpoints disponíveis

### Base path do callback

```http
/bionexo360/outbound/callback
```

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/bionexo360/outbound/callback/execute` | Monta o payload outbound a partir do `nrSeqEvento` e/ou `document`. |

### Base path do receive

```http
/bionexo360/outbound
```

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/bionexo360/outbound/ping` | Verifica se o recurso de receive outbound está disponível. |
| `POST` | `/bionexo360/outbound/receive` | Recebe o retorno técnico/de negócio do envio outbound. |


## 7. Métodos HTTP, rotas, headers e parâmetros

### `GET /bionexo360/outbound/ping`

Endpoint simples de disponibilidade do receive outbound.

#### Resposta

```text
Bionexo360 outbound receive is available
```

#### Content-Type produzido

```http
text/plain
```

### `POST /bionexo360/outbound/callback/execute`

Monta o payload outbound.

#### Headers

| Header | Obrigatório no contrato do recurso | Observação |
|---|---:|---|
| `Content-Type: application/json` | Sim | A classe usa `@Consumes(MediaType.APPLICATION_JSON)`. |
| `Accept: application/json` | Não obrigatório pelo código | A classe usa `@Produces(MediaType.APPLICATION_JSON)`. |
| `Authorization` | Não identificado | Não há código de autenticação/autorização no pacote analisado. |

#### Body

| Campo | Tipo Java | Obrigatório pelo Java | Descrição |
|---|---|---:|---|
| `nrSeqEvento` | `Long` | Não | Quando informado, busca o payload no banco por `INTB_PCK.get_evento_payload`. |
| `document` | `String` | Não | String contendo JSON válido. Quando informada, é convertida para `Map` e mesclada ao body final. |

O objeto de argumentos não pode ser nulo. Caso venha nulo, o callback lança `IllegalArgumentException`.

### `POST /bionexo360/outbound/receive`

Recebe o retorno do envio outbound.

#### Headers

| Header | Obrigatório no contrato do recurso | Observação |
|---|---:|---|
| `Content-Type: application/json` | Sim | O método usa `@Consumes(MediaType.APPLICATION_JSON)`. |
| `Accept: application/json` | Não obrigatório pelo código | O método usa `@Produces(MediaType.APPLICATION_JSON)`. |
| `Authorization` | Não identificado | Não há código de autenticação/autorização no pacote analisado. |

#### Body

| Campo | Tipo Java | Obrigatório pelo Java | Descrição |
|---|---|---:|---|
| `nrSeqEvento` | `Long` | Sim | Sequência do evento outbound. |
| `cdStatusHttp` | `Integer` | Sim | Status HTTP retornado pelo envio. Deve estar entre `100` e `599`. |
| `jsonResponse` | `String` | Condicional | JSON de resposta. Obrigatório quando `dsConsistencia` não for informado. |
| `cdConsistencia` | `Long` | Não | Código da consistência. Se houver consistência e o campo estiver nulo, o repository usa `0`. |
| `ieTipoConsistencia` | `String` | Não | Tipo da consistência. Se houver consistência e o campo estiver vazio, o repository usa `T`. É truncado para 15 caracteres. |
| `dsConsistencia` | `String` | Condicional | Descrição da consistência. Obrigatória quando `jsonResponse` não for informado. É truncada para 4000 caracteres. |
| `dsEndpoint` | `String` | Não | Endpoint relacionado ao retorno/erro. É normalizado com `trim` e truncado para 4000 caracteres. |

## 8. Exemplos de payload de entrada

### Callback apenas com `nrSeqEvento`

```json
{
  "nrSeqEvento": 26
}
```

### Callback com `document`

No POJO analisado, `document` é uma string. Portanto, o JSON interno precisa ser enviado escapado como string JSON válida.

```json
{
  "nrSeqEvento": 26,
  "document": "{\"typeEvent\":\"MATERIAL\",\"document\":[{\"cdMaterial\":\"MAT-001\",\"dsMaterial\":\"Seringa descartável 10ml\"}]}"
}
```

### Receive com resposta JSON

```json
{
  "nrSeqEvento": 26,
  "cdStatusHttp": 200,
  "jsonResponse": "{\"success\":true,\"received\":1}"
}
```

### Receive com consistência

```json
{
  "nrSeqEvento": 26,
  "cdStatusHttp": 500,
  "cdConsistencia": 1,
  "ieTipoConsistencia": "T",
  "dsConsistencia": "Erro técnico na comunicação com Bionexo360.",
  "dsEndpoint": "http://bionexo360.com/api/document/"
}
```

### Receive com resposta e consistência na mesma chamada

O código permite atualizar `jsonResponse` e inserir consistência na mesma execução quando ambos forem informados.

```json
{
  "nrSeqEvento": 26,
  "cdStatusHttp": 400,
  "jsonResponse": "{\"success\":false}",
  "cdConsistencia": 10,
  "ieTipoConsistencia": "NEGOCIO",
  "dsConsistencia": "Retorno de negócio recusado pela integração.",
  "dsEndpoint": "http://bionexo360.com/api/document/"
}
```

## 9. Exemplos de resposta de sucesso

### `GET /bionexo360/outbound/ping`

```http
HTTP/1.1 200 OK
Content-Type: text/plain

Bionexo360 outbound receive is available
```

### `POST /bionexo360/outbound/callback/execute`

O callback retorna um `Map<String, Object>`. O formato final depende do JSON retornado por `INTB_PCK.get_evento_payload` e/ou do JSON informado em `document`.

Exemplo de comportamento quando o `document` do request contém `typeEvent` e `document`, e o `nrSeqEvento` informado é `26`:

```json
{
  "typeEvent": "MATERIAL",
  "document": [
    {
      "cdMaterial": "MAT-001",
      "dsMaterial": "Seringa descartável 10ml"
    }
  ],
  "nrSeqEvento": 26
}
```

### `POST /bionexo360/outbound/receive`

```json
{
  "status": "OK"
}
```

Resposta HTTP usada pelo recurso em sucesso:

```http
HTTP/1.1 200 OK
```

## 10. Exemplos de resposta de erro

### Erro de validação no receive

Exemplo quando `nrSeqEvento` não é informado:

```json
{
  "status": "ERROR",
  "code": "VALIDATION_ERROR",
  "message": "Tasy-Interfaces: Sequencia do Evento não informado no retorno outbound da Bionexo360."
}
```

Resposta HTTP usada pelo recurso de receive:

```http
HTTP/1.1 400 Bad Request
```

### Erro de processamento no receive

```json
{
  "status": "ERROR",
  "code": "PROCESSING_ERROR",
  "message": "Tasy-Interfaces: erro interno no processamento outbound Bionexo360."
}
```

Resposta HTTP usada pelo recurso de receive:

```http
HTTP/1.1 500 Internal Server Error
```

### Erro no callback

O callback retorna um mapa de erro quando captura exceção. O método não monta explicitamente um `Response` com status HTTP; ele retorna apenas o body.

```json
{
  "status": "ERROR",
  "code": "VALIDATION_ERROR",
  "message": "Tasy-Interfaces: Argumentos não informados para o callback Bionexo360."
}
```

Para exceções de runtime no callback:

```json
{
  "status": "ERROR",
  "code": "PROCESSING_ERROR",
  "message": "Tasy-Interfaces: erro interno ao montar callback outbound Bionexo360."
}
```

As mensagens de erro retornadas pelos recursos são sanitizadas, removendo quebras de linha, e limitadas a 500 caracteres.

## 11. Validações aplicadas

### Validação do callback

Aplicada em `Bionexo360OutboundCallback.validate`:

| Regra | Erro quando inválida |
|---|---|
| O objeto de argumentos não pode ser nulo | `Tasy-Interfaces: Argumentos não informados para o callback Bionexo360.` |

### Validação do JSON usado no callback

Aplicada em `Bionexo360OutboundCallbackService.parseJson`:

| Origem do JSON | Regra |
|---|---|
| CLOB retornado por `INTB_PCK.get_evento_payload` | Deve ser um JSON que possa ser convertido para `Map<String, Object>`. |
| Campo `document` | Deve ser uma string contendo JSON válido conversível para `Map<String, Object>`. |

Quando o parse falha, o serviço lança `RuntimeException` com a mensagem:

```text
Tasy-Interfaces: Erro ao converter json_payload da intb_documento_json para Map.
```

### Validação do receive outbound

Aplicada em `Bionexo360OutboundReceiveService.validate`:

| Regra | Erro quando inválida |
|---|---|
| Request não pode ser nulo | `Tasy-Interfaces: Retorno outbound da Bionexo360 não informado.` |
| `nrSeqEvento` é obrigatório | `Tasy-Interfaces: Sequencia do Evento não informado no retorno outbound da Bionexo360.` |
| Deve existir `jsonResponse` ou `dsConsistencia` | `Tasy-Interfaces: Json Response ou Descricao da Consistencia deve ser informado no retorno outbound da Bionexo360.` |
| `cdStatusHttp` é obrigatório | `Tasy-Interfaces: Status do HTTP não informado no retorno outbound da Bionexo360.` |
| `cdStatusHttp` deve estar entre `100` e `599` | `Tasy-Interfaces: Status do HTTP inválido no retorno outbound da Bionexo360.` |

## 12. Autenticação/autorização

Não foi identificado código de autenticação/autorização no serviço outbound analisado.

Não foram encontrados filtros, validação de token, validação de header `Authorization`, roles, permissões ou qualquer mecanismo equivalente dentro dos arquivos enviados.

## 13. Integrações com banco, fila, APIs externas ou outros serviços

### Banco Oracle

O outbound integra com Oracle por meio de `DataQuery` e chamadas SQL/PLSQL declaradas em `Bionexo360DatabaseConfig` e `Bionexo360OutboundServiceQuery`.

#### Obter payload do evento

```sql
BEGIN
    :JSON_PAYLOAD_OUT_P := INTB_PCK.get_evento_payload(:NR_SEQ_EVENTO_P);
END;
```

Usado pelo callback quando `nrSeqEvento` é informado.

#### Atualizar resposta outbound

```sql
BEGIN
    UPDATE INTB_DOCUMENTO_JSON
       SET IE_TIPO_JSON = 'RT',
           IE_STATUS_HTTP = :IE_STATUS_HTTP_P,
           JSON_RESPONSE = :JSON_RESPONSE_P
     WHERE NR_SEQUENCIA = (
           SELECT NR_SEQUENCIA
             FROM (
                   SELECT NR_SEQUENCIA
                     FROM INTB_DOCUMENTO_JSON
                    WHERE NR_SEQ_EVENTO = :NR_SEQ_EVENTO_P
                      AND IE_TIPO_JSON = 'P'
                      AND NR_SEQ_DOCUMENTO IS NULL
                    ORDER BY NR_SEQUENCIA DESC
                  )
            WHERE ROWNUM = 1
     );
END;
```

Executado quando `jsonResponse` é informado no receive.

#### Inserir consistência

```sql
BEGIN
    INSERT INTO INTB_EVENTO_CONSISTENCIA (
        NR_SEQUENCIA,
        NR_SEQ_EVENTO,
        NM_USUARIO_NREC,
        DT_ATUALIZACAO_NREC,
        CD_CONSISTENCIA,
        IE_TIPO_CONSISTENCIA,
        DS_CONSISTENCIA,
        IE_STATUS_HTTP,
        DS_ENDPOINT,
        IE_ORIGEM_CONSISTENCIA,
        DT_REGISTRO
    ) VALUES (
        INTB_EVENTO_CONSISTENCIA_SEQ.NEXTVAL,
        :NR_SEQ_EVENTO_P,
        'Bio360',
        SYSDATE,
        :CD_CONSISTENCIA_P,
        :IE_TIPO_CONSISTENCIA_P,
        :DS_CONSISTENCIA_P,
        :IE_STATUS_HTTP_P,
        :DS_ENDPOINT_P,
        'TIE',
        SYSDATE
    );
END;
```

Executado quando o receive identifica dados de consistência.

#### Processar resposta

```sql
BEGIN
    INTB_PCK.processar_response(:NR_SEQ_EVENTO_P);
END;
```

Executado sempre ao final de `receiveOutboundReturn`, após atualização de resposta e/ou inserção de consistência.

### APIs externas

Não foi identificado cliente HTTP Java que envie diretamente dados para uma API da Bionexo360 dentro do pacote outbound analisado.

O código expõe recursos REST para callback e receive. O envio efetivo para fora do Java não aparece nos arquivos enviados.

### Filas e workers

Não foram identificados workers, filas, consumidores assíncronos, producers, Kafka, JMS, RabbitMQ, SQS ou mecanismo equivalente dentro do pacote outbound analisado.

## 14. Variáveis de ambiente usadas

Não foram identificadas leituras de variáveis de ambiente no código analisado.

Também não foram identificadas chamadas a `System.getenv`, propriedades locais, arquivos `.properties`, `.yml`, `.yaml` ou configuração de porta no ZIP enviado.

## 15. Logs e rastreabilidade

Não foram identificadas chamadas explícitas de log no fluxo outbound analisado.

A rastreabilidade técnica encontrada ocorre por histórico em banco quando há exceção nas etapas de persistência ou execução da procedure de resposta:

```text
Bionexo360OutboundRepository / Bionexo360OutboundProcedureExecutor
    -> Bionexo360OutboundHistoryService
        -> Bionexo360HistoryService
            -> INTB_PCK.registrar_historico(...)
```

A procedure comum chamada para histórico é montada em `Bionexo360CommonDatabaseConfig`:

```sql
BEGIN
    INTB_PCK.registrar_historico(
        :NR_SEQ_EVENTO_P,
        :NR_SEQ_DOCUMENTO_P,
        :DS_STATUS_ANTERIOR_P,
        :DS_STATUS_NOVO_P,
        :DS_OBSERVACAO_P
    );
END;
```

No histórico técnico:

- `NR_SEQ_DOCUMENTO_P` é enviado como `NULL`;
- `DS_STATUS_ANTERIOR_P` é enviado como `NULL`;
- `DS_STATUS_NOVO_P` é enviado como `NULL`;
- `DS_OBSERVACAO_P` recebe a mensagem técnica;
- a observação é limitada a 4000 caracteres.

## 16. Possíveis status do processamento

### Status HTTP retornados pelos endpoints outbound

| Endpoint | Situação | HTTP status |
|---|---|---:|
| `GET /bionexo360/outbound/ping` | Disponibilidade | `200` |
| `POST /bionexo360/outbound/receive` | Sucesso | `200` |
| `POST /bionexo360/outbound/receive` | Validação Java falha | `400` |
| `POST /bionexo360/outbound/receive` | Exceção de runtime | `500` |
| `POST /bionexo360/outbound/callback/execute` | Sucesso | Não definido explicitamente por `Response`; retorna `Map`. |
| `POST /bionexo360/outbound/callback/execute` | Erro capturado | Não definido explicitamente por `Response`; retorna `Map` com `status=ERROR`. |

### Status/códigos persistidos em banco

| Campo/tabela | Uso identificado |
|---|---|
| `INTB_DOCUMENTO_JSON.IE_TIPO_JSON` | No receive, o registro pendente `P` é atualizado para `RT` quando há `jsonResponse`. |
| `INTB_DOCUMENTO_JSON.IE_STATUS_HTTP` | Recebe o status HTTP informado no body do receive. |
| `INTB_DOCUMENTO_JSON.JSON_RESPONSE` | Recebe o JSON de resposta informado no body do receive. |
| `INTB_EVENTO_CONSISTENCIA.IE_TIPO_CONSISTENCIA` | Recebe o tipo informado ou o padrão `T`. |
| `INTB_EVENTO_CONSISTENCIA.IE_ORIGEM_CONSISTENCIA` | Recebe o valor fixo `TIE`. |
| `INTB_EVENTO_CONSISTENCIA.NM_USUARIO_NREC` | Recebe o valor fixo `Bio360`. |

## 17. Tratamento de erros

### Callback

`Bionexo360OutboundCallbackResource.execute` trata:

| Exceção | Body retornado |
|---|---|
| `IllegalArgumentException` | `status=ERROR`, `code=VALIDATION_ERROR`, mensagem da exceção. |
| `RuntimeException` | `status=ERROR`, `code=PROCESSING_ERROR`, mensagem genérica de callback. |

### Receive

`Bionexo360OutboundReceive.receive` trata:

| Exceção | Resposta |
|---|---|
| `IllegalArgumentException` | HTTP `400`, body com `status=ERROR`, `code=VALIDATION_ERROR` e mensagem da exceção. |
| `RuntimeException` | HTTP `500`, body com `status=ERROR`, `code=PROCESSING_ERROR` e mensagem genérica. |

### Repository e procedure executor

`Bionexo360OutboundRepository` registra histórico técnico quando ocorre erro ao atualizar resposta ou inserir consistência.

`Bionexo360OutboundProcedureExecutor` registra histórico técnico quando ocorre erro ao executar `INTB_PCK.processar_response`.

Contextos usados no histórico:

| Etapa | Contexto gravado |
|---|---|
| Atualização de `json_response` | `Tasy-Interfaces: erro ao atualizar json_response na intb_documento_json` |
| Inserção de consistência | `Tasy-Interfaces: erro ao inserir consistência na intb_evento_consistencia` |
| Execução de `processar_response` | `Tasy-Interfaces: erro ao executar intb_pck.processar_response` |

## 18. Cuidados de manutenção baseados no código atual

- O campo `document` do callback é `String`, não objeto JSON; quando usado em teste, o JSON interno precisa ser escapado.
- O callback aplica primeiro o payload obtido do banco, depois o conteúdo de `document` e, por último, o `nrSeqEvento` do argumento.
- O receive exige `nrSeqEvento`, `cdStatusHttp` e pelo menos `jsonResponse` ou `dsConsistencia`.
- `jsonResponse` em branco não atualiza `INTB_DOCUMENTO_JSON`.
- Dados de consistência são identificados quando pelo menos um destes campos existe: `cdConsistencia`, `dsConsistencia` ou `ieTipoConsistencia`.
- O processamento final `INTB_PCK.processar_response` é executado ao final do receive, independentemente de ter ocorrido atualização de resposta, inserção de consistência ou ambos.
- O código não verifica explicitamente `SQL%ROWCOUNT` nos updates; a documentação descreve apenas o comportamento implementado.

## 19. Funcionalidades de teste usando `curl`

> Ajuste `BASE_URL` conforme o contexto real de publicação do serviço. O código Java mostra os paths `/bionexo360/outbound/...`, mas o servidor pode adicionar prefixos próprios, como contexto de aplicação ou `/resources`, fora do pacote analisado.

### Teste de disponibilidade do receive outbound

```bash
BASE_URL="http://localhost:<PORT>"

curl -i -X GET "$BASE_URL/bionexo360/outbound/ping"
```

Resposta esperada:

```text
Bionexo360 outbound receive is available
```

### Teste de callback apenas com `nrSeqEvento`

```bash
BASE_URL="http://localhost:<PORT>"

curl -i -X POST "$BASE_URL/bionexo360/outbound/callback/execute" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "nrSeqEvento": 26
  }'
```

### Teste de callback com `document`

```bash
BASE_URL="http://localhost:<PORT>"

curl -i -X POST "$BASE_URL/bionexo360/outbound/callback/execute" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "nrSeqEvento": 26,
    "document": "{\"typeEvent\":\"MATERIAL\",\"document\":[{\"cdMaterial\":\"MAT-001\",\"dsMaterial\":\"Seringa descartável 10ml\"}]}"
  }'
```

### Teste de receive com `jsonResponse`

```bash
BASE_URL="http://localhost:<PORT>"

curl -i -X POST "$BASE_URL/bionexo360/outbound/receive" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "nrSeqEvento": 26,
    "cdStatusHttp": 200,
    "jsonResponse": "{\"success\":true,\"received\":1}"
  }'
```

Resposta esperada pelo Java quando o processamento termina sem exceção:

```json
{
  "status": "OK"
}
```

### Teste de receive com consistência

```bash
BASE_URL="http://localhost:<PORT>"

curl -i -X POST "$BASE_URL/bionexo360/outbound/receive" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "nrSeqEvento": 26,
    "cdStatusHttp": 500,
    "cdConsistencia": 1,
    "ieTipoConsistencia": "T",
    "dsConsistencia": "Erro técnico na comunicação com Bionexo360.",
    "dsEndpoint": "http://bionexo360.com/api/document/"
  }'
```

Resposta esperada pelo Java quando o processamento termina sem exceção:

```json
{
  "status": "OK"
}
```

### Teste de receive com erro de validação: `nrSeqEvento` ausente

```bash
BASE_URL="http://localhost:<PORT>"

curl -i -X POST "$BASE_URL/bionexo360/outbound/receive" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "cdStatusHttp": 200,
    "jsonResponse": "{\"success\":true}"
  }'
```

Resposta esperada pelo Java:

```json
{
  "status": "ERROR",
  "code": "VALIDATION_ERROR",
  "message": "Tasy-Interfaces: Sequencia do Evento não informado no retorno outbound da Bionexo360."
}
```

### Teste de receive com erro de validação: status HTTP inválido

```bash
BASE_URL="http://localhost:<PORT>"

curl -i -X POST "$BASE_URL/bionexo360/outbound/receive" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "nrSeqEvento": 26,
    "cdStatusHttp": 999,
    "jsonResponse": "{\"success\":true}"
  }'
```

Resposta esperada pelo Java:

```json
{
  "status": "ERROR",
  "code": "VALIDATION_ERROR",
  "message": "Tasy-Interfaces: Status do HTTP inválido no retorno outbound da Bionexo360."
}
```

