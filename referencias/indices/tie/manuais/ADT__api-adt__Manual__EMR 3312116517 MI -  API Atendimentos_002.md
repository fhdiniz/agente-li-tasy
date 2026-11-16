**API: Atendimento**

![](media/image1.jpeg)

**AVISO**

O conteúdo deste documento é de propriedade exclusiva da Philips e está sujeito a alterações sem aviso prévio.

Esta cópia deverá ser protegida contra divulgações indevidas, como cópia da documentação eletrônica, impressa ou parte dela, não deverá ser emprestada, reproduzida ou vendida.

Todos os nomes de empresas, produtos, marcas comerciais, pessoas, personagens, dados ou situações, citados neste documento são fictícios e tem somente objetivo didático.

# **Sumário**

[1 Objetivo da Integração 4](#objetivo-da-integração)

[1.1 Principais Características 4](#principais-características)

[1.2 Público 4](#público)

[2 Requisitos Necessários para a Integração 5](#requisitos-necessários-para-a-integração)

[2.1 Infraestrutura 5](#infraestrutura)

[3 Configurações e Parametrizações no Sistema 6](#configurações-e-parametrizações-no-sistema)

[3.1 Forma de Comunicação 6](#forma-de-comunicação)

[3.2 Cadastros e Parametrizações 6](#cadastros-e-parametrizações)

[3.2.1 Conector 6](#conector)

[3.2.2 Evento 7](#evento)

[3.2.3 Fluxo 7](#fluxo)

[3.2.4 Rota 8](#rota)

[3.2.5 Mapeamento 8](#_Toc129340268)

[4 Atendimento 9](#atendimento)

[4.1 Obter atendimento pelo número 9](#obter-atendimento-pelo-número)

[4.1.1 Mapeamento tags JSON 9](#mapeamento-tags-json)

[4.2 Obter atendimento pelo número externo 13](#obter-atendimento-pelo-número-externo)

[4.2.1 Mapeamento tags JSON 13](#mapeamento-tags-json-1)

[4.3 Inserir atendimento 17](#inserir-atendimento)

[4.3.1 Mapeamento tags JSON 18](#mapeamento-tags-json-2)

[4.4 Atualizar atendimento 19](#atualizar-atendimento)

[4.4.1 Mapeamento tags JSON 20](#_Toc129340277)

[5 Convênio 21](#convênio)

[5.1 Obter convênios 21](#obter-convênios)

[5.1.1 Mapeamento tags JSON 21](#mapeamento-tags-json-4)

[5.2 Obter convênio pelo número 23](#obter-convênio-pelo-número)

[5.2.1 Mapeamento tags JSON 23](#mapeamento-tags-json-5)

[5.3 Inserir convênio ao paciente 24](#inserir-convênio-ao-paciente)

[5.3.1 Mapeamento tags JSON 25](#mapeamento-tags-json-6)

[5.4 Atualizar convênio do paciente 26](#atualizar-convênio-do-paciente)

[5.4.1 Mapeamento tags JSON 27](#mapeamento-tags-json-7)

[5.5 Atualizar convênio do paciente 28](#atualizar-convênio-do-paciente-1)

[5.5.1 Mapeamento tags JSON 28](#mapeamento-tags-json-8)

[5.6 Remover convênio do paciente 30](#remover-convênio-do-paciente)

[6 Setor 31](#setor)

[6.1 Obter setores 31](#obter-setores)

[6.1.1 Mapeamento tags JSON 32](#mapeamento-tags-json-9)

[6.2 Obter setor pelo identificador 33](#obter-setor-pelo-identificador)

[6.2.1 Mapeamento tags JSON 33](#mapeamento-tags-json-10)

[6.3 Inserir setor 34](#inserir-setor)

[6.3.1 Mapeamento tags JSON 34](#mapeamento-tags-json-11)

[6.4 Atualizar setor pelo identificador 35](#atualizar-setor-pelo-identificador)

[6.4.1 Mapeamento tags JSON 35](#mapeamento-tags-json-12)

[6.5 Remover setor pelo identificador 36](#remover-setor-pelo-identificador)

# 1 Objetivo da Integração

A integração tem como objetivo obter, inserir ou alterar os dados de atendimento, convênio e setor do paciente, fazendo parte do fluxo de processamento de laudo.

![](media/image3.png)

## 1.1 Principais Características

> Automatiza a digitação dos dados nos respectivos cadastros no Tasy provenientes de sistemas terceiros.

## 1.2 Público

> Setores responsáveis pelo controle e/ou cadastro de atendimento, convênio e setores.

# 2 Requisitos Necessários para a Integração

Abaixo estão descritos os requisitos mínimos necessários em nível de infraestrutura e sistemas (Multimed, PACS – Picture Archiving and Communication System, Tasy) para que a Integração ocorra com sucesso.

## 2.1 Infraestrutura

> TIE (Tasy Interfaces Engine) e tasy-interfaces.

# 3 Configurações e Parametrizações no Sistema

Abaixo estão descritos as configurações e parametrizações necessárias em nível de sistema (Multimed, PACS, Tasy) para o funcionamento da Integração.

## 3.1 Forma de Comunicação

> A comunicação é feita utilizando o formato JSON.

## 3.2 Cadastros e Parametrizações

> Toda a parametrização da integração deve ser efetuada no TIE, incluindo conectores, eventos, fluxos, rotas e mapeamentos.

### 3.2.1 Conector

> No TIE deve ser configurado o conector conforme a orientação a abaixo.

  - General:
    
      - Name: api.ecnounterPatient

  - Source Code:  

  - Configurations:
    
      - host: 0.0.0.0
    
      - port: 9090
    
      - protocol: http

### 3.2.2 Evento

> No TIE deve ser configurado o evento conforme imagem abaixo.

![](media/image5.png)

### 3.2.3 Fluxo

> No TIE deve ser configurado o fluxo conforme abaixo.

  - General:
    
      - Name: api.encounterPatient

  - Source Code:  

  - Configurations:
    
      - host: 0.0.0.0 (endereço do tasy-interfaces)
    
      - port: 50001 (porta utilizada no tasy-interfaces)

### 3.2.4 Rota

> No TIE deve ser configurado a rota conforme imagem abaixo.

![](media/image7.png)

### 3.2.5 Mapeamento

  - integration.proton.establishment: campo “CD\_ESTABELECIMENTO” da tabela “ESTABELECIMENTO”

  - integration.proton.origin: campo “CD\_PROCEDENCIA” da tabela “PROCEDENCIA”

  - integration.proton.insurance: campo “CD\_CONVENIO” da tabela “CONVENIO”

  - integration.proton.section: campo “CD\_SETOR\_ATENDIMENTO” da tabela “SETOR\_ATENDIMENTO”

  - integration.proton.medicalDepartment: campo “CD\_DEPARTAMENTO” da tabela “DEPARTAMENTO\_MEDICO”

  - integration.proton.medicalCategory: campo “NR\_SEQUENCIA” da tabela “MEDICO\_CATEGORIA”

  - integration.proton.accommodationType: campo “CD\_TIPO\_ACOMODACAO” da tabela “TIPO\_ACOMODACAO”

# 4 Atendimento

## 4.1 Obter atendimento pelo número

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo.

  - Type: GET

  - Path: /resources/api/encounter-patient/:encounterPatientNumber

  - Params:
    
      - encounterPatientNumber: Number

![](media/image8.png)

## 4.1.1 Mapeamento tags JSON

| **TAG**                        | **TABELA**                   | **ATRIBUTO**               |
| ------------------------------ | ---------------------------- | -------------------------- |
| encounterPatientNumber         | ATENDIMENTO\_PACIENTE        | NR\_ATENDIMENTO            |
| naturalPersonCode              | ATENDIMENTO\_PACIENTE        | CD\_PESSOA\_FISICA         |
| institutionCode                | ATENDIMENTO\_PACIENTE        | CD\_ESTABELECIMENTO        |
| originCode                     | ATENDIMENTO\_PACIENTE        | CD\_PROCEDENCIA            |
| admissionDate                  | ATENDIMENTO\_PACIENTE        | DT\_ENTRADA                |
| encounterIdentifierType        | ATENDIMENTO\_PACIENTE        | IE\_TIPO\_ATENDIMENTO      |
| responsiblePhysicianCode       | ATENDIMENTO\_PACIENTE        | CD\_MEDICO\_RESP           |
| healthPlanIdentifierType       | ATENDIMENTO\_PACIENTE        | IE\_TIPO\_CONVENIO         |
| allowsVisit                    | ATENDIMENTO\_PACIENTE        | IE\_PERMITE\_VISITA        |
| waitingNumber                  | ATENDIMENTO\_PACIENTE        | NR\_SEQ\_PAC\_SENHA\_FILA  |
| personName                     | ATENDIMENTO\_PACIENTE        | NM\_PESSOA\_FISICA         |
| medicalRecordNumber            | ATENDIMENTO\_PACIENTE        | NR\_PRONTUARIO             |
| dischargeDate                  | ATENDIMENTO\_PACIENTE        | DT\_ALTA                   |
| physicianCalledDate            | ATENDIMENTO\_PACIENTE        | DT\_ATEND\_MEDICO          |
| clinicId                       | ATENDIMENTO\_PACIENTE        | IE\_CLINICA                |
| healthPlanList                 |                              |                            |
| healthPlanSeq                  | ATEND\_CATEGORIA\_CONVENIO   | NR\_SEQ\_INTERNO           |
| encounterPatientNumber         | ATEND\_CATEGORIA\_CONVENIO   | NR\_ATENDIMENTO            |
| healthPlanCode                 | ATEND\_CATEGORIA\_CONVENIO   | CD\_CONVENIO               |
| healthPlanCategoryCode         | ATEND\_CATEGORIA\_CONVENIO   | CD\_CATEGORIA              |
| vatCategoryCode                | ATEND\_CATEGORIA\_CONVENIO   | NR\_SEQ\_CATEGORIA\_IVA    |
| startVigencyDate               | ATEND\_CATEGORIA\_CONVENIO   | DT\_INICIO\_VIGENCIA       |
| finalVigencyDate               | ATEND\_CATEGORIA\_CONVENIO   | DT\_FINAL\_VIGENCIA        |
| healthPlanIdentifierDocType    | ATEND\_CATEGORIA\_CONVENIO   | IE\_TIPO\_GUIA             |
| healthPlanUserCode             | ATEND\_CATEGORIA\_CONVENIO   | CD\_USUARIO\_CONVENIO      |
| healthPlanCodePlan             | ATEND\_CATEGORIA\_CONVENIO   | CD\_PLANO\_CONVENIO        |
| healthPlanDocNumber            | ATEND\_CATEGORIA\_CONVENIO   | NR\_DOC\_CONVENIO          |
| healthPlancardValidDate        | ATEND\_CATEGORIA\_CONVENIO   | DT\_VALIDADE\_CARTEIRA     |
| inf                            |                              |                            |
| sequence                       | ATENDIMENTO\_PACIENTE\_INF   | NR\_SEQUENCIA              |
| creationDate                   | ATENDIMENTO\_PACIENTE\_INF   | DT\_ATUALIZACAO\_NREC      |
| creationUser                   | ATENDIMENTO\_PACIENTE\_INF   | NM\_USUARIO\_NREC          |
| referenceDate                  | ATENDIMENTO\_PACIENTE\_INF   | DT\_REFERENCIA             |
| encounterPatientNumber         | ATENDIMENTO\_PACIENTE\_INF   | NR\_ATENDIMENTO            |
| exists                         | ATENDIMENTO\_PACIENTE\_INF   | IE\_EXISTE                 |
| expirationDate                 | ATENDIMENTO\_PACIENTE\_INF   | DT\_VALIDADE               |
| physicianCode                  | ATENDIMENTO\_PACIENTE\_INF   | CD\_MEDICO                 |
| companyCode                    | ATENDIMENTO\_PACIENTE\_INF   | CD\_EMPRESA                |
| departmentDescription          | ATENDIMENTO\_PACIENTE\_INF   | DS\_DEPARTMENTO\_ESP       |
| fiscalId                       | ATENDIMENTO\_PACIENTE\_INF   | CD\_CGC\_INDICACAO         |
| accidentNumber                 | ATENDIMENTO\_PACIENTE\_INF   | NR\_ACIDENTE               |
| accidentDate                   | ATENDIMENTO\_PACIENTE\_INF   | DT\_ACIDENTE               |
| accidentDescription            | ATENDIMENTO\_PACIENTE\_INF   | DS\_ACIDENTE               |
| accidentTypeSequence           | ATENDIMENTO\_PACIENTE\_INF   | NR\_SEQ\_TIPO\_ACIDENTE    |
| arrivalMethodSequence          | ATENDIMENTO\_PACIENTE\_INF   | NR\_SEQ\_FORMA\_CHEGADA    |
| occurrenceCityCode             | ATENDIMENTO\_PACIENTE\_INF   | CD\_MUNICIPIO\_OCORRENCIA  |
| occurrenceDate                 | ATENDIMENTO\_PACIENTE\_INF   | DT\_OCORRENCIA             |
| rqeNumber                      | ATENDIMENTO\_PACIENTE\_INF   | NR\_RQE                    |
| bsnrNumber                     | ATENDIMENTO\_PACIENTE\_INF   | NR\_BSNR                   |
| employerFiscalId               | ATENDIMENTO\_PACIENTE\_INF   | CD\_CGC\_EMPREGADOR        |
| jobStartDate                   | ATENDIMENTO\_PACIENTE\_INF   | DT\_INICIO\_TRABALHO       |
| infoType                       | ATENDIMENTO\_PACIENTE\_INF   | IE\_TIPO\_INFORMACAO       |
| contractCode                   | ATENDIMENTO\_PACIENTE\_INF   | CD\_CONTRACT\_HOSP         |
| contractRole                   | ATENDIMENTO\_PACIENTE\_INF   | CD\_CONTRACT\_ROLE         |
| contractType                   | ATENDIMENTO\_PACIENTE\_INF   | CD\_CONTRACT\_TYPE         |
| companyDescription             | ATENDIMENTO\_PACIENTE\_INF   | DS\_EMPRESA                |
| phoneNumber                    | ATENDIMENTO\_PACIENTE\_INF   | NR\_TELEFONE               |
| employerCity                   | ATENDIMENTO\_PACIENTE\_INF   | DS\_MUNICIPIO\_EMPREG      |
| employerCep                    | ATENDIMENTO\_PACIENTE\_INF   | CD\_CEP\_EMPREG            |
| employerAddressNumber          | ATENDIMENTO\_PACIENTE\_INF   | NR\_ENDERECO\_EMPREG       |
| employerAddress                | ATENDIMENTO\_PACIENTE\_INF   | DS\_ENDERECO\_EMPREG       |
| employerCountry                | ATENDIMENTO\_PACIENTE\_INF   | DS\_PAIS\_EMPREG           |
| phoneDdi                       | ATENDIMENTO\_PACIENTE\_INF   | NR\_DDI\_TELEFONE          |
| phoneDdd                       | ATENDIMENTO\_PACIENTE\_INF   | NR\_DDD\_TELEFONE          |
| professionCode                 | ATENDIMENTO\_PACIENTE\_INF   | CD\_PROFISSAO              |
| professionDescription          | ATENDIMENTO\_PACIENTE\_INF   | DS\_PROFISSAO              |
| expirationStartDate            | ATENDIMENTO\_PACIENTE\_INF   | DT\_INICIO\_VALIDADE       |
| typeCode                       | ATENDIMENTO\_PACIENTE\_INF   | IE\_TYPE\_CODE             |
| transplantTreatment            | ATENDIMENTO\_PACIENTE\_INF   | IE\_TRAT\_TRANSPLANTE      |
| evolveCode                     | ATENDIMENTO\_PACIENTE\_INF   | CD\_EVOLUCAO               |
| hospitalizationHomeCode        | ATENDIMENTO\_PACIENTE\_INF   | CD\_PRE\_HOSP\_HOME        |
| hospitalizationRouteCode       | ATENDIMENTO\_PACIENTE\_INF   | CD\_HOSPITALIZATION\_ROUTE |
| transplant                     | ATENDIMENTO\_PACIENTE\_INF   | IE\_TRANSPLANTE            |
| externalEncounterPatientNumber | ATENDIMENTO\_PACIENTE\_INF   | NR\_ATEND\_EXTERNO         |
| attachment                     |                              |                            |
| sequence                       | ATENDIMENTO\_PACIENTE\_ANEXO | NR\_SEQUENCIA              |
| creationDate                   | ATENDIMENTO\_PACIENTE\_ANEXO | DT\_ATUALIZACAO\_NREC      |
| creationUser                   | ATENDIMENTO\_PACIENTE\_ANEXO | NM\_USUARIO\_NREC          |
| encounterPatientNumber         | ATENDIMENTO\_PACIENTE\_ANEXO | NR\_ATENDIMENTO            |
| expirationDate                 | ATENDIMENTO\_PACIENTE\_ANEXO | DT\_VALIDADE               |
| filePath                       | ATENDIMENTO\_PACIENTE\_ANEXO | DS\_ARQUIVO                |
| codePerson                     | ATENDIMENTO\_PACIENTE\_ANEXO | CD\_PESSOA\_FISICA         |
| levelAttention                 | ATENDIMENTO\_PACIENTE\_ANEXO | IE\_NIVEL\_ATENCAO         |
| deletedUser                    | ATENDIMENTO\_PACIENTE\_ANEXO | NM\_USUARIO\_EXCLUSAO      |
| deletedReason                  | ATENDIMENTO\_PACIENTE\_ANEXO | DS\_MOTIVO\_EXCLUSAO       |
| deletedData                    | ATENDIMENTO\_PACIENTE\_ANEXO | DT\_EXCLUSAO               |
| sequenceFile                   | ATENDIMENTO\_PACIENTE\_ANEXO | NR\_SEQ\_DOCUMENTO         |
| sequenceSchedule               | ATENDIMENTO\_PACIENTE\_ANEXO | NR\_SEQ\_AGEINT            |

## 4.2 Obter atendimento pelo número externo

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: GET

  - Path: /resources/api/encounter-patient/inf/:externalEncounterPatientNumber

<!-- end list -->

  - Params:
    
      - externalEncounterPatientNumber: String

![](media/image9.png)

## 4.2.1 Mapeamento tags JSON

| **TAG**                        | **TABELA**                   | **ATRIBUTO**               |
| ------------------------------ | ---------------------------- | -------------------------- |
| encounterPatientNumber         | ATENDIMENTO\_PACIENTE        | NR\_ATENDIMENTO            |
| naturalPersonCode              | ATENDIMENTO\_PACIENTE        | CD\_PESSOA\_FISICA         |
| institutionCode                | ATENDIMENTO\_PACIENTE        | CD\_ESTABELECIMENTO        |
| originCode                     | ATENDIMENTO\_PACIENTE        | CD\_PROCEDENCIA            |
| admissionDate                  | ATENDIMENTO\_PACIENTE        | DT\_ENTRADA                |
| encounterIdentifierType        | ATENDIMENTO\_PACIENTE        | IE\_TIPO\_ATENDIMENTO      |
| responsiblePhysicianCode       | ATENDIMENTO\_PACIENTE        | CD\_MEDICO\_RESP           |
| healthPlanIdentifierType       | ATENDIMENTO\_PACIENTE        | IE\_TIPO\_CONVENIO         |
| allowsVisit                    | ATENDIMENTO\_PACIENTE        | IE\_PERMITE\_VISITA        |
| waitingNumber                  | ATENDIMENTO\_PACIENTE        | NR\_SEQ\_PAC\_SENHA\_FILA  |
| personName                     | ATENDIMENTO\_PACIENTE        | NM\_PESSOA\_FISICA         |
| medicalRecordNumber            | ATENDIMENTO\_PACIENTE        | NR\_PRONTUARIO             |
| dischargeDate                  | ATENDIMENTO\_PACIENTE        | DT\_ALTA                   |
| physicianCalledDate            | ATENDIMENTO\_PACIENTE        | DT\_ATEND\_MEDICO          |
| clinicId                       | ATENDIMENTO\_PACIENTE        | IE\_CLINICA                |
| healthPlanList                 |                              |                            |
| healthPlanSeq                  | ATEND\_CATEGORIA\_CONVENIO   | NR\_SEQ\_INTERNO           |
| encounterPatientNumber         | ATEND\_CATEGORIA\_CONVENIO   | NR\_ATENDIMENTO            |
| healthPlanCode                 | ATEND\_CATEGORIA\_CONVENIO   | CD\_CONVENIO               |
| healthPlanCategoryCode         | ATEND\_CATEGORIA\_CONVENIO   | CD\_CATEGORIA              |
| vatCategoryCode                | ATEND\_CATEGORIA\_CONVENIO   | NR\_SEQ\_CATEGORIA\_IVA    |
| startVigencyDate               | ATEND\_CATEGORIA\_CONVENIO   | DT\_INICIO\_VIGENCIA       |
| finalVigencyDate               | ATEND\_CATEGORIA\_CONVENIO   | DT\_FINAL\_VIGENCIA        |
| healthPlanIdentifierDocType    | ATEND\_CATEGORIA\_CONVENIO   | IE\_TIPO\_GUIA             |
| healthPlanUserCode             | ATEND\_CATEGORIA\_CONVENIO   | CD\_USUARIO\_CONVENIO      |
| healthPlanCodePlan             | ATEND\_CATEGORIA\_CONVENIO   | CD\_PLANO\_CONVENIO        |
| healthPlanDocNumber            | ATEND\_CATEGORIA\_CONVENIO   | NR\_DOC\_CONVENIO          |
| healthPlancardValidDate        | ATEND\_CATEGORIA\_CONVENIO   | DT\_VALIDADE\_CARTEIRA     |
| inf                            |                              |                            |
| sequence                       | ATENDIMENTO\_PACIENTE\_INF   | NR\_SEQUENCIA              |
| creationDate                   | ATENDIMENTO\_PACIENTE\_INF   | DT\_ATUALIZACAO\_NREC      |
| creationUser                   | ATENDIMENTO\_PACIENTE\_INF   | NM\_USUARIO\_NREC          |
| referenceDate                  | ATENDIMENTO\_PACIENTE\_INF   | DT\_REFERENCIA             |
| encounterPatientNumber         | ATENDIMENTO\_PACIENTE\_INF   | NR\_ATENDIMENTO            |
| exists                         | ATENDIMENTO\_PACIENTE\_INF   | IE\_EXISTE                 |
| expirationDate                 | ATENDIMENTO\_PACIENTE\_INF   | DT\_VALIDADE               |
| physicianCode                  | ATENDIMENTO\_PACIENTE\_INF   | CD\_MEDICO                 |
| companyCode                    | ATENDIMENTO\_PACIENTE\_INF   | CD\_EMPRESA                |
| departmentDescription          | ATENDIMENTO\_PACIENTE\_INF   | DS\_DEPARTMENTO\_ESP       |
| fiscalId                       | ATENDIMENTO\_PACIENTE\_INF   | CD\_CGC\_INDICACAO         |
| accidentNumber                 | ATENDIMENTO\_PACIENTE\_INF   | NR\_ACIDENTE               |
| accidentDate                   | ATENDIMENTO\_PACIENTE\_INF   | DT\_ACIDENTE               |
| accidentDescription            | ATENDIMENTO\_PACIENTE\_INF   | DS\_ACIDENTE               |
| accidentTypeSequence           | ATENDIMENTO\_PACIENTE\_INF   | NR\_SEQ\_TIPO\_ACIDENTE    |
| arrivalMethodSequence          | ATENDIMENTO\_PACIENTE\_INF   | NR\_SEQ\_FORMA\_CHEGADA    |
| occurrenceCityCode             | ATENDIMENTO\_PACIENTE\_INF   | CD\_MUNICIPIO\_OCORRENCIA  |
| occurrenceDate                 | ATENDIMENTO\_PACIENTE\_INF   | DT\_OCORRENCIA             |
| rqeNumber                      | ATENDIMENTO\_PACIENTE\_INF   | NR\_RQE                    |
| bsnrNumber                     | ATENDIMENTO\_PACIENTE\_INF   | NR\_BSNR                   |
| employerFiscalId               | ATENDIMENTO\_PACIENTE\_INF   | CD\_CGC\_EMPREGADOR        |
| jobStartDate                   | ATENDIMENTO\_PACIENTE\_INF   | DT\_INICIO\_TRABALHO       |
| infoType                       | ATENDIMENTO\_PACIENTE\_INF   | IE\_TIPO\_INFORMACAO       |
| contractCode                   | ATENDIMENTO\_PACIENTE\_INF   | CD\_CONTRACT\_HOSP         |
| contractRole                   | ATENDIMENTO\_PACIENTE\_INF   | CD\_CONTRACT\_ROLE         |
| contractType                   | ATENDIMENTO\_PACIENTE\_INF   | CD\_CONTRACT\_TYPE         |
| companyDescription             | ATENDIMENTO\_PACIENTE\_INF   | DS\_EMPRESA                |
| phoneNumber                    | ATENDIMENTO\_PACIENTE\_INF   | NR\_TELEFONE               |
| employerCity                   | ATENDIMENTO\_PACIENTE\_INF   | DS\_MUNICIPIO\_EMPREG      |
| employerCep                    | ATENDIMENTO\_PACIENTE\_INF   | CD\_CEP\_EMPREG            |
| employerAddressNumber          | ATENDIMENTO\_PACIENTE\_INF   | NR\_ENDERECO\_EMPREG       |
| employerAddress                | ATENDIMENTO\_PACIENTE\_INF   | DS\_ENDERECO\_EMPREG       |
| employerCountry                | ATENDIMENTO\_PACIENTE\_INF   | DS\_PAIS\_EMPREG           |
| phoneDdi                       | ATENDIMENTO\_PACIENTE\_INF   | NR\_DDI\_TELEFONE          |
| phoneDdd                       | ATENDIMENTO\_PACIENTE\_INF   | NR\_DDD\_TELEFONE          |
| professionCode                 | ATENDIMENTO\_PACIENTE\_INF   | CD\_PROFISSAO              |
| professionDescription          | ATENDIMENTO\_PACIENTE\_INF   | DS\_PROFISSAO              |
| expirationStartDate            | ATENDIMENTO\_PACIENTE\_INF   | DT\_INICIO\_VALIDADE       |
| typeCode                       | ATENDIMENTO\_PACIENTE\_INF   | IE\_TYPE\_CODE             |
| transplantTreatment            | ATENDIMENTO\_PACIENTE\_INF   | IE\_TRAT\_TRANSPLANTE      |
| evolveCode                     | ATENDIMENTO\_PACIENTE\_INF   | CD\_EVOLUCAO               |
| hospitalizationHomeCode        | ATENDIMENTO\_PACIENTE\_INF   | CD\_PRE\_HOSP\_HOME        |
| hospitalizationRouteCode       | ATENDIMENTO\_PACIENTE\_INF   | CD\_HOSPITALIZATION\_ROUTE |
| transplant                     | ATENDIMENTO\_PACIENTE\_INF   | IE\_TRANSPLANTE            |
| externalEncounterPatientNumber | ATENDIMENTO\_PACIENTE\_INF   | NR\_ATEND\_EXTERNO         |
| attachment                     |                              |                            |
| sequence                       | ATENDIMENTO\_PACIENTE\_ANEXO | NR\_SEQUENCIA              |
| creationDate                   | ATENDIMENTO\_PACIENTE\_ANEXO | DT\_ATUALIZACAO\_NREC      |
| creationUser                   | ATENDIMENTO\_PACIENTE\_ANEXO | NM\_USUARIO\_NREC          |
| encounterPatientNumber         | ATENDIMENTO\_PACIENTE\_ANEXO | NR\_ATENDIMENTO            |
| expirationDate                 | ATENDIMENTO\_PACIENTE\_ANEXO | DT\_VALIDADE               |
| filePath                       | ATENDIMENTO\_PACIENTE\_ANEXO | DS\_ARQUIVO                |
| codePerson                     | ATENDIMENTO\_PACIENTE\_ANEXO | CD\_PESSOA\_FISICA         |
| levelAttention                 | ATENDIMENTO\_PACIENTE\_ANEXO | IE\_NIVEL\_ATENCAO         |
| deletedUser                    | ATENDIMENTO\_PACIENTE\_ANEXO | NM\_USUARIO\_EXCLUSAO      |
| deletedReason                  | ATENDIMENTO\_PACIENTE\_ANEXO | DS\_MOTIVO\_EXCLUSAO       |
| deletedData                    | ATENDIMENTO\_PACIENTE\_ANEXO | DT\_EXCLUSAO               |
| sequenceFile                   | ATENDIMENTO\_PACIENTE\_ANEXO | NR\_SEQ\_DOCUMENTO         |
| sequenceSchedule               | ATENDIMENTO\_PACIENTE\_ANEXO | NR\_SEQ\_AGEINT            |

## 4.3 Inserir atendimento

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: POST

  - Path: /resources/api/encounter-patient

  - Body ( Raw JSON ):

> {
> 
> "naturalPersonCode": "Number",
> 
> "institutionCode": "Number",
> 
> "originCode": "Number",
> 
> "admissionDate": "yyyy-mm-dd",
> 
> "encounterIdentifierType": "Number",
> 
> "responsiblePhysicianCode": "Number",
> 
> "healthPlanIdentifierType": "Number",
> 
> "allowsVisit": "String",
> 
> "externalEncounterPatientNumber": "String",
> 
> "patientScheduleSequences": \["Number"\],
> 
> "filePath": "String"
> 
> }

![](media/image10.png)

## 4.3.1 Mapeamento tags JSON

| **TAG**                        | **TABELA**                   | **ATRIBUTO**          |
| ------------------------------ | ---------------------------- | --------------------- |
| naturalPersonCode              | ATENDIMENTO\_PACIENTE        | CD\_PESSOA\_FISICA    |
| institutionCode                | ATENDIMENTO\_PACIENTE        | CD\_ESTABELECIMENTO   |
| originCode                     | ATENDIMENTO\_PACIENTE        | CD\_PROCEDENCIA       |
| admissionDate                  | ATENDIMENTO\_PACIENTE        | DT\_ENTRADA           |
| encounterIdentifierType        | ATENDIMENTO\_PACIENTE        | IE\_TIPO\_ATENDIMENTO |
| responsiblePhysicianCode       | ATENDIMENTO\_PACIENTE        | CD\_MEDICO\_RESP      |
| healthPlanIdentifierType       | ATENDIMENTO\_PACIENTE        | IE\_TIPO\_CONVENIO    |
| allowsVisit                    | ATENDIMENTO\_PACIENTE        | IE\_PERMITE\_VISITA   |
| physicianCalledDate            | ATENDIMENTO\_PACIENTE        | DT\_ATEND\_MEDICO     |
| externalEncounterPatientNumber | ATENDIMENTO\_PACIENTE\_INF   | NR\_ATEND\_EXTERNO    |
| filePath                       | ATENDIMENTO\_PACIENTE\_ANEXO | DS\_ARQUIVO           |

## 

## 4.4 Atualizar atendimento

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: PUT

  - Path: /resources/api/encounter-patient

  - Params:
    
      - encounterPatientNumber: Number

  - Body ( Raw JSON ):

> {
> 
> "naturalPersonCode": "Number",
> 
> "institutionCode": "Number",
> 
> "originCode": "Number",
> 
> "admissionDate": "yyyy-mm-dd",
> 
> "encounterIdentifierType": "Number",
> 
> "responsiblePhysicianCode": "Number",
> 
> "healthPlanIdentifierType": "Number",
> 
> "allowsVisit": "String",
> 
> "externalEncounterPatientNumber": "String",
> 
> "patientScheduleSequences": \["Number"\],
> 
> "filePath": "String"
> 
> }

![](media/image11.png)

## 

## 4.4.1 Mapeamento tags JSON

| **TAG**                        | **TABELA**                   | **ATRIBUTO**          |
| ------------------------------ | ---------------------------- | --------------------- |
| naturalPersonCode              | ATENDIMENTO\_PACIENTE        | CD\_PESSOA\_FISICA    |
| institutionCode                | ATENDIMENTO\_PACIENTE        | CD\_ESTABELECIMENTO   |
| originCode                     | ATENDIMENTO\_PACIENTE        | CD\_PROCEDENCIA       |
| admissionDate                  | ATENDIMENTO\_PACIENTE        | DT\_ENTRADA           |
| encounterIdentifierType        | ATENDIMENTO\_PACIENTE        | IE\_TIPO\_ATENDIMENTO |
| responsiblePhysicianCode       | ATENDIMENTO\_PACIENTE        | CD\_MEDICO\_RESP      |
| healthPlanIdentifierType       | ATENDIMENTO\_PACIENTE        | IE\_TIPO\_CONVENIO    |
| allowsVisit                    | ATENDIMENTO\_PACIENTE        | IE\_PERMITE\_VISITA   |
| physicianCalledDate            | ATENDIMENTO\_PACIENTE        | DT\_ATEND\_MEDICO     |
| externalEncounterPatientNumber | ATENDIMENTO\_PACIENTE\_INF   | NR\_ATEND\_EXTERNO    |
| filePath                       | ATENDIMENTO\_PACIENTE\_ANEXO | DS\_ARQUIVO           |

# 5 Convênio

## 5.1 Obter convênios

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: GET

  - Path: /resources/api/encounter-patient/health-plan

  - Params:
    
      - encounter-patient-number: Number
    
      - health-plan-code: Number
    
      - health-plan-category-code: Number
    
      - start-vigency-date: yyyy-mm-dd

![](media/image12.png)

## 5.1.1 Mapeamento tags JSON

| **TAG**                     | **TABELA**                 | **ATRIBUTO**            |
| --------------------------- | -------------------------- | ----------------------- |
| healthPlanSeq               | ATEND\_CATEGORIA\_CONVENIO | NR\_SEQ\_INTERNO        |
| encounterPatientNumber      | ATEND\_CATEGORIA\_CONVENIO | NR\_ATENDIMENTO         |
| healthPlanCode              | ATEND\_CATEGORIA\_CONVENIO | CD\_CONVENIO            |
| healthPlanCategoryCode      | ATEND\_CATEGORIA\_CONVENIO | CD\_CATEGORIA           |
| vatCategoryCode             | ATEND\_CATEGORIA\_CONVENIO | NR\_SEQ\_CATEGORIA\_IVA |
| startVigencyDate            | ATEND\_CATEGORIA\_CONVENIO | DT\_INICIO\_VIGENCIA    |
| finalVigencyDate            | ATEND\_CATEGORIA\_CONVENIO | DT\_FINAL\_VIGENCIA     |
| healthPlanIdentifierDocType | ATEND\_CATEGORIA\_CONVENIO | IE\_TIPO\_GUIA          |
| healthPlanUserCode          | ATEND\_CATEGORIA\_CONVENIO | CD\_USUARIO\_CONVENIO   |
| healthPlanCodePlan          | ATEND\_CATEGORIA\_CONVENIO | CD\_PLANO\_CONVENIO     |
| healthPlanDocNumber         | ATEND\_CATEGORIA\_CONVENIO | NR\_DOC\_CONVENIO       |
| healthPlancardValidDate     | ATEND\_CATEGORIA\_CONVENIO | DT\_VALIDADE\_CARTEIRA  |

## 5.2 Obter convênio pelo número

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: GET

  - Path: /resources/api/encounter-patient/health-plan/:encounterPatientNumber

  - Params:
    
      - encounterPatientNumber: Number

![](media/image13.png)

## 5.2.1 Mapeamento tags JSON

| **TAG**                     | **TABELA**                 | **ATRIBUTO**           |
| --------------------------- | -------------------------- | ---------------------- |
| healthPlanSeq               | ATEND\_CATEGORIA\_CONVENIO | NR\_SEQ\_INTERNO       |
| encounterPatientNumber      | ATEND\_CATEGORIA\_CONVENIO | NR\_ATENDIMENTO        |
| healthPlanCode              | ATEND\_CATEGORIA\_CONVENIO | CD\_CONVENIO           |
| healthPlanCategoryCode      | ATEND\_CATEGORIA\_CONVENIO | CD\_CATEGORIA          |
| startVigencyDate            | ATEND\_CATEGORIA\_CONVENIO | DT\_INICIO\_VIGENCIA   |
| finalVigencyDate            | ATEND\_CATEGORIA\_CONVENIO | DT\_FINAL\_VIGENCIA    |
| healthPlanIdentifierDocType | ATEND\_CATEGORIA\_CONVENIO | IE\_TIPO\_GUIA         |
| healthPlanUserCode          | ATEND\_CATEGORIA\_CONVENIO | CD\_USUARIO\_CONVENIO  |
| healthPlanCodePlan          | ATEND\_CATEGORIA\_CONVENIO | CD\_PLANO\_CONVENIO    |
| healthPlanDocNumber         | ATEND\_CATEGORIA\_CONVENIO | NR\_DOC\_CONVENIO      |
| healthPlancardValidDate     | ATEND\_CATEGORIA\_CONVENIO | DT\_VALIDADE\_CARTEIRA |

## 5.3 Inserir convênio ao paciente

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: POST

  - Path: /resources/api/encounter-patient/health-plan

  - Body ( Raw JSON ):

> {
> 
> "healthPlanSeq": "Number",
> 
> "encounterPatientNumber": "Number",
> 
> "healthPlanCode": "Number",
> 
> "healthPlanCategoryCode": "Number",
> 
> "startVigencyDate": "yyyy-mm-dd",
> 
> "finalVigencyDate": "yyyy-mm-dd",
> 
> "healthPlanIdentifierDocType": "String",
> 
> "healthPlanUserCode": "Number",
> 
> "healthPlanCodePlan": "Number",
> 
> "healthPlanDocNumber": "Number"
> 
> }

![](media/image14.png)

## 5.3.1 Mapeamento tags JSON

| **TAG**                     | **TABELA**                 | **ATRIBUTO**          |
| --------------------------- | -------------------------- | --------------------- |
| healthPlanSeq               | ATEND\_CATEGORIA\_CONVENIO | NR\_SEQ\_INTERNO      |
| encounterPatientNumber      | ATEND\_CATEGORIA\_CONVENIO | NR\_ATENDIMENTO       |
| healthPlanCode              | ATEND\_CATEGORIA\_CONVENIO | CD\_CONVENIO          |
| healthPlanCategoryCode      | ATEND\_CATEGORIA\_CONVENIO | CD\_CATEGORIA         |
| startVigencyDate            | ATEND\_CATEGORIA\_CONVENIO | DT\_INICIO\_VIGENCIA  |
| finalVigencyDate            | ATEND\_CATEGORIA\_CONVENIO | DT\_FINAL\_VIGENCIA   |
| healthPlanIdentifierDocType | ATEND\_CATEGORIA\_CONVENIO | IE\_TIPO\_GUIA        |
| healthPlanUserCode          | ATEND\_CATEGORIA\_CONVENIO | CD\_USUARIO\_CONVENIO |
| healthPlanCodePlan          | ATEND\_CATEGORIA\_CONVENIO | CD\_PLANO\_CONVENIO   |
| healthPlanDocNumber         | ATEND\_CATEGORIA\_CONVENIO | NR\_DOC\_CONVENIO     |

## 5.4 Atualizar convênio do paciente

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: PUT

  - Path: /resources/api/encounter-patient/health-plan

  - Params:
    
      - encounter-patient-number: Number
    
      - health-plan-code: Number
    
      - health-plan-category-code: Number
    
      - start-vigency-date: yyyy-mm-dd

  - Body ( Raw JSON ):

> {
> 
> "encounterPatientNumber": "Number",
> 
> "healthPlanCode": "Number",
> 
> "healthPlanCategoryCode": "Number",
> 
> "startVigencyDate": "yyyy-mm-dd",
> 
> "finalVigencyDate": "yyyy-mm-dd",
> 
> "healthPlanIdentifierDocType": "String",
> 
> "healthPlanUserCode": "Number",
> 
> "healthPlanCodePlan": "Number",
> 
> "healthPlanDocNumber": "Number"
> 
> }

![](media/image15.png)

## 5.4.1 Mapeamento tags JSON

| **TAG**                     | **TABELA**                 | **ATRIBUTO**          |
| --------------------------- | -------------------------- | --------------------- |
| encounterPatientNumber      | ATEND\_CATEGORIA\_CONVENIO | NR\_ATENDIMENTO       |
| healthPlanCode              | ATEND\_CATEGORIA\_CONVENIO | CD\_CONVENIO          |
| healthPlanCategoryCode      | ATEND\_CATEGORIA\_CONVENIO | CD\_CATEGORIA         |
| startVigencyDate            | ATEND\_CATEGORIA\_CONVENIO | DT\_INICIO\_VIGENCIA  |
| finalVigencyDate            | ATEND\_CATEGORIA\_CONVENIO | DT\_FINAL\_VIGENCIA   |
| healthPlanIdentifierDocType | ATEND\_CATEGORIA\_CONVENIO | IE\_TIPO\_GUIA        |
| healthPlanUserCode          | ATEND\_CATEGORIA\_CONVENIO | CD\_USUARIO\_CONVENIO |
| healthPlanCodePlan          | ATEND\_CATEGORIA\_CONVENIO | CD\_PLANO\_CONVENIO   |
| healthPlanDocNumber         | ATEND\_CATEGORIA\_CONVENIO | NR\_DOC\_CONVENIO     |

## 

## 5.5 Atualizar convênio do paciente

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: PUT

  - Path: /resources/api/encounter-patient/health-plan/:healthPlanSeq

  - Params:
    
      - healthPlanSeq: Number

  - Body ( Raw JSON ):

> {
> 
> "encounterPatientNumber": "Number",
> 
> "healthPlanCode": "Number",
> 
> "healthPlanCategoryCode": "Number",
> 
> "startVigencyDate": "yyyy-mm-dd",
> 
> "finalVigencyDate": "yyyy-mm-dd",
> 
> "healthPlanIdentifierDocType": "String",
> 
> "healthPlanUserCode": "Number",
> 
> "healthPlanCodePlan": "Number",
> 
> "healthPlanDocNumber": "Number"
> 
> }

![](media/image16.png)

## 5.5.1 Mapeamento tags JSON

| **TAG**                     | **TABELA**                 | **ATRIBUTO**          |
| --------------------------- | -------------------------- | --------------------- |
| encounterPatientNumber      | ATEND\_CATEGORIA\_CONVENIO | NR\_ATENDIMENTO       |
| healthPlanCode              | ATEND\_CATEGORIA\_CONVENIO | CD\_CONVENIO          |
| healthPlanCategoryCode      | ATEND\_CATEGORIA\_CONVENIO | CD\_CATEGORIA         |
| startVigencyDate            | ATEND\_CATEGORIA\_CONVENIO | DT\_INICIO\_VIGENCIA  |
| finalVigencyDate            | ATEND\_CATEGORIA\_CONVENIO | DT\_FINAL\_VIGENCIA   |
| healthPlanIdentifierDocType | ATEND\_CATEGORIA\_CONVENIO | IE\_TIPO\_GUIA        |
| healthPlanUserCode          | ATEND\_CATEGORIA\_CONVENIO | CD\_USUARIO\_CONVENIO |
| healthPlanCodePlan          | ATEND\_CATEGORIA\_CONVENIO | CD\_PLANO\_CONVENIO   |
| healthPlanDocNumber         | ATEND\_CATEGORIA\_CONVENIO | NR\_DOC\_CONVENIO     |

## 5.6 Remover convênio do paciente

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: DELETE

  - Path: /resources/api/encounter-patient/health-plan/:healthPlanSeq

  - Params:
    
      - healthPlanSeq

![](media/image17.png)

# 6 Setor

## 6.1 Obter setores

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: GET

  - Path: /resources/api/encounter-patient/section

  - Params:
    
      - patient-number
    
      - admission-date
    
      - section-code
    
      - department-code
    
      - accommodation-type-code
    
      - departure-date
    
      - page
    
      - maxResults

![](media/image18.png)

##   
6.1.1 Mapeamento tags JSON

| **TAG**               | **TABELA**               | **ATRIBUTO**           |
| --------------------- | ------------------------ | ---------------------- |
| id                    | ATEND\_PACIENTE\_UNIDADE | NR\_SEQ\_INTERNO       |
| sequence              | ATEND\_PACIENTE\_UNIDADE | NR\_SEQUENCIA          |
| encounterNumber       | ATEND\_PACIENTE\_UNIDADE | NR\_ATENDIMENTO        |
| sectionCode           | ATEND\_PACIENTE\_UNIDADE | CD\_SETOR\_ATENDIMENTO |
| departmentCode        | ATEND\_PACIENTE\_UNIDADE | CD\_DEPARTAMENTO       |
| baseUnitCode          | ATEND\_PACIENTE\_UNIDADE | CD\_UNIDADE\_BASICA    |
| complementaryUnitCode | ATEND\_PACIENTE\_UNIDADE | CD\_UNIDADE\_COMPL     |
| accommodationTypeCode | ATEND\_PACIENTE\_UNIDADE | CD\_TIPO\_ACOMODACAO   |
| admissionDate         | ATEND\_PACIENTE\_UNIDADE | DT\_ENTRADA\_UNIDADE   |
| departureDate         | ATEND\_PACIENTE\_UNIDADE | DT\_SAIDA\_UNIDADE     |
| companionAmount       | ATEND\_PACIENTE\_UNIDADE | NR\_ACOMPANHANTE       |
| notes                 | ATEND\_PACIENTE\_UNIDADE | DS\_OBSERVACAO         |
| sectorDescription     | ATEND\_PACIENTE\_UNIDADE | DS\_SETOR\_ATENDIMENTO |
| accommodationType     | ATEND\_PACIENTE\_UNIDADE | DS\_TIPO\_ACOMODACAO   |

## 6.2 Obter setor pelo identificador

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: GET

  - Path: /resources/api/encounter-patient/section/:id

  - Params:
    
      - id: Number

![](media/image19.png)

## 6.2.1 Mapeamento tags JSON

| **TAG**               | **TABELA**               | **ATRIBUTO**           |
| --------------------- | ------------------------ | ---------------------- |
| id                    | ATEND\_PACIENTE\_UNIDADE | NR\_SEQ\_INTERNO       |
| sequence              | ATEND\_PACIENTE\_UNIDADE | NR\_SEQUENCIA          |
| encounterNumber       | ATEND\_PACIENTE\_UNIDADE | NR\_ATENDIMENTO        |
| sectionCode           | ATEND\_PACIENTE\_UNIDADE | CD\_SETOR\_ATENDIMENTO |
| departmentCode        | ATEND\_PACIENTE\_UNIDADE | CD\_DEPARTAMENTO       |
| baseUnitCode          | ATEND\_PACIENTE\_UNIDADE | CD\_UNIDADE\_BASICA    |
| complementaryUnitCode | ATEND\_PACIENTE\_UNIDADE | CD\_UNIDADE\_COMPL     |
| accommodationTypeCode | ATEND\_PACIENTE\_UNIDADE | CD\_TIPO\_ACOMODACAO   |
| admissionDate         | ATEND\_PACIENTE\_UNIDADE | DT\_ENTRADA\_UNIDADE   |
| departureDate         | ATEND\_PACIENTE\_UNIDADE | DT\_SAIDA\_UNIDADE     |
| companionAmount       | ATEND\_PACIENTE\_UNIDADE | NR\_ACOMPANHANTE       |
| notes                 | ATEND\_PACIENTE\_UNIDADE | DS\_OBSERVACAO         |
| sectorDescription     | ATEND\_PACIENTE\_UNIDADE | DS\_SETOR\_ATENDIMENTO |
| accommodationType     | ATEND\_PACIENTE\_UNIDADE | DS\_TIPO\_ACOMODACAO   |

## 6.3 Inserir setor

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: POST

  - Path: / resources/api/encounter-patient/section

  - Body ( Raw JSON ):

> {
> 
> "patientNumber": "Number",
> 
> "sectionCode": "Number",
> 
> "departmentCode": "Number",
> 
> "accommodationTypeCode": "Number",
> 
> "baseUnitCode": "String",
> 
> "complementaryUnitCode": "String",
> 
> "admissionDate": "yyyy-mm-dd ",
> 
> "departureDate": "yyyy-mm-dd ",
> 
> "companionAmount": "Number",
> 
> "notes": "String"
> 
> }

## 6.3.1 Mapeamento tags JSON

| **TAG**               | **TABELA**               | **ATRIBUTO**           |
| --------------------- | ------------------------ | ---------------------- |
| patientNumber         | ATEND\_PACIENTE\_UNIDADE | NR\_ATENDIMENTO        |
| sectionCode           | ATEND\_PACIENTE\_UNIDADE | CD\_SETOR\_ATENDIMENTO |
| departmentCode        | ATEND\_PACIENTE\_UNIDADE | CD\_DEPARTAMENTO       |
| accommodationTypeCode | ATEND\_PACIENTE\_UNIDADE | CD\_TIPO\_ACOMODACAO   |
| baseUnitCode          | ATEND\_PACIENTE\_UNIDADE | CD\_UNIDADE\_BASICA    |
| complementaryUnitCode | ATEND\_PACIENTE\_UNIDADE | CD\_UNIDADE\_COMPL     |
| admissionDate         | ATEND\_PACIENTE\_UNIDADE | DT\_ENTRADA\_UNIDADE   |
| departureDate         | ATEND\_PACIENTE\_UNIDADE | DT\_SAIDA\_UNIDADE     |
| companionAmount       | ATEND\_PACIENTE\_UNIDADE | NR\_ACOMPANHANTE       |
| notes                 | ATEND\_PACIENTE\_UNIDADE | DS\_OBSERVACAO         |

## 6.4 Atualizar setor pelo identificador

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: PUT

  - Path: /resources/api/encounter-patient/section/:id

  - Params:
    
      - id: Number

  - Body ( Raw JSON ):

> {
> 
> "sectionCode": "Number",
> 
> "departmentCode": "Number",
> 
> "accommodationTypeCode": "Number",
> 
> "baseUnitCode": "String",
> 
> "complementaryUnitCode": "String",
> 
> "admissionDate": "yyyy-mm-dd ",
> 
> "departureDate": "yyyy-mm-dd ",
> 
> "companionAmount": "Number",
> 
> "notes": "String"
> 
> }

## 6.4.1 Mapeamento tags JSON

| **TAG**               | **TABELA**               | **ATRIBUTO**           |
| --------------------- | ------------------------ | ---------------------- |
| patientNumber         | ATEND\_PACIENTE\_UNIDADE | NR\_ATENDIMENTO        |
| sectionCode           | ATEND\_PACIENTE\_UNIDADE | CD\_SETOR\_ATENDIMENTO |
| departmentCode        | ATEND\_PACIENTE\_UNIDADE | CD\_DEPARTAMENTO       |
| accommodationTypeCode | ATEND\_PACIENTE\_UNIDADE | CD\_TIPO\_ACOMODACAO   |
| baseUnitCode          | ATEND\_PACIENTE\_UNIDADE | CD\_UNIDADE\_BASICA    |
| complementaryUnitCode | ATEND\_PACIENTE\_UNIDADE | CD\_UNIDADE\_COMPL     |
| admissionDate         | ATEND\_PACIENTE\_UNIDADE | DT\_ENTRADA\_UNIDADE   |
| departureDate         | ATEND\_PACIENTE\_UNIDADE | DT\_SAIDA\_UNIDADE     |
| companionAmount       | ATEND\_PACIENTE\_UNIDADE | NR\_ACOMPANHANTE       |
| notes                 | ATEND\_PACIENTE\_UNIDADE | DS\_OBSERVACAO         |

## 6.5 Remover setor pelo identificador

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: DELETE

  - Path: / resources/api/encounter-patient/section/:id

  - Params:
    
      - Id: Number
