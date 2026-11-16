                                      Manual de Integração        HISS EMR
                                                                  Código documento: ########
                                MANUAL DE INTEGRAÇÃO              Revisão: ###
                                                                  Status: ###
                                TASY – MEDICAL RECORD
                                         DATA




        MANUAL DE INTEGRAÇÃO TASY – MEDICAL RECORD DATA




                                              AVISO

O conteúdo deste documento é de propriedade exclusiva da Philips e está sujeito a alterações
sem aviso prévio.


Esta cópia deverá ser protegida contra divulgações indevidas, como cópia da documentação
eletrônica, impressa ou parte dela, não deverá ser emprestada, reproduzida ou vendida.


Todos os nomes de empresas, produtos, marcas comerciais, pessoas, personagens, dados
ou situações, citados neste documento são fictícios e tem somente objetivo didático.



 Confidencial da Companhia Philips                                               Página 1 de 26
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                                   Manual de Integração                         HISS EMR
                                                                                                Código documento: ########
                                       MANUAL DE INTEGRAÇÃO                                     Revisão: ###
                                                                                                Status: ###
                                       TASY – MEDICAL RECORD
                                                DATA


                                                           Sumário

1 OBJETIVO DA INTERFACE .............................................................................................. 3
2 REQUISITOS DA INTERFACE.......................................................................................... 3
3 CONFIGURAÇÕES ........................................................................................................... 3
  3.1 Configurações - TIE ...................................................................................................... 3
  3.2 Verificando o status do Tasy-interfaces: ....................................................................... 6
5 REQUISIÇÕES .................................................................................................................. 7
  5.1 Clinical Notes – Notas Clínicas ..................................................................................... 7
  5.2 Patient Care (Atendimentos do Paciente) ..................................................................... 8
  5.3 Health History (Histórico de Saúde) .............................................................................. 9
     5.3.1 Allergies .................................................................................................................. 9
     5.3.2 Current Medications (Medicações Atuais)..............................................................12
     5.3.3 Past History (Histórico Clínico) ..............................................................................14
     5.3.4 Social History (Histórico Social) .............................................................................16
     5.3.5 Surgical History (Histórico Cirúrgico) .....................................................................18
  5.4 Laboratory Tests (Exames Laboratoriais) ....................................................................20
  5.5 Non-Laboratory Tests (Exames de Imagem/Diagnósticos) ..........................................23
  5.6 Emergency Discharge (Alta de Emergência) ...............................................................24
6. INFORMAÇOES RELEVANTES..................................................................................... 26
  6.1 Headers Obrigatórios ...................................................................................................26
  6.2 Códigos de Resposta HTTP ........................................................................................26
  6.3 Campos Comuns (Mapeamento Padrão).....................................................................26




  Confidencial da Companhia Philips                                                                                  Página 2 de 26
                                                CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração             HISS EMR
                                                                       Código documento: ########
                                MANUAL DE INTEGRAÇÃO                   Revisão: ###
                                                                       Status: ###
                                TASY – MEDICAL RECORD
                                         DATA


1 OBJETIVO DA INTERFACE

      Permitir que seja obtido histórico de saúde, notas clínicas, exames laboratoriais, exames não
laboratoriais e alta de emergência do paciente, que estão localizados na função ‘PEP – Prontuário
Eletrônico do Paciente’.


2 REQUISITOS DA INTERFACE

       Para que a integração funcione corretamente, é necessário que as seguintes aplicações estejam
       instaladas:
   •    Tasy Interfaces
   •    Tasy Interface Engine (TIE)


3 CONFIGURAÇÕES

       Abaixo estão descritas as configurações e parametrizações necessárias a nível de sistema para
o funcionamento da integração.


       3.1 Configurações - TIE

     Primeiramente, é necessário realizar a importação do arquivo philips-tie-Patient Information -
Medical Records.bft

Esse arquivo é responsável por disponibilizar todos os artefatos necessários para o correto
funcionamento da integração.

                                           Connectors
 Encounter Information API [Medical Records]    Contém todas as chamadas
                                                /api/encounterInformation
 Patient Health History API [Medical Records]   Contém todas as chamadas /api/health-history

                                          Flow’s & Route:
 encounter.information.request                     Contém os endpoints de
                                                   /api/encounterInformation
 medical.record.data.request                       Contém todos os endpoints de api/health-
                                                   history




 Confidencial da Companhia Philips                                                    Página 3 de 26
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                        Manual de Integração            HISS EMR
                                                                        Código documento: ########
                                MANUAL DE INTEGRAÇÃO                    Revisão: ###
                                                                        Status: ###
                                TASY – MEDICAL RECORD
                                         DATA




No item “CONNECTOR” para os artefatos “Encounter Information API [Medical Records]” & “Patient
Health History API [Medical Records]” é necessário configura conforme ilustro abaixo:
   •   Port: Informar a porta que será disponibilizada na rede para uso da integração.
   OBS: Os conectores não podem possuir a mesma porta.
   •   Protocol: http / https
   •   Host:                                                                                    0.0.0.0


                                 Encounter Information API [Medical Records]




 Confidencial da Companhia Philips                                                      Página 4 de 26
                                       CÓPIAS NÃO SÃO CONTROLADAS
                                        Manual de Integração             HISS EMR
                                                                         Código documento: ########
                                MANUAL DE INTEGRAÇÃO                     Revisão: ###
                                                                         Status: ###
                                TASY – MEDICAL RECORD
                                         DATA

                               Patient Health History API [Medical Records]




No item “FLOW” para os artefatos “encounter.information.request” & “medical.record.data.request” é
necessário informar o IP & Porta do endereço do Tasy-interfaces.


                      encounter.information.request & medical.record.data.request




 Confidencial da Companhia Philips                                                      Página 5 de 26
                                       CÓPIAS NÃO SÃO CONTROLADAS
                                     Manual de Integração        HISS EMR
                                                                 Código documento: ########
                               MANUAL DE INTEGRAÇÃO              Revisão: ###
                                                                 Status: ###
                               TASY – MEDICAL RECORD
                                        DATA


 3.2 Verificando o status do Tasy-interfaces:




Confidencial da Companhia Philips                                               Página 6 de 26
                                    CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração            HISS EMR
                                                                      Código documento: ########
                                MANUAL DE INTEGRAÇÃO                  Revisão: ###
                                                                      Status: ###
                                TASY – MEDICAL RECORD
                                         DATA


5 REQUISIÇÕES
      5.1 Clinical Notes – Notas Clínicas

Endpoint
GET /api/encounterInformation/{identityDocumentNumber}/patient-care


Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/encounterInformation/989997/clinical-notes
Método: GET
Content-Type: application/json
Parâmetros
- {encounterId} (Path) - Obrigatório: ID do atendimento (NR_ATENDIMENTO)
- evolutionTypes (Query) - Opcional: Tipos de evolução clínica (ex: 'E,AB')


SQL
SELECT
  ep.CD_EVOLUCAO,
  ep.DT_EVOLUCAO,
  ep.DS_EVOLUCAO,
  ep.NR_ATENDIMENTO,
  ep.IE_SITUACAO,
  ep.IE_EVOLUCAO_CLINICA,
  ep.IE_TIPO_EVOLUCAO,
  ep.CD_MEDICO,
  substr(obter_valor_dominio(72, ep.ie_tipo_evolucao), 1, 200) AS ds_function,
  substr(Obter_desc_tipo_evolucao(ep.ie_evolucao_clinica), 1, 200) AS ds_type_clinical_notes,
  substr(Obter_nome_pf(ep.cd_medico), 1, 200) AS nm_physician
FROM EVOLUCAO_PACIENTE ep
WHERE ep.NR_ATENDIMENTO = :encounterId
AND ep.IE_SITUACAO = 'A'
ORDER BY ep.DT_EVOLUCAO DESC




 Confidencial da Companhia Philips                                                   Página 7 de 26
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                         Manual de Integração         HISS EMR
                                                                      Código documento: ########
                                   MANUAL DE INTEGRAÇÃO               Revisão: ###
                                                                      Status: ###
                                   TASY – MEDICAL RECORD
                                            DATA

Mapeamento de Campos (Banco → JSON)
{
    "clinicalNotesId": "CD_EVOLUCAO",
    "clinicalNotesDate": "DT_EVOLUCAO",
    "clinicalNotes": "DS_EVOLUCAO",
    "encounterId": "NR_ATENDIMENTO",
    "status": "IE_SITUACAO",
    "clinicalEvolutionType": "IE_EVOLUCAO_CLINICA",
    "typeOfClinicalNotes": "ds_type_clinical_notes",
    "function": "ds_function",
    "physician": "nm_physician",
    "physicianCode": "CD_MEDICO",
    "patientId": "CD_PESSOA_FISICA"
}




        5.2 Patient Care (Atendimentos do Paciente)

Endpoint
GET /api/encounterInformation/{identityDocumentNumber}/patient-care


Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/encounterInformation/9890809/patient-care
Método: GET
Content-Type: application/json


Parâmetros
- {identityDocumentNumber} (Path) - Obrigatório: Número do documento de identidade
(NR_IDENTIDADE)
- gender (Query) - Opcional: Sexo do paciente (ex: 'F' ou 'M')
- birthDate (Query) - Opcional: Data de nascimento no formato DD/MM/YYYY




    Confidencial da Companhia Philips                                                Página 8 de 26
                                        CÓPIAS NÃO SÃO CONTROLADAS
                                         Manual de Integração          HISS EMR
                                                                       Código documento: ########
                                   MANUAL DE INTEGRAÇÃO                Revisão: ###
                                                                       Status: ###
                                   TASY – MEDICAL RECORD
                                            DATA

SQL
SELECT
  a.cd_pessoa_fisica as personId,
  a.nr_atendimento as encounter,
  substr(obter_nome_tipo_atend(a.IE_TIPO_ATENDIMENTO), 1, 30) as encounterType,
  a.DT_ENTRADA as admissionDate,
  Nvl(Nvl(a.DT_ALTA, a.DT_FIM_CONTA), a.dt_saida_real) as dischargeDate
FROM atendimento_paciente a, PESSOA_FISICA c
WHERE a.cd_pessoa_fisica = c.cd_pessoa_fisica
AND c.NR_IDENTIDADE = :identityDocumentNumber
Mapeamento de Campos (Banco → JSON)
{
    "patientId": "cd_pessoa_fisica", // CD_PESSOA_FISICA
    "encounterId": "encounter", // NR_ATENDIMENTO
    "encounterType": "encounterType", // IE_TIPO_ATENDIMENTO (descritivo)
    "admissionDate": "admissionDate", // DT_ENTRADA
    "dischargeDate": "dischargeDate" // DT_ALTA/DT_FIM_CONTA/dt_saida_real
}



        5.3 Health History (Histórico de Saúde)

               5.3.1 Allergies

Endpoint
GET /api/health-history/allergies-history/patient/{patientId}
Exemplo de Requisição

URL: http://bifrostdev.whebdc.com.br:9020/api/health-history/allergies-history/patient/632516
Método: GET
Content-Type: application/json
Parâmetros
- {patientId} (Path) - Obrigatório: ID do paciente (CD_PESSOA_FISICA)




    Confidencial da Companhia Philips                                                 Página 9 de 26
                                        CÓPIAS NÃO SÃO CONTROLADAS
                                     Manual de Integração        HISS EMR
                                                                 Código documento: ########
                                MANUAL DE INTEGRAÇÃO             Revisão: ###
                                                                 Status: ###
                                TASY – MEDICAL RECORD
                                         DATA

SQL

SELECT
  pa.NR_SEQUENCIA AS id,
  pa.CD_PESSOA_FISICA AS cd_pessoa_fisica,
  pa.NR_ATENDIMENTO AS nr_atendimento,
  pa.DT_REGISTRO AS dt_registro,
  pa.DT_INICIO AS dt_inicio,
  pa.DT_FIM AS dt_fim,
  pa.IE_CLASSIFICACAO AS ie_classificacao,
  pa.IE_CONFIRMACAO AS ie_confirmacao,
  pa.IE_ESTADO_ATUAL AS ie_estado_atual,
  pa.IE_INTENSIDADE AS ie_intensidade,
  pa.CD_MATERIAL AS cd_material,
  substr(obter_desc_material(pa.CD_MATERIAL),1,254) AS ds_material,
  pa.DS_MEDIC_NAO_CAD AS ds_medic_nao_cad,
  pa.CD_DOENCA AS cd_doenca,
  substr(obter_desc_cid(pa.CD_DOENCA),1,200) AS ds_cid_doenca,
  pa.NR_SEQ_REACAO AS nr_seq_reacao,
  substr(obter_desc_reacao_alergica(pa.NR_SEQ_REACAO),1,100) AS ds_reacao,
  pa.DS_OBSERVACAO AS ds_observacao,
  substr(obter_valor_dominio(1337,pa.IE_ABORDAGEM),1,60) AS ds_abordagem,
  pa.CD_PROFISSIONAL AS cd_profissional,
  substr(obter_nome_pf(pa.CD_PROFISSIONAL),1,100) AS nm_profissional
FROM PACIENTE_ALERGIA pa
WHERE pa.DT_LIBERACAO IS NOT NULL
AND pa.CD_PESSOA_FISICA = :patientId
ORDER BY pa.DT_REGISTRO DESC




Confidencial da Companhia Philips                                               Página 10 de 26
                                    CÓPIAS NÃO SÃO CONTROLADAS
                                         Manual de Integração          HISS EMR
                                                                       Código documento: ########
                                    MANUAL DE INTEGRAÇÃO               Revisão: ###
                                                                       Status: ###
                                    TASY – MEDICAL RECORD
                                             DATA

Mapeamento de Campos (Banco → JSON)

{
     "patientId": "CD_PESSOA_FISICA", // Identificador do paciente
     "encounterId": "NR_ATENDIMENTO", // ID do atendimento
     "allergiesHistory": {
        "items": [
           {
              "id": "NR_SEQUENCIA", // ID da alergia
              "registerDate": "DT_REGISTRO", // Data de registro
              "classification": "IE_CLASSIFICACAO", // Classificação da alergia
              "confirmationStatus": "IE_CONFIRMACAO", // Status de confirmação
              "currentStatus": "IE_ESTADO_ATUAL", // Estado atual
              "material": {
                 "code": "CD_MATERIAL", // Código do material
                 "description": "ds_material" // Descrição do material
              },
              "cid": {
                 "code": "CD_DOENCA", // Código CID
                 "description": "ds_cid_doenca" // Descrição CID
              },
              "reactionType": {
                 "code": "NR_SEQ_REACAO", // Código da reação
                 "description": "ds_reacao" // Descrição da reação
              },
              "approach": "ds_abordagem", // Abordagem clínica
              "observation": "DS_OBSERVACAO", // Observações
              "professional": {
                 "code": "CD_PROFISSIONAL", // Código do profissional
                 "name": "nm_profissional" // Nome do profissional
              }
           }
        ]
     }
}




    Confidencial da Companhia Philips                                                 Página 11 de 26
                                        CÓPIAS NÃO SÃO CONTROLADAS
                                         Manual de Integração         HISS EMR
                                                                      Código documento: ########
                                    MANUAL DE INTEGRAÇÃO              Revisão: ###
                                                                      Status: ###
                                    TASY – MEDICAL RECORD
                                             DATA


                5.3.2 Current Medications (Medicações Atuais)

Endpoint
GET /api/health-history/current-medications/patient/{patientId}
Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/health-history/current-medications/patient/632516
Método: GET
Content-Type: application/json
Parâmetros
- {patientId} (Path) - Obrigatório: ID do paciente (CD_PESSOA_FISICA)
SQL
SELECT
  pmu.NR_SEQUENCIA AS id,
  pmu.CD_PESSOA_FISICA AS cd_pessoa_fisica,
  pmu.NR_ATENDIMENTO AS nr_atendimento,
  pmu.DT_REGISTRO AS dt_registro,
  pmu.CD_MATERIAL AS cd_material,
  substr(obter_desc_material(pmu.CD_MATERIAL),1,100) AS ds_material,
  pmu.DS_MEDICAMENTO AS ds_medicamento,
  pmu.DS_DESCRICAO_COMPLEMENTAR AS ds_descricao_complementar,
  SUBSTR(DECODE(OBTER_FICHA_TECNICA_MEDIC(pmu.CD_MATERIAL), NULL,
obter_desc_material(Obter_Mat_Generico(pmu.CD_MATERIAL)),
OBTER_PRINC_ATIVO_MATMED(pmu.CD_MATERIAL)),1,255) AS ds_principio_ativo,
  pmu.QT_DOSE AS qt_dose,
  pmu.CD_UNID_MED AS cd_unid_med,
  substr(obter_desc_intervalo_prescr(pmu.CD_INTERVALO),1,60) AS ds_intervalo,
  pmu.DS_HORARIOS AS ds_horarios,
  pmu.IE_VIA_APLICACAO AS ie_via_aplicacao,
  pmu.DT_INICIO AS dt_inicio,
  pmu.DT_FIM AS dt_fim,
  pmu.DS_OBSERVACAO AS ds_observacao,
  pmu.CD_PROFISSIONAL AS cd_profissional,
  substr(obter_nome_pf(pmu.cd_profissional),1,100) AS nm_profissional
FROM PACIENTE_MEDIC_USO pmu
WHERE pmu.DT_LIBERACAO IS NOT NULL
AND pmu.CD_PESSOA_FISICA = :patientId
ORDER BY pmu.DT_REGISTRO DESC
Mapeamento de Campos (Banco → JSON)
{
     "patientId": "CD_PESSOA_FISICA", // ID do paciente



    Confidencial da Companhia Philips                                                Página 12 de 26
                                        CÓPIAS NÃO SÃO CONTROLADAS
                                     Manual de Integração        HISS EMR
                                                                 Código documento: ########
                                MANUAL DE INTEGRAÇÃO             Revisão: ###
                                                                 Status: ###
                                TASY – MEDICAL RECORD
                                         DATA

  "encounterId": "NR_ATENDIMENTO", // ID do atendimento
  "currentMedications": {
    "items": [
       {
          "id": "NR_SEQUENCIA", // ID da medicação
          "registerDate": "DT_REGISTRO", // Data de registro
          "material": {
             "code": "CD_MATERIAL", // Código do material
             "description": "ds_material" // Descrição do material
          },
          "medicationName": "DS_MEDICAMENTO", // Nome do medicamento
          "complementaryDescription": "DS_DESCRICAO_COMPLEMENTAR", // Descrição
complementar
          "activeIngredient": "ds_principio_ativo", // Princípio ativo
          "dose": "QT_DOSE", // Dose
          "unitOfMeasure": "CD_UNID_MED", // Unidade de medida
          "interval": "ds_intervalo", // Intervalo
          "schedule": "DS_HORARIOS", // Horários
          "administrationRoute": "IE_VIA_APLICACAO", // Via de aplicação
          "startDate": "DT_INICIO", // Data de início
          "endDate": "DT_FIM", // Data de fim
          "observation": "DS_OBSERVACAO", // Observações
          "professional": {
             "code": "CD_PROFISSIONAL", // Código do profissional
             "name": "nm_profissional" // Nome do profissional
          }
       }
    ]
  }
}




Confidencial da Companhia Philips                                               Página 13 de 26
                                    CÓPIAS NÃO SÃO CONTROLADAS
                                        Manual de Integração            HISS EMR
                                                                        Código documento: ########
                                 MANUAL DE INTEGRAÇÃO                   Revisão: ###
                                                                        Status: ###
                                 TASY – MEDICAL RECORD
                                          DATA


             5.3.3 Past History (Histórico Clínico)

Endpoint
GET /api/health-history/clinical-history/patient/{patientId}
Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/health-history/clinical-history/patient/632516
Método: GET
Content-Type: application/json
Parâmetros
- {patientId} (Path) - Obrigatório: ID do paciente (CD_PESSOA_FISICA)

SQL Utilizado
SELECT
  pac.NR_SEQUENCIA AS nr_sequencia,
  substr(obter_desc_pe_doenca(pac.NR_SEQ_DOENCA),1,80) AS nr_seq_doenca,
  pac.CD_PESSOA_FISICA AS cd_pessoa_fisica,
  pac.NR_ATENDIMENTO AS nr_atendimento,
  pac.DT_REGISTRO AS dt_registro,
  pac.CD_CID AS cd_cid,
  substr(obter_desc_cid(pac.CD_DOENCA),1,200) AS ds_cid_doenca,
  pac.CD_DOENCA AS cd_doenca,
  pac.DS_DOENCA AS ds_doenca,
  pac.IE_PACIENTE AS ie_paciente,
  substr(obter_valor_dominio(1332,pac.IE_STATUS),1,60) AS ie_status,
  pac.DT_INICIO AS dt_inicio,
  pac.DT_FIM AS dt_fim,
  pac.QT_AGE_DIAGNOSIS AS qt_age_diagnosis,
  pac.IE_DOENCA_CRONICA AS ie_doenca_cronica,
  pac.DS_OBSERVACAO AS ds_observacao,
  pac.CD_PROFISSIONAL AS cd_profissional,
  substr(obter_nome_pf(pac.cd_profissional),1,100) AS nm_profissional
FROM PACIENTE_ANTEC_CLINICO pac
WHERE pac.DT_LIBERACAO IS NOT NULL
AND pac.CD_PESSOA_FISICA = :patientId
ORDER BY pac.DT_REGISTRO DESC




 Confidencial da Companhia Philips                                                     Página 14 de 26
                                      CÓPIAS NÃO SÃO CONTROLADAS
                                         Manual de Integração        HISS EMR
                                                                     Código documento: ########
                                    MANUAL DE INTEGRAÇÃO             Revisão: ###
                                                                     Status: ###
                                    TASY – MEDICAL RECORD
                                             DATA

Mapeamento de Campos (Banco → JSON)
{
     "patientId": "CD_PESSOA_FISICA", // ID do paciente
     "encounterId": "NR_ATENDIMENTO", // ID do atendimento
     "pastHistory": {
       "items": [
          {
             "id": "NR_SEQUENCIA", // ID do histórico
             "registerDate": "DT_REGISTRO", // Data de registro
             "diseaseDescription": "nr_seq_doenca", // Descrição da doença
             "cid": {
                "code": "CD_CID", // Código CID
                "description": "ds_cid_doenca" // Descrição CID
             },
             "diseaseCode": "CD_DOENCA", // Código da doença
             "diseaseName": "DS_DOENCA", // Nome da doença
             "patient": "IE_PACIENTE", // Indicador do paciente
             "status": "ie_status", // Status
             "startDate": "DT_INICIO", // Data de início
             "endDate": "DT_FIM", // Data de fim
             "ageAtDiagnosis": "QT_AGE_DIAGNOSIS", // Idade no diagnóstico
             "chronicDisease": "IE_DOENCA_CRONICA", // Doença crônica
             "observation": "DS_OBSERVACAO", // Observações
             "professional": {
                "code": "CD_PROFISSIONAL", // Código do profissional
                "name": "nm_profissional" // Nome do profissional
             }
          }
       ]
     }
}




    Confidencial da Companhia Philips                                               Página 15 de 26
                                        CÓPIAS NÃO SÃO CONTROLADAS
                                       Manual de Integração            HISS EMR
                                                                       Código documento: ########
                                 MANUAL DE INTEGRAÇÃO                  Revisão: ###
                                                                       Status: ###
                                 TASY – MEDICAL RECORD
                                          DATA


             5.3.4 Social History (Histórico Social)

Endpoint
GET /api/health-history/social-history/patient/{patientId}
Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/health-history/social-history/patient/632516
Método: GET
Content-Type: application/json
Parâmetros
- {patientId} (Path) - Obrigatório: ID do paciente (CD_PESSOA_FISICA)
SQL Utilizado
SELECT
  phv.NR_SEQUENCIA AS id,
  phv.CD_PESSOA_FISICA AS cd_pessoa_fisica,
  phv.NR_ATENDIMENTO AS nr_atendimento,
  phv.DT_REGISTRO AS dt_registro,
  phv.IE_NEGA_HABITO AS ie_nega_habito,
  substr(obter_valor_dominio(1335,phv.ie_classificacao),1,60) AS ds_classificacao,
  substr(obter_desc_tipo_vicio(phv.NR_SEQ_TIPO),1,80) AS ds_tipo_vicio,
  phv.NR_SEQ_MARCA AS nr_seq_marca,
  phv.CD_UNIDADE_MEDIDA AS cd_unidade_medida,
  phv.QT_UTILIZACAO AS qt_utilizacao,
  phv.DS_QUANTIDADE AS ds_quantidade,
  phv.IE_FREQUENCIA AS ie_frequencia,
  phv.QT_MACO_ANO AS qt_maco_ano,
  obter_desc_ipa(phv.QT_MACO_ANO) AS ds_maco_ano,
  phv.QT_IDADE_EXP AS qt_idade_exp,
  phv.QT_IDADE_REG AS qt_idade_reg,
  phv.QT_NICOTINE_DEPENDENCE AS qt_nicotine_dependence,
  phv.IE_PASSIVE_SMOKER AS ie_passive_smoker,
  phv.DT_INICIO AS dt_inicio,
  phv.DT_FIM AS dt_fim,
  phv.DS_CONSEQUENCIA AS ds_consequencia,
  phv.DS_ANTECEDENTES_FAM AS ds_antecedentes_fam,
  phv.DS_OBSERVACAO AS ds_observacao,
  phv.CD_PROFISSIONAL AS cd_profissional,
  substr(obter_nome_pf(phv.cd_profissional),1,100) AS nm_profissional
FROM PACIENTE_HABITO_VICIO phv
WHERE phv.DT_LIBERACAO IS NOT NULL
AND phv.CD_PESSOA_FISICA = :patientId
ORDER BY phv.DT_REGISTRO DESC



 Confidencial da Companhia Philips                                                    Página 16 de 26
                                      CÓPIAS NÃO SÃO CONTROLADAS
                                         Manual de Integração        HISS EMR
                                                                     Código documento: ########
                                    MANUAL DE INTEGRAÇÃO             Revisão: ###
                                                                     Status: ###
                                    TASY – MEDICAL RECORD
                                             DATA

Mapeamento de Campos (Banco → JSON)
{
     "patientId": "CD_PESSOA_FISICA", // ID do paciente
     "encounterId": "NR_ATENDIMENTO", // ID do atendimento
     "socialHistory": {
       "items": [
          {
             "id": "NR_SEQUENCIA", // ID do histórico social
             "registerDate": "DT_REGISTRO", // Data de registro
             "deniesHabits": "IE_NEGA_HABITO", // Nega hábitos
             "classification": "ds_classificacao", // Classificação
             "addictionType": "ds_tipo_vicio", // Tipo de vício
             "brandSequence": "NR_SEQ_MARCA", // Sequência da marca
             "unitOfMeasure": "CD_UNIDADE_MEDIDA", // Unidade de medida
             "quantityUsed": "QT_UTILIZACAO", // Quantidade utilizada
             "quantityDescription": "DS_QUANTIDADE", // Descrição da quantidade
             "frequency": "IE_FREQUENCIA", // Frequência
             "packsPerYear": "QT_MACO_ANO", // Maços por ano
             "packsPerYearDescription": "ds_maco_ano", // Descrição maços/ano
             "exposureAge": "QT_IDADE_EXP", // Idade de exposição
             "regularAge": "QT_IDADE_REG", // Idade regular
             "nicotineDependence": "QT_NICOTINE_DEPENDENCE", // Dependência de nicotina
             "passiveSmoker": "IE_PASSIVE_SMOKER", // Fumante passivo
             "startDate": "DT_INICIO", // Data de início
             "endDate": "DT_FIM", // Data de fim
             "consequences": "DS_CONSEQUENCIA", // Consequências
             "familyHistory": "DS_ANTECEDENTES_FAM", // Antecedentes familiares
             "observation": "DS_OBSERVACAO", // Observações
             "professional": {
                "code": "CD_PROFISSIONAL", // Código do profissional
                "name": "nm_profissional" // Nome do profissional
             }
          }
       ]
     }
}




    Confidencial da Companhia Philips                                               Página 17 de 26
                                        CÓPIAS NÃO SÃO CONTROLADAS
                                       Manual de Integração            HISS EMR
                                                                       Código documento: ########
                                 MANUAL DE INTEGRAÇÃO                  Revisão: ###
                                                                       Status: ###
                                 TASY – MEDICAL RECORD
                                          DATA


             5.3.5 Surgical History (Histórico Cirúrgico)
Endpoint
GET /api/health-history/surgical-history/patient/{patientId}
Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/health-history/surgical-history/patient/632516
Método: GET
Content-Type: application/json
Parâmetros
- {patientId} (Path) - Obrigatório: ID do paciente (CD_PESSOA_FISICA)

SQL
SELECT
  hsc.NR_SEQUENCIA AS id,
  hsc.CD_PESSOA_FISICA AS cd_pessoa_fisica,
  hsc.NR_ATENDIMENTO AS nr_atendimento,
  hsc.DT_ATUALIZACAO_NREC AS dt_registro,
  hsc.DT_CIRURGIA AS dt_cirurgia,
  hsc.DT_INICIO AS dt_inicio,
  hsc.DT_FIM AS dt_fim,
  hsc.CD_PROCEDIMENTO AS cd_procedimento,
  hsc.CD_PROCEDIMENTO_LOC AS cd_procedimento_loc,
  hsc.NR_SEQ_PROC_INTERNO AS nr_seq_proc_interno,
  hsc.DS_PROCEDIMENTO_INF AS ds_procedimento_inf,
  substr(Obter_Desc_Procedimento(hsc.CD_PROCEDIMENTO,
hsc.IE_ORIGEM_PROCED),1,255) AS ds_procedimento,
  hsc.CD_DOENCA_CID AS cd_doenca_cid,
  substr(obter_desc_cid(hsc.CD_DOENCA_CID),1,200) AS ds_doenca_cid,
  hsc.DS_LOCAL AS ds_local,
  hsc.DS_COMPLICACAO AS ds_complicacao,
  hsc.DS_OBSERVACAO AS ds_observacao,
  hsc.IE_TIPO_ANESTESIA AS ie_tipo_anestesia,
  substr(obter_valor_dominio(36,hsc.ie_tipo_anestesia),1,100) AS ds_tipo_anestesia,
  hsc.IE_NEGA_CIRURGIAS AS ie_nega_cirurgias,
  hsc.CD_PROFISSIONAL AS cd_profissional,
  substr(obter_nome_pf(hsc.cd_profissional),1,100) AS nm_profissional
FROM HISTORICO_SAUDE_CIRURGIA hsc
WHERE hsc.DT_LIBERACAO IS NOT NULL
AND hsc.CD_PESSOA_FISICA = :patientId
ORDER BY hsc.DT_ATUALIZACAO_NREC DESC




 Confidencial da Companhia Philips                                                    Página 18 de 26
                                      CÓPIAS NÃO SÃO CONTROLADAS
                                         Manual de Integração        HISS EMR
                                                                     Código documento: ########
                                    MANUAL DE INTEGRAÇÃO             Revisão: ###
                                                                     Status: ###
                                    TASY – MEDICAL RECORD
                                             DATA

Mapeamento de Campos (Banco → JSON)
{
     "patientId": "CD_PESSOA_FISICA", // ID do paciente
     "encounterId": "NR_ATENDIMENTO", // ID do atendimento
     "surgicalHistory": {
       "items": [
          {
             "id": "NR_SEQUENCIA", // ID do histórico cirúrgico
             "registerDate": "DT_ATUALIZACAO_NREC", // Data de registro
             "surgeryDate": "DT_CIRURGIA", // Data da cirurgia
             "startDate": "DT_INICIO", // Data de início
             "endDate": "DT_FIM", // Data de fim
             "procedure": {
                "code": "CD_PROCEDIMENTO", // Código do procedimento
                "localCode": "CD_PROCEDIMENTO_LOC", // Código local do procedimento
                "internalSequence": "NR_SEQ_PROC_INTERNO", // Sequência interna
                "description": "ds_procedimento", // Descrição do procedimento
                "informedDescription": "DS_PROCEDIMENTO_INF" // Descrição informada
             },
             "cid": {
                "code": "CD_DOENCA_CID", // Código CID
                "description": "ds_doenca_cid" // Descrição CID
             },
             "location": "DS_LOCAL", // Local da cirurgia
             "complications": "DS_COMPLICACAO", // Complicações
             "observation": "DS_OBSERVACAO", // Observações
             "anesthesia": {
                "type": "IE_TIPO_ANESTESIA", // Tipo de anestesia
                "description": "ds_tipo_anestesia" // Descrição da anestesia
             },
             "deniesSurgeries": "IE_NEGA_CIRURGIAS", // Nega cirurgias
             "professional": {
                "code": "CD_PROFISSIONAL", // Código do profissional
                "name": "nm_profissional" // Nome do profissional
             }
          }
       ]
     }
}




    Confidencial da Companhia Philips                                               Página 19 de 26
                                        CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração           HISS EMR
                                                                     Código documento: ########
                                 MANUAL DE INTEGRAÇÃO                Revisão: ###
                                                                     Status: ###
                                 TASY – MEDICAL RECORD
                                          DATA


      5.4 Laboratory Tests (Exames Laboratoriais)
Endpoint
GET /api/encounterInformation/{encounterId}/laboratory-results
Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/encounterInformation/989997/laboratory-results
Método: GET
Content-Type: application/json
Parâmetros
- {encounterId} (Path) - Obrigatório: ID do atendimento (NR_ATENDIMENTO)
SQL
SELECT
  ELR.NR_ATENDIMENTO AS ENCOUNTER_ID,
  ELR.NR_PRESCRICAO AS PRESCRIPTION,
  ELI.NR_SEQ_PRESCR AS EXAM_GROUP,
  ELI.NR_SEQUENCIA AS EXAM_SEQ,
  OBTER_DESC_EXAME(ELI.NR_SEQ_EXAME) AS EXAM_NAME,
  ELI.QT_RESULTADO AS RESULT_QUANTITY,
  ELI.DS_RESULTADO AS RESULT_TEXT,
  ELI.PR_RESULTADO AS RESULT_PERCENTAGE,
  ELI.DS_REFERENCIA AS REFERENCE_TEXT,
  ELI.QT_MINIMA AS REFERENCE_MIN,
  ELI.QT_MAXIMA AS REFERENCE_MAX,
  OBTER_PF_USUARIO(ELR.NM_USUARIO, 'c') AS REQUESTER_NAME,
  OBTER_DADOS_USUARIO_OPCAO(ELR.NM_USUARIO, 'C') AS REQUESTER_COD,
  RLP.DS_PDF_SERIAL AS ATTACHMENT
FROM EXAME_LAB_RESULTADO ELR
LEFT JOIN EXAME_LAB_RESULT_ITEM ELI ON ELI.NR_SEQ_RESULTADO =
ELR.NR_SEQ_RESULTADO
LEFT JOIN RESULT_LABORATORIO_PDF RLP ON ELR.NR_PRESCRICAO =
RLP.NR_PRESCRICAO
WHERE ELR.NR_ATENDIMENTO = :ENCOUNTERID
ORDER BY ELR.NR_ATENDIMENTO, ELR.NR_PRESCRICAO, ELI.NR_SEQ_PRESCR




 Confidencial da Companhia Philips                                                  Página 20 de 26
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                         Manual de Integração        HISS EMR
                                                                     Código documento: ########
                                    MANUAL DE INTEGRAÇÃO             Revisão: ###
                                                                     Status: ###
                                    TASY – MEDICAL RECORD
                                             DATA

Mapeamento de Campos (Banco → JSON)
{
     "encounterId": "ENCOUNTER_ID", // NR_ATENDIMENTO
     "prescriptions": [
        {
          "prescriptionId": "PRESCRIPTION", // NR_PRESCRICAO
          "requesterName": "REQUESTER_NAME", // Nome do solicitante
          "requesterCode": "REQUESTER_COD", // Código do solicitante
          "examGroups": [
             {
                "examGroupId": "EXAM_GROUP", // NR_SEQ_PRESCR
                "examGroupName": "EXAM_NAME", // Nome do grupo de exame
                "results": [
                   {
                     "itemId": "EXAM_SEQ", // NR_SEQUENCIA
                     "itemName": "EXAM_NAME", // Nome do exame
                     "resultQuantity": "RESULT_QUANTITY", // QT_RESULTADO
                     "resultText": "RESULT_TEXT", // DS_RESULTADO
                     "resultPercentage": "RESULT_PERCENTAGE", // PR_RESULTADO
                     "referenceText": "REFERENCE_TEXT", // DS_REFERENCIA
                     "referenceMin": "REFERENCE_MIN", // QT_MINIMA
                     "referenceMax": "REFERENCE_MAX", // QT_MAXIMA
                     "attachment": "ATTACHMENT" // DS_PDF_SERIAL
                   }
                ]
             }
          ]
        }
     ]
}




    Confidencial da Companhia Philips                                               Página 21 de 26
                                        CÓPIAS NÃO SÃO CONTROLADAS
                                         Manual de Integração        HISS EMR
                                                                     Código documento: ########
                                    MANUAL DE INTEGRAÇÃO             Revisão: ###
                                                                     Status: ###
                                    TASY – MEDICAL RECORD
                                             DATA

Estrutura do JSON Retornado
{
     "encounterId": "989997",
     "prescriptions": [
        {
          "prescriptionId": "394715",
          "requesterName": "Jane Doe",
          "requesterCode": "643451",
          "examGroups": [
             {
                "examGroupId": "12345",
                "examGroupName": "Hemograma",
                "results": [
                   {
                     "itemId": "67890",
                     "itemName": "Hemoglobina",
                     "result": "12.5",
                     "unit": "g/dL",
                     "referenceRange": "12.0-15.5"
                   }
                ]
             }
          ]
        }
     ]
}




    Confidencial da Companhia Philips                                               Página 22 de 26
                                        CÓPIAS NÃO SÃO CONTROLADAS
                                      Manual de Integração          HISS EMR
                                                                    Código documento: ########
                                 MANUAL DE INTEGRAÇÃO               Revisão: ###
                                                                    Status: ###
                                 TASY – MEDICAL RECORD
                                          DATA


      5.5 Non-Laboratory Tests (Exames de Imagem/Diagnósticos)

Endpoint
GET /api/encounterInformation/{encounterId}/img-result
Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/encounterInformation/1277509/img-result
Método: GET
Content-Type: application/json
Parâmetros
- {encounterId} (Path) - Obrigatório: ID do atendimento (NR_ATENDIMENTO)
Principais Tabelas Utilizadas
- LAUDO_PACIENTE (LP)
- LAUDO_PACIENTE_PDF_SERIAL (LPPS)
- PROC_INTERNO (PI)
SQL Utilizado
SELECT
  LP.NR_SEQUENCIA                   DIAGNOSTIC_REPORT_ID,
  LP.NR_ATENDIMENTO                    ENCOUNTER_ID,
  LP.NR_PRESCRICAO                    PRESCRIPTION,
  OBTER_DADO_PROC_LAUDO(LP.NR_SEQUENCIA, 6)         PROCEDURE_CODE,
  OBTER_DESCRICAO_EXAMES_LAUDO(LP.NR_SEQUENCIA, 'D')
DIAGNOSTIC_REPORT_NAME,
  LP.CD_MEDICO_RESP                    PERFORMER_CODE,
  OBTER_NOME_MEDICO(LP.CD_MEDICO_RESP, 'n')       PERFORMER,
  LP.DT_LIBERACAO                   RELEASE_DATE,
  LPPS.NR_ACESSO_DICOM                   DICOM_NUMBER,
  PI.CD_INTEGRACAO                   INTEGRATION_CODE,
  LPPS.DS_PDF_SERIAL                  ATTACHMENT
FROM LAUDO_PACIENTE LP
JOIN LAUDO_PACIENTE_PDF_SERIAL LPPS ON LPPS.NR_SEQ_LAUDO = LP.NR_SEQUENCIA
LEFT JOIN PROC_INTERNO PI ON PI.NR_SEQUENCIA =
OBTER_DADO_PROC_LAUDO(LP.NR_SEQUENCIA, 6)
WHERE LP.DT_LIBERACAO IS NOT NULL
AND LP.NR_ATENDIMENTO = :NR_ATENDIMENTO
ORDER BY LP.NR_SEQUENCIA DESC




 Confidencial da Companhia Philips                                                 Página 23 de 26
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                         Manual de Integração        HISS EMR
                                                                     Código documento: ########
                                    MANUAL DE INTEGRAÇÃO             Revisão: ###
                                                                     Status: ###
                                    TASY – MEDICAL RECORD
                                             DATA

Mapeamento de Campos (Banco → JSON)
{
     "diagnosticReports": [
        {
          "diagnosticReportId": "DIAGNOSTIC_REPORT_ID", // NR_SEQUENCIA
          "encounterId": "ENCOUNTER_ID", // NR_ATENDIMENTO
          "prescription": "PRESCRIPTION", // NR_PRESCRICAO
          "procedureCode": "PROCEDURE_CODE", // Código do procedimento
          "diagnosticReportName": "DIAGNOSTIC_REPORT_NAME", // Nome do relatório
          "performer": {
             "code": "PERFORMER_CODE", // CD_MEDICO_RESP
             "name": "PERFORMER" // Nome do médico responsável
          },
          "releaseDate": "RELEASE_DATE", // DT_LIBERACAO
          "dicomNumber": "DICOM_NUMBER", // NR_ACESSO_DICOM
          "integrationCode": "INTEGRATION_CODE", // CD_INTEGRACAO
          "attachment": "ATTACHMENT" // DS_PDF_SERIAL (BASE64)
        }
     ]
}



         5.6 Emergency Discharge (Alta de Emergência)
Endpoint
GET /api/encounterInformation/{encounterId}/emergency-discharge
Exemplo de Requisição
URL: http://bifrostdev.whebdc.com.br:9020/api/encounterInformation/989997/emergency-discharge
Método: GET
Content-Type: application/json
Parâmetros
- {encounterId} (Path) - Obrigatório: ID do atendimento (NR_ATENDIMENTO)




    Confidencial da Companhia Philips                                               Página 24 de 26
                                        CÓPIAS NÃO SÃO CONTROLADAS
                                         Manual de Integração        HISS EMR
                                                                     Código documento: ########
                                    MANUAL DE INTEGRAÇÃO             Revisão: ###
                                                                     Status: ###
                                    TASY – MEDICAL RECORD
                                             DATA

SQL
SELECT
  aa.NR_ATENDIMENTO as encounterId,
  aa.CD_TIPO_ALTA as dischargeTypeCode,
  substr(obter_desc_tipo_alta(aa.CD_TIPO_ALTA), 1, 100) as dischargeTypeDescription,
  aa.DS_ORIENTACAO as orientationText,
  aa.CD_ESPECIALIDADE as specialtyCode,
  substr(obter_desc_especialidade(aa.CD_ESPECIALIDADE), 1, 100) as specialtyDescription,
  aa.NR_SEQ_AREA_DESTINO as destinationAreaSequence,
  aa.CD_MEDICO as doctorCode,
  substr(obter_nome_medico(aa.CD_MEDICO, 'N'), 1, 200) as doctorName,
  aa.IE_MEDICO_CIENTE as doctorAware,
  aa.CD_INSTITUICAO_DESTINO as destinationInstitutionCode,
  substr(obter_desc_empresa(aa.CD_INSTITUICAO_DESTINO), 1, 200) as
destinationInstitutionName,
  aa.CD_SETOR_DESTINO as destinationSectorCode,
  substr(obter_desc_setor(aa.CD_SETOR_DESTINO), 1, 100) as destinationSectorDescription,
  aa.CD_MOTIVO_ALTA as dischargeReasonCode,
  substr(obter_desc_motivo_alta(aa.CD_MOTIVO_ALTA), 1, 100) as dischargeReasonDescription,
  aa.IE_FICOU_OBSERVACAO as stayedInObservation
FROM ATENDIMENTO_ALTA aa
WHERE aa.NR_ATENDIMENTO = :encounterId
Mapeamento de Campos (Banco → JSON)
{
     "encounterId": "NR_ATENDIMENTO",
     "dischargeTypeCode": "CD_TIPO_ALTA",
     "dischargeTypeDescription": "obter_desc_tipo_alta()",
     "orientationText": "DS_ORIENTACAO",
     "specialtyCode": "CD_ESPECIALIDADE",
     "specialtyDescription": "obter_desc_especialidade()",
     "destinationAreaSequence": "NR_SEQ_AREA_DESTINO",
     "doctorCode": "CD_MEDICO",
     "doctorName": "obter_nome_medico()",
     "doctorAware": "IE_MEDICO_CIENTE", // "S"/"N" → true/false
     "destinationInstitutionCode": "CD_INSTITUICAO_DESTINO",
     "destinationInstitutionName": "obter_desc_empresa()",
     "destinationSectorCode": "CD_SETOR_DESTINO",
     "destinationSectorDescription": "obter_desc_setor()",
     "dischargeReasonCode": "CD_MOTIVO_ALTA",
     "dischargeReasonDescription": "obter_desc_motivo_alta()",
     "stayedInObservation": "IE_FICOU_OBSERVACAO" // "S"/"N" → true/false
}


    Confidencial da Companhia Philips                                               Página 25 de 26
                                        CÓPIAS NÃO SÃO CONTROLADAS
                                       Manual de Integração        HISS EMR
                                                                   Código documento: ########
                                 MANUAL DE INTEGRAÇÃO              Revisão: ###
                                                                   Status: ###
                                 TASY – MEDICAL RECORD
                                          DATA


6. INFORMAÇOES RELEVANTES
      6.1 Headers Obrigatórios
- Content-Type: application/json
- Accept: application/json


      6.2 Códigos de Resposta HTTP
- 200: Sucesso - Dados encontrados
- 400: Bad Request - Parâmetros inválidos
- 404: Not Found - Dados não encontrados
- 500: Internal Server Error - Erro interno do servidor


      6.3 Campos Comuns (Mapeamento Padrão)
CD_PESSOA_FISICA → patientId (ID do Paciente)
NR_ATENDIMENTO → encounterId (ID do Atendimento)
NR_IDENTIDADE → identityDocumentNumber (Número do Documento)
DT_NASCIMENTO → birthDate (Data de Nascimento)
IE_SEXO → gender (Sexo)




 Confidencial da Companhia Philips                                                Página 26 de 26
                                      CÓPIAS NÃO SÃO CONTROLADAS
