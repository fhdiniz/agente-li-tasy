**EPIMED**

![](media/image1.jpeg)

AVISO

O conteúdo deste documento é de propriedade exclusiva da ***Philips*** e está sujeito a alterações sem aviso prévio.

Esta cópia deverá ser protegida contra divulgações indevidas, como cópia da documentação eletrônica, impressa ou parte dela, não deverá ser emprestada, reproduzida ou vendida.

Todos os nomes de empresas, produtos, marcas comerciais, pessoas, personagens, dados ou situações, citados neste documento são fictícios e tem somente objetivo didático.

**2 Sumário**

[1 Objetivo da Integração 3](#objetivo-da-integração)

[1.1 Público 3](#__RefHeading___Toc114490364)

[2 Requisitos Necessários para a Integração 4](#requisitos-necessários-para-a-integração)

[2.1 Infraestrutura 4](#infraestrutura)

[3 Configurações e Parametrizações no Sistema 5](#configurações-e-parametrizações-no-sistema)

[3.1 Forma de Comunicação 5](#forma-de-comunicação)

[3.2 Cadastros e Parametrizações 5](#cadastros-e-parametrizações)

[4 Eventos 8](#eventos)

[4.1 patient.admission 8](#patient.admission)

[4.2 patient.admission.cancel.monitor 9](#patient.admission.cancel.monitor)

[4.3 patient.discharge 9](#patient.discharge)

[4.4 patient.discharge.cancel.monitor 10](#patient.discharge.cancel.monitor)

[4.5 patient.transfer 10](#patient.transfer)

[5 Cadastros de estabelecimento 12](#cadastros-de-estabelecimento)

[5.1 Duplicar o Flow 12](#duplicar-o-flow)

[5.2 Duplicar o código 13](#duplicar-o-código)

[6 Atributos 15](#atributos)

#   

# 1 Objetivo da Integração

Este documento tem como objetivo demonstrar a integração com Tasy Interface Engine entre o sistema Tasy e EPIMED.

## 1.1 Público

Hospitais que desejam utilizar a integração Tasy e EPIMED.

# 2 Requisitos Necessários para a Integração

Abaixo estão descritos os requisitos mínimos necessários a nível de infraestrutura e sistemas (Multimed, PACS - Picture Archiving and Communication System, Tasy) para que a Integração ocorra com sucesso.

## 2.1 Infraestrutura

Tasy Interface Engine e tasy-interfaces.

# 3 Configurações e Parametrizações no Sistema 

Abaixo estão descritos as configurações e parametrizações necessárias a nível de sistema (Multimed, PACS, Tasy) para o funcionamento da Integração.

## 3.1 Forma de Comunicação

Enviado do HL7 para o enpoint (SOAP) terceiro.

## 3.2 Cadastros e Parametrizações 

Solicitar o arquivo .bft que contém os artefatos base do TIE para os eventos EPIMED ADT's: A01, A02, A03, A11 e A13. Esta integração trabalha com a versão 2.3 do HL7.

Para importar os artefatos deve-se clicar em “Import Artefacts” e posteriormente carregar o arquivo recebido pelo botão “Load file” e por fim o “Import”.

![](media/image2.png)

Após importar validar se todos os artefatos se encontram na base, segue abaixo lista do que deve conter:

  - Event:
    
      - patient.admission
    
      - patient.transfer
    
      - patient.discharge
    
      - patient.discharge.cancel
    
      - patient.admission.cancel.monitor

  - Flow:
    
      - ADT – EPIMED

  - JSON to HL7:
    
      - EPIMED\_ADT\_A01
    
      - EPIMED\_ADT\_A02
    
      - EPIMED\_ADT\_A03
    
      - EPIMED\_ADT\_A11
    
      - EPIMED\_ADT\_A13

  - Route:
    
      - EPIMED – patient.admission
    
      - EPIMED – patient.admission.cancel.monitor
    
      - EPIMED – patient.discharge
    
      - EPIMED – patient.discharge.cancel
    
      - EPIMED – patient.transfer

  - Template:
    
      - epimed.soap.format.adt

Ativar e configurar as rotas somente dos eventos que se deseja integrar.

![](media/image3.png)

Obs.: Desta forma é possível configurar até 3 estabelecimentos.

Cada rota equivale a um ADT, segue abaixo relação entre Route x ADT:

  - EPIMED – patient.admission = ADT\_01

  - EPIMED – patient.transfer = ADT\_02

  - EPIMED – patient.discharge = ADT\_03

  - EPIMED – patient.admission.cancel.monitor = ADT\_11

  - EPIMED – patient.discharge.cancel = ADT\_13

No Tasy deve ser configurado os parâmetros 10 e 11 (Administração do Sistema \> Sistema \> Integração), ativando a integração com TIE e informando o endereço do servidor do TIE.

![](media/image4.png)

![](media/image5.png)

#  4 Eventos

Os serviços cadastrados são disparados de acordo com ações específicas realizadas no Tasy e poderão ser visualizados através da seguinte busca:

![](media/image6.png)

Neste exemplo, a busca está filtrando pelo evento patient.admission, e para buscar por outros eventos basta mudar o patient.admission pelo evento desejado.

Os dados estão guardados no campo DS\_CONTENT, e copiando o texto dessa coluna, espera-se um resultado como este:

![](media/image7.png)

## 4.1 patient.admission

Referente ao ADT\_A01 – Admissão do Paciente. Disparado ao admitir o paciente no primeiro setor do atendimento.

Pode ser gerado da seguinte forma: função Entrada Única de Pacientes -\> novo atendimento -\> salvar o setor.

## 4.2 patient.admission.cancel.monitor

1.  Referente ao ADT\_A11 – Cancelamento de admissão do Paciente. Disparado ao cancelar um atendimento.
    
    Pode ser gerado da seguinte forma: função Entrada Única de Pacientes -\> selecionar um atendimento -\> botão direito do mouse -\> atendimento -\> cancelar atendimento.
    
    ![](media/image8.png)

## 4.3 patient.discharge

4.  Referente ao ADT\_A03 – Alta do Paciente. Disparado ao gerar alta de um atendimento.
    
    Pode ser gerado da seguinte forma: função Entrada Única de Pacientes -\> selecionar um atendimento sem alta -\> botão direito -\> atendimento -\> gerar alta (manual).
    
    ![](media/image9.png)

## 4.4 patient.discharge.cancel.monitor

7.  Referente ao ADT\_A13 – Cancelamento de alta do Paciente. Disparado ao estornar a alta de um paciente.
    
    Pode ser gerado da seguinte forma: função Entrada Única de Pacientes -\> selecionar um atendimento com alta -\> atendimento -\> desfazer alta.
    
    ![](media/image10.png)

## 4.5 patient.transfer

10. Referente ao ADT\_A02 – Transferência do Paciente. Disparado ao transferir um paciente de um setor para o
    
    Pode ser gerado da seguinte forma: função Movimentação de Pacientes -\> selecionar atendimento do paciente -\> aba transferência paciente -\> gerar transferência setor.

![](media/image11.png)

Outro modo de disparar este evento seria: função Movimentação de Pacientes -\> selecionar atendimento do paciente -\> aba transferência paciente -\> registrar saída setor.

![](media/image12.png)

# 5 Cadastros de estabelecimento

Por padrão é possível cadastrar no Flow três estabelecimentos, três tokens e três Id’s mas caso seja necessário mais valores é possível realizar de duas maneiras.

## 5.1 Duplicar o Flow

Encontrar o artefato “ADT – EPIMED” no item Flow e utilizar a opção “Copy”.

![](media/image13.png)

Será criado um novo artefato com o nome anterior apenas adicionando “\_copy” no sufixo, é possível alterar esse nome para algum outro para melhor identificação.

![](media/image14.png)

É necessário realizar o mesmo processo para os artefatos que se encontram dentro do item “Routes” sendo eles: EPIMED – patient.admission, EPIMED – patient.admission.cancel.monitor, EPIMED – patient.discharge, EPIMED – patient.discharge.cancel e EPIMED – patient.transfer.

![](media/image15.png)

Após duplicar e alterar o nome conforme desejado, deve apenas vincular o flow criado anteriormente com a nova rota criada.

![](media/image16.png)

## 5.2 Duplicar o código

Outra forma de fazer realizar o cadastro de mais estabelecimentos seria duplicar o código do artefato e adicionar novas variáveis de controle.

Abrir o artefato “ADT – EPIMED” que se encontra dentro do item Flow, ir na aba “Configurations” e utilizar o botão “Add”, cadastrar o nome do item “dynamicToken\_N”, “establishmentID\_N” e “integrationId\_N”, sendo N qualquer valor numérico para melhor compreensão.

**Obs.: Para cada estabelecimento novo é necessário cadastrar um “dynamicToken\_N”, “establishmentID\_N” e “integrationId\_N”.**

Após realizar esse cadastro, deve-se ir na aba “Source Code”, copiar e colar a área destacada na imagem alterando o “\_3” para o mesmo sufixo criado anteriormente.

![](media/image17.png)

# 6 Atributos

Para verificar os atributos enviados ao TIE, requisitar o documento “Campos HL7 – ADT’s” pois nele constará todos os valores e chaves do json que atualmente são utilizados.
