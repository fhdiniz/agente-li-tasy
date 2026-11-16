**API VOICEHCS**

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

[2.2 Sistema 4](#_Toc98401976)

[3 Configurações e Parametrizações no Sistema 5](#configurações-e-parametrizações-no-sistema)

[3.1 Forma de Comunicação 5](#forma-de-comunicação)

[3.2 Cadastros e Parametrizações 5](#cadastros-e-parametrizações)

[3.2.1 Conector 5](#conector)

[3.2.2 Evento 6](#evento)

[3.2.3 Fluxo 7](#fluxo)

[3.2.4 Rota 8](#rota)

[3.2.5 Mapeamento 9](#mapeamento)

[4 Retorno 10](#retorno)

[4.1 Caso de Erro 10](#caso-de-erro)

[4.2 Caso de Sucesso 11](#caso-de-sucesso)

# 1 Objetivo da Integração

Enviar ao sistema terceiro que houve uma internação ou uma necessidade de higienização e receber do sistema terceiro o novo status de leito.

## 1.1 Principais Características

  - Permite o envio das alterações de status de leito.

  - Permite receber o novo status do leito.

## 1.2 Público

A integração está destinada aos profissionais responsáveis pela hotelaria e governança hospitalar.

# 2 Requisitos Necessários para a Integração

Abaixo estão descritos os requisitos mínimos necessários a nível de infraestrutura e sistemas (Multimed, PACS - Picture Archiving and Communication System, Tasy) para que a Integração ocorra com sucesso.

## 2.1 Infraestrutura

> TIE (Tasy Interfaces Engine) e tasy-interfaces.

## 2.2 Sistema

> Compilar o objeto 'recebimento\_voicehcs\_tie' disponibilizados pela Philips.

# 3 Configurações e Parametrizações no Sistema

Abaixo estão descritos as configurações e parametrizações necessárias a nível de sistema (Multimed, PACS, Tasy) para o funcionamento da Integração.

## 3.1 Forma de Comunicação

> A comunicação é feita utilizando o formato JSON.

## 3.2 Cadastros e Parametrizações

> Toda a parametrização da integração deve ser efetuada no TIE, incluindo conectores, eventos, fluxos, rotas e mapeamentos.

### 3.2.1 Conector

> No TIE deve ser configurado o conector conforme a orientação a abaixo. Sendo este artefato utilizado para o evento de recebimento dos dados do terceiro.

  - General:
    
      - Name: api.voice.receiver (Conector de recebimento dos dados do terceiro)

  - Source Code

![](media/image3.png)

  - Configurations:
    
      - host: 0.0.0.0
    
      - methods: PUT
    
      - path: api/bed-control
    
      - port: 9090
    
      - protocol: http

### 3.2.2 Evento

> No TIE deve existir os eventos conforme imagens abaixo.

  - General:
    
      - Name: api.voice.receiver (Evento de recebimento dos dados do terceiro)

![Interface gráfica do usuário, Texto, Aplicativo, Email Descrição gerada automaticamente](media/image4.png)

  - General:
    
      - Name: voicehcstie.send (Evento de envio dos dados ao terceiro)

![Interface gráfica do usuário, Texto, Aplicativo, Email Descrição gerada automaticamente](media/image5.png)

### 3.2.3 Fluxo

> No TIE devem ser configurados os fluxos conforme abaixo.

  - General:
    
      - Name: api.voice.receiver (Fluxo de recebimento dos dados do terceiro)

  - ![](media/image6.png)Source Code:

> Configurations:

  - host: 0.0.0.0 (endereço do tasy-interfaces)

  - port: 50001 (porta utilizada no tasy-interfaces)

<!-- end list -->

  - General:
    
      - Name: api.voice.receiver (Fluxo de envio dos dados ao terceiro)

  - Source Code:

![](media/image7.png)

### 3.2.4 Rota

> No TIE devem ser configuradas as rotas conforme imagens abaixo.

  - General:
    
      - Name: api.voice.receiver (Rota de recebimento dos dados do terceiro)

![](media/image8.png)

  - General:
    
      - Name: VOICEHCS Main (Rota de envio dos dados ao terceiro)

![](media/image9.png)

### 3.2.5 Mapeamento

  - General:
    
      - Name: api.voice.map.return (Mapeamento utilizado para o JSON de retorno ao terceiro)

> ![](media/image10.png)

# 4 Retorno

## 4.1 Caso de Erro

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo.

  - Type: PUT

  - Path: /api/bed-control/update-action

  - Body (Raw JSON):

> {
> 
> "mensagem": {
> 
> "hospital": {
> 
> "uuid": "9999",
> 
> "nome": "Pirajussara"
> 
> },
> 
> "lugar": {
> 
> "uuid": "1",
> 
> "nome": "1"
> 
> },
> 
> "status": "1",
> 
> "codigo": "EMD"
> 
> }
> 
> }

![Interface gráfica do usuário, Texto, Aplicativo, Email, Teams Descrição gerada automaticamente](media/image11.jpeg)

## 4.2 Caso de Sucesso

> Utilizando o Postman, deve-se criar uma nova requisição conforme os dados abaixo.

  - Type: PUT

  - Path: /api/bed-control/update-action

  - Body (Raw JSON):

> {
> 
> "mensagem": {
> 
> "hospital": {
> 
> "uuid": "9999",
> 
> "nome": "Pirajussara"
> 
> },
> 
> "lugar": {
> 
> "uuid": "79449", /\*Informar um setor cadastro no Tasy\*/
> 
> "nome": "Acomodado2” /\*Informar um leito cadastro no Tasy\*/
> 
> },
> 
> "status": "3",
> 
> "codigo": ""
> 
> }
> 
> }

![Interface gráfica do usuário, Texto, Aplicativo, Email Descrição gerada automaticamente](media/image12.png)
