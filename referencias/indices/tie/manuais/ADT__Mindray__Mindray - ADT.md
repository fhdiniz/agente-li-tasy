**Mindray**

![](media/image1.jpeg)

AVISO

O conteúdo deste documento é de propriedade exclusiva da ***Philips*** e está sujeito a alterações sem aviso prévio.

Esta cópia deverá ser protegida contra divulgações indevidas, como cópia da documentação eletrônica, impressa ou parte dela, não deverá ser emprestada, reproduzida ou vendida.

Todos os nomes de empresas, produtos, marcas comerciais, pessoas, personagens, dados ou situações, citados neste documento são fictícios e tem somente objetivo didático.

**2 Sumário**

[1 Objetivo da Integração 3](#objetivo-da-integração)

[1.1 Público 3](#__RefHeading___Toc126917289)

[2 Requisitos Necessários para a Integração 4](#requisitos-necessários-para-a-integração)

[2.1 Infraestrutura 4](#infraestrutura)

[3 Configurações e Parametrizações no Sistema 5](#configurações-e-parametrizações-no-sistema)

[3.1 Forma de Comunicação 5](#forma-de-comunicação)

[3.2 Cadastros e Parametrizações 5](#cadastros-e-parametrizações)

[4 Eventos 8](#eventos)

[4.1 patient.admission 8](#patient.admission)

[4.2 patient.discharge 9](#patient.discharge)

[4.4 patient.transfer 9](#patient.transfer)

[6 Atributos 11](#atributos)

#   

# 1 Objetivo da Integração

Este documento tem como objetivo demonstrar a integração com Tasy Interface Engine entre o sistema Tasy e Mindray.

## 1.1 Público

Hospitais que desejam utilizar a integração Tasy e Mindray.

# 2 Requisitos Necessários para a Integração

Abaixo estão descritos os requisitos mínimos necessários a nível de infraestrutura e sistemas (Multimed, PACS - Picture Archiving and Communication System, Tasy) para que a Integração ocorra com sucesso.

## 2.1 Infraestrutura

Tasy Interface Engine e tasy-interfaces.

# 3 Configurações e Parametrizações no Sistema 

Abaixo estão descritos as configurações e parametrizações necessárias a nível de sistema (Multimed, PACS, Tasy) para o funcionamento da Integração.

## 3.1 Forma de Comunicação

Envio do HL7 para o enpoint terceiro.

## 3.2 Cadastros e Parametrizações 

Solicitar o arquivo .bft que contém os artefatos base do TIE para os eventos Mindray ADT's: A01, A02 e A03. Esta integração trabalha com a versão 2.6 do HL7.

Para importar os artefatos deve-se clicar em “Import Artefacts” e posteriormente carregar o arquivo recebido pelo botão “Load file” e por fim o “Import”.

![](media/image2.png)

Após importar validar se todos os artefatos se encontram na base, segue abaixo lista do que deve conter:

  - Event:
    
      - patient.admission
    
      - patient.transfer
    
      - patient.discharge

  - Flow:
    
      - Mindray - ADT

  - JSON to HL7:
    
      - MINDRAY\_ADT\_A01
    
      - MINDRAY\_ADT\_A02
    
      - MINDRAY\_ADT\_A03

  - Route:
    
      - Mindray.route.ADT\_A01
    
      - Mindray.route.ADT\_A02
    
      - Mindray.route.ADT\_A03

Ativar e configurar as rotas somente dos eventos que se deseja integrar.

![](media/image3.png)

Cada rota equivale a um ADT, segue abaixo relação entre Route x ADT:

  - Mindray.route.ADT\_A01= ADT\_01

  - Mindray.route.ADT\_A02= ADT\_02

  - Mindray.route.ADT\_A03= ADT\_03

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

## 4.2 patient.discharge

1.  Referente ao ADT\_A03 – Alta do Paciente. Disparado ao gerar alta de um atendimento.
    
    Pode ser gerado da seguinte forma: função Entrada Única de Pacientes -\> selecionar um atendimento sem alta -\> botão direito -\> atendimento -\> gerar alta (manual).
    
    ![](media/image8.png)

## 4.4 patient.transfer

4.  Referente ao ADT\_A02 – Transferência do Paciente. Disparado ao transferir um paciente de um setor para o
    
    Pode ser gerado da seguinte forma: função Movimentação de Pacientes -\> selecionar atendimento do paciente -\> aba transferência paciente -\> gerar transferência setor.

![](media/image9.png)

Outro modo de disparar este evento seria: função Movimentação de Pacientes -\> selecionar atendimento do paciente -\> aba transferência paciente -\> registrar saída setor.

![](media/image10.png)

# 6 Atributos

Para verificar os atributos enviados ao TIE, requisitar o documento “Campos HL7 – ADT’s” pois nele constará todos os valores e chaves do json que atualmente são utilizados.
