**API Catraca**

![](media/image1.jpg)

**AVISO**

O conteúdo deste documento é de propriedade exclusiva da Philips e está sujeito a alterações sem aviso prévio.

Esta cópia deverá ser protegida contra divulgações indevidas, como cópia da documentação eletrônica, impressa ou parte dela, não deverá ser emprestada, reproduzida ou vendida.

Todos os nomes de empresas, produtos, marcas comerciais, pessoas, personagens, dados ou situações, citados neste documento são fictícios e tem somente objetivo didático.

# Sumário

[Sumário 2](#sumário)

[1 Objetivo da Integração 3](#objetivo-da-integração)

[1.1 Principais Características 3](#principais-características)

[1.2 Público 3](#público)

[2 Requisitos Necessários para a Integração 4](#requisitos-necessários-para-a-integração)

[2.1 Infraestrutura 4](#infraestrutura)

[3 Configurações e Parametrizações no Sistema 5](#configurações-e-parametrizações-no-sistema)

[3.1 Forma de Comunicação 5](#forma-de-comunicação)

[3.2 Cadastros e Parametrizações 5](#cadastros-e-parametrizações)

[3.2.1 Conector 5](#conector)

[3.2.2 Evento 6](#evento)

[3.2.3 Fluxo 6](#fluxo)

[3.2.4 Rota 8](#rota)

[3.2.5 Transformação 8](#transformação)

[4 Catraca 10](#catraca)

[4.1 Enviar Request 10](#enviar-request)

[4.2 Atualizar ação da Catraca 12](#atualizar-ação-da-catraca)

# 1 Objetivo da Integração

A integração tem como objetivo requisitar a liberação de acesso.

## 1.1 Principais Características

> Automatiza a digitação dos dados para liberação de acesso no sistema terceiro.

## 1.2 Público

> Setores responsáveis pelo controle de visitas.

# 2 Requisitos Necessários para a Integração

Abaixo estão descritos os requisitos mínimos necessários a nível de infraestrutura e sistemas (Multimed, PACS - Picture Archiving and Communication System, Tasy) para que a Integração ocorra com sucesso.

## 2.1 Infraestrutura

> TIE (Tasy Interfaces Engine), Tasy e tasy-interfaces.

# 3 Configurações e Parametrizações no Sistema

Abaixo estão descritos as configurações e parametrizações necessárias a nível de sistema (Multimed, PACS, Tasy) para o funcionamento da Integração.

## 3.1 Forma de Comunicação

> A comunicação é feita utilizando o formato JSON.

## 3.2 Cadastros e Parametrizações

> Toda a parametrização da integração deve ser efetuada no TIE, incluindo conectores, eventos, fluxos, rotas, mapeamentos e transformações.

### 3.2.1 Conector

> No TIE deve ser configurado o conector conforme a orientação abaixo.

  - General:
    
      - Name: api.forponto

  - Source Code:  
    ![](media/image3.png)

  - Configurations:
    
      - host: 0.0.0.0
    
      - port: 9090
    
      - protocol: http
    
      - Methods: PUT
    
      - Path: api/turnstile

### 3.2.2 Evento

> No TIE deve ser configurado os eventos conforme imagem abaixo.

![](media/image4.png)

![](media/image5.png)

### 3.2.3 Fluxo

> No TIE deve ser configurado os fluxos conforme abaixo.

  - General:
    
      - Name: api.forponto

  - Source Code:  
    ![](media/image6.png)

  - Configurations:
    
      - host: 0.0.0.0 (endereço do tasy-interfaces)
    
      - port: 50001 (porta utilizada no tasy-interfaces)

  - General:
    
      - Name: forponto.send.request

  - Source Code:  
    ![](media/image7.png)

  - Configurations:
    
      - uri:

### 3.2.4 Rota

> No TIE deve ser configurado as rotas conforme imagem abaixo.

![](media/image8.png) 

![](media/image9.png)

### 3.2.5 Transformação

> No TIE deve ser configurado os mappings conforme abaixo.

  - General:
    
      - integration.forponto.type

> ![](media/image10.png)

  - Mapping Table:  
    ![](media/image11.png)
    
      - Nos campos “Input Value” deve ser preenchido o valor que será enviado internamente ao chamar a API.

  - General:
    
      - integration.forponto.guestType

> ![](media/image12.png)

  - Mapping Table:  
    ![](media/image13.png)
    
      - Nos campos “Input Value” deve ser preenchido o valor que será enviado internamente ao chamar a API.

# 4 Catraca

## 4.1 Enviar Request

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: POST

  - Path: /api/cross/schedule

  - Headers:
    
      - BifrostMessageEvent **(Obrigatório**): forponto.send.request
    
      - BifrostMessageType **(Obrigatório)**: sync

  - Body ( Raw JSON ):
    
      - companyCode;
    
      - naturalPersonCode;
    
      - sectionCode;
    
      - notes;
    
      - lastUpdatedDate;
    
      - lastUpdatedNrecDate;
    
      - entryDate;
    
      - accurateEntryDate;
    
      - accessReleaseDate;
    
      - birthDate;
    
      - departureDate;
    
      - accurateDepartureDate;
    
      - genderCode;
    
      - lastUpdatedBy;
    
      - lastUpdatedNrecBy;
    
      - departureBy;
    
      - guestName;
    
      - encounterNumber;
    
      - accessControlNumber;
    
      - phoneDd;
    
      - civilId;
    
      - controlNumber;
    
      - typeNumber;
    
      - phoneNumber;
    
      - guestType;
    
      - action;

![](media/image14.png)

## 4.2 Atualizar ação da Catraca

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo:

  - Type: PUT

  - Path: /api/turnstile/update-action

  - Parâmetros:
    
      - type **(Obrigatório):** Tipo de entrada
        
          - Valores aceitos conforme “Input Value” informados no mapping **integration.forponto.type**
    
      - nameTag
    
      - guestType **(Obrigatório):** Tipo de visita
        
          - Valores aceitos conforme “Input Value” informados no mapping **integration.forponto.guestType**
    
      - actionDate (**Obrigatório):** Data da ação
    
      - **Deve ser informado no mínimo um dos parâmetros a seguir, um sendo informado, o outro torna-se opcional:**
        
          - accessControlNumber: Número do controle de acesso
        
          - nameTag: Crachá

![](media/image15.png)

# 5 Tabelas

> Abaixo a tabela com o relacionamento entre os campos da API de envio de informações com os campos das tabelas:

<table>
<thead>
<tr class="header">
<th><blockquote>
<p><strong>Campos API</strong></p>
</blockquote></th>
<th><blockquote>
<p><strong>ATENDIMENTO_VISITA</strong></p>
</blockquote></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><blockquote>
<p> </p>
</blockquote></td>
<td><blockquote>
<p> </p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>companyCode</p>
</blockquote></td>
<td><blockquote>
<p>cd_empresa</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>naturalPersonCode</p>
</blockquote></td>
<td><blockquote>
<p>cd_pessoa_fisica</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>sectionCode</p>
</blockquote></td>
<td><blockquote>
<p>cd_setor_atendimento</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>notes</p>
</blockquote></td>
<td><blockquote>
<p>ds_observacao</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>lastUpdatedDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_atualizacao</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>lastUpdatedNrecDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_atualizacao_nrec</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>entryDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_entrada</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>accurateEntryDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_entrada_real</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>accessReleaseDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_liberacao_acesso</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>birthDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_nascimento</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>departureDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_saida</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>accurateDepartureDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_saida_real</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>genderCode</p>
</blockquote></td>
<td><blockquote>
<p>ie_sexo</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>lastUpdatedBy</p>
</blockquote></td>
<td><blockquote>
<p>nm_usuario</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>lastUpdatedNrecBy</p>
</blockquote></td>
<td><blockquote>
<p>nm_usuario_nrec</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>departureBy</p>
</blockquote></td>
<td><blockquote>
<p>nm_usuario_saida</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>guestName</p>
</blockquote></td>
<td><blockquote>
<p>nm_visitante</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>encounterNumber</p>
</blockquote></td>
<td><blockquote>
<p>nr_atendimento</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>accessControlNumber</p>
</blockquote></td>
<td><blockquote>
<p>nr_controle_acesso</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>phoneDd</p>
</blockquote></td>
<td><blockquote>
<p>nr_ddi_telefone</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>civilId</p>
</blockquote></td>
<td><blockquote>
<p>nr_identidade</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>controlNumber</p>
</blockquote></td>
<td><blockquote>
<p>nr_seq_controle</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>typeNumber</p>
</blockquote></td>
<td><blockquote>
<p>nr_seq_tipo</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>phoneNumber</p>
</blockquote></td>
<td><blockquote>
<p>nr_telefone</p>
</blockquote></td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr class="header">
<th><blockquote>
<p><strong>Campos API</strong></p>
</blockquote></th>
<th><blockquote>
<p><strong>ATENDIMENTO_ACOMPANHANTE</strong></p>
</blockquote></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><blockquote>
<p> </p>
</blockquote></td>
<td><blockquote>
<p> </p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>companyCode</p>
</blockquote></td>
<td><blockquote>
<p> </p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>naturalPersonCode</p>
</blockquote></td>
<td><blockquote>
<p>cd_pessoa_fisica</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>sectionCode</p>
</blockquote></td>
<td><blockquote>
<p> </p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>notes</p>
</blockquote></td>
<td><blockquote>
<p>ds_observacao</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>lastUpdatedDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_atualizacao</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>lastUpdatedNrecDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_atualizacao_nrec</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>entryDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_acompanhante</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>accurateEntryDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_entrada_real</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>accessReleaseDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_liberacao_acesso</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>birthDate</p>
</blockquote></td>
<td><blockquote>
<p> </p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>departureDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_saida</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>accurateDepartureDate</p>
</blockquote></td>
<td><blockquote>
<p>dt_saida_real</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>genderCode</p>
</blockquote></td>
<td><blockquote>
<p> </p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>lastUpdatedBy</p>
</blockquote></td>
<td><blockquote>
<p>nm_usuario</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>lastUpdatedNrecBy</p>
</blockquote></td>
<td><blockquote>
<p>nm_usuario_nrec</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>departureBy</p>
</blockquote></td>
<td><blockquote>
<p>nm_usuario_saida</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>guestName</p>
</blockquote></td>
<td><blockquote>
<p>nm_acompanhante</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>encounterNumber</p>
</blockquote></td>
<td><blockquote>
<p>nr_atendimento</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>accessControlNumber</p>
</blockquote></td>
<td><blockquote>
<p>nr_controle_acesso</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>phoneDd</p>
</blockquote></td>
<td><blockquote>
<p>nr_ddi</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>civilId</p>
</blockquote></td>
<td><blockquote>
<p>nr_identidade</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>controlNumber</p>
</blockquote></td>
<td><blockquote>
<p>nr_controle</p>
</blockquote></td>
</tr>
<tr class="even">
<td><blockquote>
<p>typeNumber</p>
</blockquote></td>
<td><blockquote>
<p>nr_seq_tipo</p>
</blockquote></td>
</tr>
<tr class="odd">
<td><blockquote>
<p>phoneNumber</p>
</blockquote></td>
<td><blockquote>
<p>nr_telefone</p>
</blockquote></td>
</tr>
</tbody>
</table>
