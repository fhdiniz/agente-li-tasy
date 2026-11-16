                                      Manual de Integração        HISS EMR
                                                                  Código documento: ########
                                MANUAL DE INTEGRAÇÃO              Revisão: ###
                                                                  Status: ###
                                  TASY – DISCHARGE
                                     SUMMARY




         MANUAL DE INTEGRAÇÃO TASY – DISCHARGE SUMMARY




                                              AVISO

O conteúdo deste documento é de propriedade exclusiva da Philips e está sujeito a alterações
sem aviso prévio.


Esta cópia deverá ser protegida contra divulgações indevidas, como cópia da documentação
eletrônica, impressa ou parte dela, não deverá ser emprestada, reproduzida ou vendida.


Todos os nomes de empresas, produtos, marcas comerciais, pessoas, personagens, dados
ou situações, citados neste documento são fictícios e tem somente objetivo didático.



 Confidencial da Companhia Philips                                               Página 1 de 12
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                                 Manual de Integração                       HISS EMR
                                                                                            Código documento: ########
                                     MANUAL DE INTEGRAÇÃO                                   Revisão: ###
                                                                                            Status: ###
                                       TASY – DISCHARGE
                                          SUMMARY


                                                         Sumário

1 OBJETIVO DA INTERFACE .............................................................................................. 3
2 REQUISITOS DA INTERFACE.......................................................................................... 3
3 CONFIGURAÇÕES ........................................................................................................... 3
  3.1 Configurações - TIE ...................................................................................................... 3
  3.2 Verificando o status do Tasy-interfaces: ....................................................................... 5
5 REQUISIÇÕES .................................................................................................................. 6
  5.1 Discharge Plan (Plano de Alta) ..................................................................................... 6
  5.2 Discharge Orders (Pedidos de Alta) ............................................................................. 7
  5.3 Discharge Prescriptions (Prescrições de Alta) .............................................................. 8
  5.4 Discharge Recommendations (Recomendações de Alta) ............................................10
6. INFORMAÇÕES RELEVANTES..................................................................................... 12




  Confidencial da Companhia Philips                                                                             Página 2 de 12
                                               CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração             HISS EMR
                                                                       Código documento: ########
                                MANUAL DE INTEGRAÇÃO                   Revisão: ###
                                                                       Status: ###
                                  TASY – DISCHARGE
                                     SUMMARY


1 OBJETIVO DA INTERFACE

     Permitir que seja obtido informações do sumário de alta do paciente, que estão localizados na
função ‘PEP – Prontuário Eletrônico do Paciente’.

2 REQUISITOS DA INTERFACE

       Para que a integração funcione corretamente, é necessário que as seguintes aplicações estejam
       instaladas:
   •    Tasy Interfaces
   •    Tasy Interface Engine (TIE)


3 CONFIGURAÇÕES

       Abaixo estão descritas as configurações e parametrizações necessárias a nível de sistema para
o funcionamento da integração.


       3.1 Configurações - TIE

     Primeiramente, é necessário realizar a importação do arquivo philips-tie-Discharge Summary -
[Medical Records].bft

Esse arquivo é responsável por disponibilizar todos os artefatos necessários para o correto
funcionamento da integração.

                                       Connectors
 DischargeSummary API [Medical Record Data] Responsável por chamar o flow
                                            api.dischargesummary

                                          Flow’s & Route:
 api.dischargesummary                              Contém a chamada dos endpoints:
                                                   discharge/plan; discharge/orders;
                                                   discharge/prescription




 Confidencial da Companhia Philips                                                    Página 3 de 12
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração            HISS EMR
                                                                      Código documento: ########
                                MANUAL DE INTEGRAÇÃO                  Revisão: ###
                                                                      Status: ###
                                  TASY – DISCHARGE
                                     SUMMARY




No item “CONNECTOR” para o artefato “DischargeSummary API [Medical Record Data]” é necessário
configura conforme ilustro abaixo:
   •   Port: Informar a porta que será disponibilizada na rede para uso da integração.
   OBS: Os conectores não podem possuir a mesma porta.
   •   Protocol: http / https
   •   Host: 0.0.0.0




 Confidencial da Companhia Philips                                                   Página 4 de 12
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração          HISS EMR
                                                                    Código documento: ########
                                MANUAL DE INTEGRAÇÃO                Revisão: ###
                                                                    Status: ###
                                  TASY – DISCHARGE
                                     SUMMARY

No item “FLOW” para o artefato “api.dischargesummary” é necessário informar o IP & Porta do
endereço do Tasy-interfaces.




  3.2 Verificando o status do Tasy-interfaces:




 Confidencial da Companhia Philips                                                 Página 5 de 12
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração          HISS EMR
                                                                    Código documento: ########
                                MANUAL DE INTEGRAÇÃO                Revisão: ###
                                                                    Status: ###
                                  TASY – DISCHARGE
                                     SUMMARY


5 REQUISIÇÕES
     5.1 Discharge Plan (Plano de Alta)

Endpoint
GET /api/encounterInformation/{encounterId}/discharge/plan

Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/encounterInformation/989997/discharge/plan

Método: GET
Content-Type: application/json

Parâmetros
- `{encounterId}` (Path) - **Obrigatório**: ID do atendimento (NR_ATENDIMENTO)

SQL Utilizado

SELECT asar.*
FROM ATEND_SUMARIO_ALTA_RESUMO asar
WHERE asar.NR_SEQ_ATEND_SUMARIO IN (
  SELECT asa.NR_SEQUENCIA
  FROM ATEND_SUMARIO_ALTA asa
  WHERE asa.NR_ATENDIMENTO = :encounterId
  AND asa.IE_SITUACAO = 'A'
  AND asa.DT_LIBERACAO IS NOT NULL
)
AND asar.DS_RESUMO IS NOT NULL

Mapeamento de Campos (Banco → JSON)
{
  "clinicalSummaryId": "NR_SEQUENCIA",
  "dischargeSummaryId": "NR_SEQ_ATEND_SUMARIO",
  "clinicalSummary": "DS_RESUMO"
}




 Confidencial da Companhia Philips                                                 Página 6 de 12
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração          HISS EMR
                                                                    Código documento: ########
                                MANUAL DE INTEGRAÇÃO                Revisão: ###
                                                                    Status: ###
                                  TASY – DISCHARGE
                                     SUMMARY


     5.2 Discharge Orders (Pedidos de Alta)

Endpoint
GET /api/encounterInformation/{encounterId}/discharge/orders

Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/encounterInformation/989997/discharge/orders

Método: GET
Content-Type: application/json

Parâmetros

- `{encounterId}` (Path) - **Obrigatório**: ID do atendimento (NR_ATENDIMENTO)

SQL Utilizado

SELECT asai.*
FROM ATEND_SUMARIO_ALTA_ITEM asai,
ATEND_SUMARIO_ALTA asa
WHERE asa.NR_SEQUENCIA = asai.NR_SEQ_ATEND_SUMARIO
AND asai.IE_TIPO_ITEM = 'C'
AND asa.IE_SITUACAO = 'A'
AND asa.DT_LIBERACAO IS NOT NULL
AND asa.NR_ATENDIMENTO = :encounterId

Mapeamento de Campos (Banco → JSON)
{
  "id": "NR_SEQUENCIA",
  "items": "ds_auxiliar",
  "itemType": "ie_tipo_item",
  "dischargeSummaryId": "NR_SEQ_ATEND_SUMARIO",
  "updateDate": "dt_atualizacao"
}




 Confidencial da Companhia Philips                                                 Página 7 de 12
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração            HISS EMR
                                                                      Código documento: ########
                                MANUAL DE INTEGRAÇÃO                  Revisão: ###
                                                                      Status: ###
                                  TASY – DISCHARGE
                                     SUMMARY


     5.3 Discharge Prescriptions (Prescrições de Alta)

Endpoint

GET /api/encounterInformation/{encounterId}/discharge/prescriptions

Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/encounterInformation/989997/discharge/prescriptions

Método: GET
Content-Type: application/json

Parâmetros
- `{encounterId}` (Path) - **Obrigatório**: ID do atendimento (NR_ATENDIMENTO)

SQL Utilizado
1. Procedimentos de Alta
SELECT
   a.cd_procedimento procedureCode,
   a.nr_proc_interno internalProcedureCode,
   substr(obter_desc_prescr_proc(b.cd_procedimento, b.ie_origem_proced,
a.nr_proc_interno),1,255) description,
   a.NR_SEQ_ATEND_SUMARIO dischargesummaryid
FROM atend_sumario_alta_item a,
procedimento b,
atend_sumario_alta c
WHERE a.cd_procedimento = b.cd_procedimento
AND a.ie_origem_proced = b.ie_origem_proced
AND a.nr_seq_atend_sumario = c.nr_sequencia
AND c.nr_atendimento = :encounterId
AND a.ie_tipo_item = 'P'
ORDER BY dischargesummaryid;

2. Exames de Alta

SELECT b.NM_EXAME labTestName, c.nr_sequencia dischargesummaryid
FROM ATEND_SUMARIO_ALTA_ITEM a,
EXAME_LABORATORIO b,
ATEND_SUMARIO_ALTA c
WHERE a.NR_SEQ_EXAME = b.NR_SEQ_EXAME
AND a.NR_SEQ_ATEND_SUMARIO = c.NR_SEQUENCIA
AND c.NR_ATENDIMENTO = :encounterId
AND a.ie_tipo_item = 'E'



 Confidencial da Companhia Philips                                                   Página 8 de 12
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração        HISS EMR
                                                                  Código documento: ########
                                MANUAL DE INTEGRAÇÃO              Revisão: ###
                                                                  Status: ###
                                  TASY – DISCHARGE
                                     SUMMARY

UNION
SELECT substr(Obter_Desc_Procedimento(cd_procedimento, ie_origem_proced),1,255)
examName,
a.NR_SEQ_ATEND_SUMARIO dischargesummaryid
FROM ATEND_SUMARIO_ALTA_ITEM a,
ATEND_SUMARIO_ALTA c
WHERE a.nr_seq_Exame is null
AND a.NR_SEQ_ATEND_SUMARIO = c.NR_SEQUENCIA
AND c.NR_ATENDIMENTO = :encounterId
AND a.ie_tipo_item = 'E'
ORDER BY dischargesummaryid;

3. Cirurgias de Alta
SELECT
    substr(obter_exame_agenda(b.cd_procedimento_princ, b.ie_origem_proced,
b.nr_seq_proc_interno),1,255) descriptionSurgery,
    a.NR_SEQ_ATEND_SUMARIO dischargesummaryid
FROM atend_sumario_alta_item a,
cirurgia b,
atend_sumario_alta c
WHERE a.nr_cirurgia = b.nr_cirurgia
AND a.nr_seq_atend_sumario = c.nr_sequencia
AND c.nr_atendimento = :encounterId
AND a.ie_tipo_item = 'I'
ORDER BY dischargesummaryid;
```

Observação: São executadas 3 consultas separadas. Os resultados são consolidados no JSON de
resposta final.




 Confidencial da Companhia Philips                                               Página 9 de 12
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração         HISS EMR
                                                                   Código documento: ########
                                 MANUAL DE INTEGRAÇÃO              Revisão: ###
                                                                   Status: ###
                                   TASY – DISCHARGE
                                      SUMMARY

Mapeamento de Campos (Banco → JSON)
{
  "procedures": {
     "procedureCode": "cd_procedimento",
     "internalProcedureCode": "nr_proc_interno",
     "description": "obter_desc_prescr_proc()",
     "dischargeSummaryId": "NR_SEQ_ATEND_SUMARIO"
  },
  "labTests": {
     "labTestName": "NM_EXAME ou Obter_Desc_Procedimento()",
     "dischargeSummaryId": "nr_sequencia"
  },
  "surgeries": {
     "descriptionSurgery": "obter_exame_agenda()",
     "dischargeSummaryId": "NR_SEQ_ATEND_SUMARIO"
  }
}


      5.4 Discharge Recommendations (Recomendações de Alta)

Endpoint
GET /api/encounterInformation/{encounterId}/discharge/recommendations

Exemplo de Requisição
URL:
http://bifrostdev.whebdc.com.br:9020/api/encounterInformation/989997/discharge/recommendations

Método: GET
Content-Type: application/json

Parâmetros
- `{encounterId}` (Path) - **Obrigatório**: ID do atendimento (NR_ATENDIMENTO)




 Confidencial da Companhia Philips                                                Página 10 de 12
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                     Manual de Integração        HISS EMR
                                                                 Código documento: ########
                                MANUAL DE INTEGRAÇÃO             Revisão: ###
                                                                 Status: ###
                                  TASY – DISCHARGE
                                     SUMMARY

SQL Utilizado
SELECT ep.*, asai.*
FROM EVOLUCAO_PACIENTE ep,
ATEND_SUMARIO_ALTA_ITEM asai
WHERE ep.CD_EVOLUCAO = asai.CD_EVOLUCAO
AND asai.NR_SEQ_ATEND_SUMARIO IN (
  SELECT asa.NR_SEQUENCIA
  FROM ATEND_SUMARIO_ALTA asa
  WHERE asa.NR_ATENDIMENTO = :encounterId
  AND asa.IE_SITUACAO = 'A'
  AND asa.DT_LIBERACAO IS NOT NULL
)

Mapeamento de Campos (Banco → JSON)
{
  "clinicalNotes": {
     "clinicalNotesId": "CD_EVOLUCAO",
     "evolutionDate": "DT_EVOLUCAO",
     "evolutionText": "DS_EVOLUCAO",
     "physicianCode": "CD_MEDICO",
     "evolutionType": "IE_EVOLUCAO_CLINICA",
     "status": "IE_SITUACAO"
  },
  "orders": {
     "id": "NR_SEQUENCIA",
     "items": "DS_AUXILIAR",
     "itemType": "IE_TIPO_ITEM",
     "dischargeSummaryId": "NR_SEQ_ATEND_SUMARIO",
     "updateDate": "DT_ATUALIZACAO"
  }
}




Confidencial da Companhia Philips                                               Página 11 de 12
                                    CÓPIAS NÃO SÃO CONTROLADAS
                                       Manual de Integração        HISS EMR
                                                                   Código documento: ########
                                 MANUAL DE INTEGRAÇÃO              Revisão: ###
                                                                   Status: ###
                                   TASY – DISCHARGE
                                      SUMMARY


6. INFORMAÇÕES RELEVANTES

Headers Obrigatórios
- `Content-Type: application/json`
- `Accept: application/json`

Códigos de Resposta HTTP
- **200**: Sucesso - Dados encontrados
- **400**: Bad Request - Parâmetros inválidos
- **404**: Not Found - Dados não encontrados
- **500**: Internal Server Error - Erro interno do servidor




 Confidencial da Companhia Philips                                                Página 12 de 12
                                      CÓPIAS NÃO SÃO CONTROLADAS
