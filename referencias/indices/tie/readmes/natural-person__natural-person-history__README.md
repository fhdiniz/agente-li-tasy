
# 📄 Documentação - Inserção de Histórico em Cadastro de Pessoa Física

## 🧾 Visão Geral

Os históricos são salvos na tabela: PESSOA_FISICA_HISTORICO

Este documento descreve como inserir um histórico no cadastro de pessoa física utilizando dois métodos disponíveis:
 
- **API REST (JSON - POST)**
- **MLLP/HL7 (via HL7)**

---

## 🔗 API REST: `API Create History Natural Person - JSON`

### 📌 Endpoints

- **Tasy Interfaces:** `/api/natural-person/history/create`
- **TIE (EndPoint externo):** `http://{HOST}:{PORT}/api/history/create`

### 📤 Método: `POST`

### 📦 Exemplo de Payload JSON

```json
{
  "naturalPersonCode": "835186",              // NR_SEQUENCIA
  "historyDescription": "API - POSTMAN",      // DS_HISTORICO
  "releaseDate": "2025-02-25",                // DT_LIBERACAO
  "historyTypeSequence": 3,                   // NR_SEQ_TIPO_HIST
  "startDate": "2025-02-24",                  // DT_INICIAL
  "endDate": "2025-02-24",                    // DT_FINAL
  "cancellationDate": "2025-02-24",           // DT_CANCELAMENTO
  "cancellationObservation": "Cancelamento",  // DS_OBS_CANCELAMENTO
  "establishmentCode": 1                      // CD_ESTABELECIMENTO
}
```

---

## ⚙️ Artefatos Criados no BFT `API Create History Natural Person - JSON`

| Artefato       | Nome                         |
|----------------|------------------------------|
| **Connector**  | `api.natural.person.history` |
| **Event**      | `natural.person.history`     |
| **Flow**       | `api.natural.person.history` |
| **Route**      | `api.natural.person.history` |
| **Integration**| `API Create History Natural Person - JSON` |

---

## 🔄 Integração via MLLP/HL7

Também é possível realizar a criação do histórico utilizando o protocolo MLLP com mensagens HL7. Esta opção é indicada quando o ambiente já utiliza integrações no padrão HL7.

> ⚠️ Para mais detalhes sobre o modelo HL7 e estrutura da mensagem, consulte a documentação técnica específica do Tasy ou da equipe de integração.

### 📦 Artefatos da Integração via HL7

| Artefato       | Nome                                      |
|----------------|-------------------------------------------|
| **Flow**       | `natural.person.history`                  |
| **Route**      | `natural.person.history`                  |
| **JSON to JSON**   | `NATURAL-PERSON-HISTORY-v2.4_VALIDATE`|
| **Connector**      | `natural.person.history`              |
| **Integration**    | `Natural Person - History`            |

---

