**Draeger - ADT**

![](media/image1.jpeg)

AVISO

O conteúdo deste documento é de propriedade exclusiva da ***Philips*** e está sujeito a alterações sem aviso prévio.

Esta cópia deverá ser protegida contra divulgações indevidas, como cópia da documentação eletrônica, impressa ou parte dela, não deverá ser emprestada, reproduzida ou vendida.

Todos os nomes de empresas, produtos, marcas comerciais, pessoas, personagens, dados ou situações, citados neste documento são fictícios e tem somente objetivo didático.

**2 Sumário**

[1 Objetivo da Integração 3](#objetivo-da-integração)

[1.1 Público 3](#__RefHeading___Toc493853014)

[2 Requisitos Necessários para a Integração 4](#requisitos-necessários-para-a-integração)

[2.1 Infraestrutura 4](#infraestrutura)

[3 Configurações e Parametrizações no Sistema 6](#configurações-e-parametrizações-no-sistema)

[3.1 Forma de Comunicação 6](#forma-de-comunicação)

[3.2 Cadastros e Parametrizações 6](#cadastros-e-parametrizações)

[4 Eventos 8](#eventos)

# 1 Objetivo da Integração

Permitir obter os dados da pessoa e atendimento.

## 1.1 Público

Setor que mantem os dados de pessoa e atendimento.

# 2 Requisitos Necessários para a Integração

Abaixo estão descritos os requisitos mínimos necessários a nível de infraestrutura e sistemas (Multimed, PACS - Picture Archiving and Communication System, Tasy) para que a Integração ocorra com sucesso.

## 2.1 Infraestrutura

Tasy Interface Engine e tasy-interfaces.

# 3 Configurações e Parametrizações no Sistema 

Abaixo estão descritos as configurações e parametrizações necessárias a nível de sistema (Multimed, PACS, Tasy) para o funcionamento da Integração.

Este manual tem o intuito de apresentar a configuração necessária para a ativação da integração no TIE e não a configuração entre Tasy x TIE.

## 3.1 Forma de Comunicação

HL7, podendo ser configurado para JSON ou XML.

## 3.2 Cadastros e Parametrizações 

Solicitar os artefatos base da integração Draeger TIE.

Após importar no TIE configurar o host e porta do servidor que irá receber o HL7 em *Management -\> Flow*.

![](media/image2.png)

Ativar a rota somente dos eventos que se deseja integrar.

Atenção: É possível configurar a porta e host nos artefatos de rota mas caso configure neles o valor informado anteriormente no flow deixará de ser consistido.

![](media/image3.png)

Foram criados os HL7 baseado na versão 2.3 em uma estrutura padrão, caso o terceiro utilize uma versão ou estrutura diferente deverá ser requisitado na OS e enviado um exemplo com todas as informações necessárias.

É possível visualizar os atributos que temos hoje disponiveís para envio no HL7 no documento “Campos HL7 - ADT's” para isso solicite na OS o arquivo.

![](media/image4.png)

No Tasy deve ser configurado os parâmetros 10 e 11 (Administração do Sistema \> Sistema \> Integração), ativando a integração com TIE e informando o endereço do servidor do TIE.

![](media/image5.png)

![](media/image6.png)

#  4 Eventos

## 4.1 patient.admission

Referente ao HL7 ADT A01. Disparado ao admitir o paciente no primeiro setor do atendimento.

## 4.2 patient.transfer

1.  Referente ao HL7 ADT A02. Disparado ao transferir o paciente de unidade.

## 4.3 patient.discharge

2.  Referente ao HL7 ADT A03. Disparado ao efetuar a alta do paciente.

## 4.4 patient.information.update

3.  Referente ao HL7 ADT A08. Disparado ao atualizar um atendimento.

## 4.5 patient.discharge.cancel

5.  Referente ao HL7 ADT A13. Disparado ao estornar a alta do paciente.

## 4.6 patient.swap

Referente ao HL7 ADT A17. Disparado ao realizar a troca de leitos entre os pacientes.

6.  
#  5 Artefatos

Devem existir os seguintes artefatos na base após a importação do .bft.

## 5.1 Event

  - patient.admission

  - patient.transfer

  - patient.discharge

  - patient.information.update

  - patient.discharge.cancel

  - patient.swap

## 5.2 Flow

  - API\_DRAEGER\_ADT

## 5.4 JSON to HL7v2

  - DRAEGER\_ADT\_A01

  - DRAEGER\_ADT\_A02

  - DRAEGER\_ADT\_A03

  - DRAEGER\_ADT\_A08

  - DRAEGER\_ADT\_A13

  - DRAEGER\_ADT\_A17

## 5.3 Route

  - DRAEGER - patient.admission

  - DRAEGER - patient.transfer

  - DRAEGER - patient.discharge

  - DRAEGER - patient.information.update

  - DRAEGER - patient.discharge.cancel

  - DRAEGER - patient.swap

## 5.5 Integrations

  - Draeger - ADT
