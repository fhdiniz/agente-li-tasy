# Documentação Técnica – Integração de Pessoa Física no Tasy

## Visão Geral

Este documento descreve os eventos, triggers e artefatos envolvidos no processo de integração de dados de Pessoa Física e seus complementos no sistema Tasy com sistemas externos, através do BFT `Tecsalud-send_Receive_Natural_Person_Data_And_Complement.bft`.

---

## Acionamento de Triggers

O acionamento dos casos de uso ocorre a partir do **cadastro de pessoa física** e de seus complementos no sistema **Tasy**, o que automaticamente dispara as seguintes triggers:

### Trigger: `pessoa_fisica_insert_hl7.trg`
- **Evento Gerado:** `patient.create`
- **Descrição:** Acionada na criação de uma nova pessoa física.

### Trigger: `compl_pessoa_fisica_update_hl7.trg`
- **Evento Gerado:** `patient.registration.update`
- **Descrição:** Acionada em qualquer atualização dos dados complementares da pessoa física.

### Trigger: `pessoa_fisica_update_hl7.trg`
- **Evento Gerado:** `patient.address.update`
- **Descrição:** Acionada na criação ou atualização de endereço (tabela `COMPL_PESSOA_FISICA`).

### Trigger: `pf_codigo_externo_send_tie.trg`
- **Evento Gerado:** `api.pf_codigo_externo.send`
- **Descrição:** Acionada a partir de qualquer operação (inserção, atualização ou exclusão) na tabela `PF_CODIGO_EXTERNO`. Responsável por enviar as alterações referentes ao campo **Código de Deudor** (`CD_SISTEMA_SAP`), garantindo a sincronização com sistemas externos.

---

## Artefatos do BFT `Tecsalud-send_Receive_Natural_Person_Data_And_Complement.bft`

| Tipo        | Nome                                     | Caso de Uso         |
|-------------|------------------------------------------|----------------------|
| **Connector** | API Natural Person (REST)                | Caso de uso 05       |
| **Event**     | `api.natural-person.request`            | Caso de uso 05       |
| **Flow**      | Tasy REST API Natural Person             | Caso de uso 05       |
| **Route**     | API Natural Person (REST)                | Caso de uso 05       |
| **Token Credential** | `natural-person`                  | Caso de uso 05       |
| **Event**     | `patient.address.update`                | Casos de uso 03 e 04 |
| **Event**     | `patient.create`                        | Caso de uso 01       |
| **Event**     | `patient.registration.update`           | Caso de uso 02       |
| **Route**     | TecSalud.send.create.person.route       | Caso de uso 01       |
| **Flow**      | TecSalud.patientAndAddress.create.update| Caso de uso 03       |
| **Route**     | TecSalud.send.update.person.route       | Caso de uso 02       |
| **Route**     | TecSalud.patient.address.update         | Caso de uso 03       |
| **Event**     | `api.pf_codigo_externo.send`            | Casos de uso 01 e 02 |
| **Flow**      | TecSalud.PFcodigoexterno.create.update.delete | Casos de uso 01 e 02 |
| **Route**     | TecSalud.api.pf_codigo_externo.send.route | Casos de uso 01 e 02 |
| **Integration** | send_Receive_Natural_Person_Data_And_Complement | * |

---

## Observações

- Os eventos são enviados de forma assíncrona através da infraestrutura de integração do Tasy.
- A integração garante que todas as alterações relevantes de cadastro e complementos de pessoa física sejam refletidas em sistemas externos conforme o mapeamento de cada caso de uso.
