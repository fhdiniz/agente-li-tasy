**TASY X PFCS**

![](media/image1.jpeg)

AVISO

O conteúdo deste documento é de propriedade exclusiva da ***Philips*** e está sujeito a alterações sem aviso prévio.

Esta cópia deverá ser protegida contra divulgações indevidas, como cópia da documentação eletrônica, impressa ou parte dela, não deverá ser emprestada, reproduzida ou vendida.

Todos os nomes de empresas, produtos, marcas comerciais, pessoas, personagens, dados ou situações, citados neste documento são fictícios e tem somente objetivo didático.

**2 Sumário**

[1 Objetivo da Integração 4](#objetivo-da-integração)

[1.1 Público 4](#__RefHeading___Toc121228213)

[2 Requisitos Necessários para a Integração 5](#requisitos-necessários-para-a-integração)

[2.1 Infraestrutura 5](#infraestrutura)

[3 Configurações e Parametrizações no Sistema 5](#configurações-e-parametrizações-no-sistema)

[3.1 Cadastros e Parametrizações 5](#__RefHeading___Toc121228217)

[3.1.1 Parâmetros Administração do Sistema 5](#parâmetros-administração-do-sistema)

[3.2 Configuração de artefatos TIE 6](#regra-cadastros-gerais)

[4 Testes da integração 7](#testes-da-integração)

[4.1 Empresa 7](#empresa)

[4.2 Estabelecimento 8](#estabelecimento)

[4.3 Setor 8](#setor)

[4.4 Leito/Unidade 10](#leitounidade)

[4.5 Equipamento 11](#equipamento)

[4.6 Atendimento, Médico e Paciente 13](#atendimento-médico-e-paciente)

[4.7 Sinais vitais 13](#sinais-vitais)

[4.8 Fluxo do paciente 14](#fluxo-do-paciente)

[4.8.1 Admissão: 14](#admissão)

[4.8.2 Transferência: 15](#transferência)

[4.8.3 Alta: 17](#alta)

[4.9 Special Request 18](#special-request)

[4.9.1 Contact: 18](#isolamento)

[4.9.2 Droplet: 18](#equipamento-de-proteção-individual-epi)

[4.9.3 Negative pressure: 19](#pressão-negativa)

[4.9.4 Male e Female: 19](#masculino-e-feminino)

[4.9.5 Inmate: 22](#paciente-detento)

[4.9.6 Radiation: 23](#radioterapia)

[4.9.7 Dialysis room: 24](#unidade-diálise)

[4.9.6 Bariatric: 27](#leito-adaptado)

[4.9.7 Fall Risk: 28](#risco-de-queda)

[4.9.8 Wander risk/cognition: 30](#disfunção-cognitiva)

[4.9.9 Needy patient: 31](#paciente-com-deficiência)

[4.9.10 Aggressive/risk behavior: 31](#agressivo)

[4.10 Procedimentos 32](#procedimentos)

# 1 Objetivo da Integração

Inserir e atualizar informações no sistema PFCS.

## 1.1 Público

Sistemas que necessitam consultar, alterar e cadastrar informações no Tasy.

# 2 Requisitos Necessários para a Integração

Abaixo estão descritos os requisitos mínimos necessários a nível de infraestrutura e sistemas (Multimed, PACS - Picture Archiving and Communication System, Tasy) para que a Integração ocorra com sucesso.

## 2.1 Infraestrutura

Tasy Interface Engine.

# 3 Configurações e Parametrizações no Sistema 

Abaixo estão descritos as configurações e parametrizações necessárias a nível de sistema (Multimed, PACS, Tasy) para o funcionamento da Integração.

## 3.1 Cadastros e Parametrizações

2.  
Os cadastros no Tasy Interface Engine serão enviados para serem utilizados como base.

### 3.1.1 Parâmetros Administração do Sistema

Conforme imagem abaixo, deve ser configurado o parâmetro “\[14\] – Versão do PFCS para envio de informações”, da função “Integração”.

![](media/image2.png)

### 3.1.1 Regra Cadastros Gerais

Conforme imagens a seguir, é necessário criar um registro na regra “Cadastros Gerais -\> Sistema -\> Integração -\> Dados da Integração”, nesta regra o ideal é cadastrar informar os campos: Estabelecimento e Estab Integração. Sendo obrigatório o campo “Código Identificador” o valor “PFCS” e o Leito padrão integração com o “PA.NA.NA” esse valor do leito padrão é possível questionar o PFCS se pode ser este valor ou algum outro.

![](media/image3.png)

![](media/image4.png)

## 3.2 Configuração de artefatos TIE

1.  Solicitar os artefatos do TIE informando a versão do PFCS. Após importação configurar o host e porta do servidor que irá receber o fhir em cada Flow.
    
    ![](media/image5.png)

Segue listas com todos os artefatos que devem existir na base após importação do arquivo “.bft”.

  - Event:
    
      - PFCS.company.event;
    
      - PFCS.establishment.event;
    
      - PFCS.company.establishment.event;
    
      - PFCS.device.event;
    
      - PFCS.encounter.event;
    
      - PFCS.location.event;
    
      - PFCS.patient.event;
    
      - PFCS.practitioner.event;
    
      - PFCS.procedure.event;
    
      - PFCS.service.request.event;
    
      - PFCS.special.request.event;
    
      - PFCS.vital.signs.event;
    
      - PFCS.task.event.

  - Flow:
    
      - PFCS.company.flow;
    
      - PFCS.establishment.flow;
    
      - PFCS.company.establishment.flow;
    
      - PFCS.device.flow;
    
      - PFCS.encounter.flow;
    
      - PFCS.location.flow;
    
      - PFCS.patient.flow;
    
      - PFCS.practitioner.flow;
    
      - PFCS.procedure.flow;
    
      - PFCS.service.request.flow;
    
      - PFCS.special.request.flow;
    
      - PFCS.vital.signs.flow;
    
      - PFCS.task.flow.

  - Routes:
    
      - PFCS.company.routes;
    
      - PFCS.establishment.routes;
    
      - PFCS.company.establishment.routes;
    
      - PFCS.device.routes;
    
      - PFCS.encounter.routes;
    
      - PFCS.location.routes;
    
      - PFCS.patient.routes;
    
      - PFCS.practitioner.routes;
    
      - PFCS.procedure.routes;
    
      - PFCS.service.request.routes;
    
      - PFCS.special.request.routes;
    
      - PFCS.vital.signs.routes;
    
      - PFCS.task.routes.

  - JSON to JSON:
    
      - PFCS.company;
    
      - PFCS.establishment;
    
      - PFCS.company.establishment;
    
      - PFCS.patient;
    
      - PFCS.encounter;
    
      - PFCS.encounter.saida;
    
      - PFCS.device;
    
      - PFCS.location;
    
      - PFCS.service.request;
    
      - PFCS.special.request;
    
      - PFCS.practitioner;
    
      - PFCS.procedure;
    
      - PFCS.vital.signs.

# 4 Testes da integração

Abaixo estão descritos os casos em que a integração é utilizada.

## 4.1 Empresa

3.  A empresa será enviada, quando for cadastrado um novo registro, quando o usuário alterar a razão social ou
    
    a situação ou quando a empresa for deletada.
    
    ![](media/image6.png)

## 4.2 Estabelecimento

7.  O estabelecimento será enviado, quando for cadastrado um novo registro, quando for alterarado o nome
    
    fantasia ou a situação ou quando o estabelecimeto for deletado.

![](media/image7.png)

##  4.3 Setor

9.  O setor será enviado ao ser cadastrado sendo enviado com um leito virtual, após isso, ele será enviado quando for alterado a descrição, a situação, a classificação ou quando o setor for deletado. Para que o setor seja enviado é necessário que a classificação seja: Pronto socorro(1), Centro cirúrgico(2), Unidades de Internação(3), Unidade de terapia intensiva(4) e Recém-nascido(9).

![](media/image8.png)

![](media/image9.png)

## 4.4 Leito/Unidade

12. A unidade será enviada, quando for cadastrado um novo registro, quando for alterado a situação ou o status da unidade e quando a unidade for deletada. Porém para que seja enviada, o setor deve possuir a classificação: Pronto socorro(1), Centro cirúrgico(2), Unidades de Internação(3), Unidade de terapia intensiva(4) e Recém-nascido(9).

![](media/image10.png)

## 4.5 Equipamento

13. O equipamento será enviado sempre que for cadastrado um novo registro, quando alterá-lo ou quando ele for excluído. Porém para que seja enviado, a sua classificação precisa conter o campo “Monitor” checkado. Ele será iniciado e finalizado conforme entrada e saída do paciente na unidade em que o equipamento está vinculado.

![](media/image11.png)

![](media/image12.png)

![](media/image13.png)

## 4.6 Atendimento, Médico e Paciente

14. O atendimento, paciente e médico serão enviados sempre que for cadastrado um novo atendimento, quando alterar o tipo de atendimento, procedência, médico responsável, data de cancelamento, data de alta, data de observação, data de previsão de alta e quando for cadastrado ou alterado o setor e leito, ou quando o atendimento for excluído. Também é enviado ao criar e liberar um diagnóstico.

![](media/image14.png)

## 4.7 Sinais vitais

16. Os sinais vitais serão enviados sempre que for cadastrado um novo registro, quando alterar a pressão arterial diastólica, pressão arterial sistólica, frequência cardíaca, frequência respiratória, saturação de oxigênio, data da coleta do sinal vital, situação ou quando o sinais vitais forem excluídos.

![](media/image15.png)

## 4.8 Fluxo do paciente

17. O fluxo do paciente é separado em três partes, admissão, transferência e alta.

### 4.8.1 Admissão:

Sempre que um atendimento, for criado ou alterado para o tipo Pronto socorro ou Ambulatorial é enviado uma “Admissão planejada”, isso ocorre também quando o atendimento receber um novo médico responsável. Caso o atendimento seja criado ou alterado para um tipo diferente de ambos, é enviado uma “Admissão realizada” e caso o atendimento seja cancelado, excluído ou o médico deixe de assumir o atendimento, é enviado um “Estorno da Admissão”.

![](media/image16.png)

### 4.8.2 Transferência:

Sempre que for criado uma reserva de leito para um paciente com o status abaixo, é enviado uma “Transferência planejada”.

  - Aceito

  - Aguardando

  - Aguardando Análise

  - Aprovada

  - Chamado

  - Em análise

  - Reservado

![](media/image17.png)

Sempre que for criado uma reserva de leito para um paciente com o status abaixo, é enviado uma “Transferência realizada”.

  - Realizada

  - Transferência realizada

  - Acomodado

![](media/image18.png)

Sempre que for excluído uma reserva de leito ou criado uma uma com o status abaixo, é enviado um “Estorno da transferência”.

  - Transferência recusada pelo paciente

  - Negada

  - Cancelada

  - Desistiu

![](media/image19.png)

### 4.8.3 Alta:

Sempre que um atendimento, receber data de alta prevista, é enviado uma “Alta planejada”, quando o atendimento recebe a data de alta, é enviado uma “Alta realizada” e caso ocorra o estorno da alta é enviado um “Estorno da Alta”.

![](media/image20.png)

Também será enviado uma previsão de alta, quando for criada e liberada pela CPOE uma prescrição especial do tipo “Alta”.

![](media/image21.png)

## 4.9 Special Request

### 4.9.1 Isolamento:

18. 
Sempre que um atendimento for inserido ou alterado e o campo “Isolamento” conter o valor “S” (Em azul), a flag “Contact” é enviada. Caso o campo “Isolamento” seja alterado para “N” em branco, é enviado uma flag “Contact” com o status inativo.

![](media/image22.png)

### 4.9.2 Equipamento de Proteção Individual (EPI):

19. 
Sempre que uma precaução for liberada e conter o campo “Equipamento de Proteção Individual (EPI)” com valor “S” (Em azul), a flag “Equipamento de Proteção Individual (EPI)” é enviada. Caso a precaução seja inativada e o atendimento não possua nenhuma outra precaução com o campo com valor “S”, é enviado uma flag “Equipamento de Proteção Individual (EPI)” com o status inativo. Também é enviado ao criar e liberar um diagnóstico.

![](media/image23.png)

### 4.9.3 Pressão negativa:

20. 
Sempre que uma precaução for liberada e conter o campo “Pressão negativa” com valor “S” (Em azul), a flag “Negative pressure” é enviada. Caso a precaução seja inativada e o atendimento não possua nenhuma outra precaução com o campo com valor “S”, é enviado uma flag “Negative pressure” com o status inativo. Também é enviado ao criar e liberar um diagnóstico.

![](media/image24.png)

### 4.9.4 Masculino e Feminino:

21. 
Sempre que for criado uma reserva de leito para um paciente do sexo “Masculino” com o status abaixo é enviado uma flag “Male”, caso o paciente seja do sexo “Feminino” é enviado a flag “Female”.

  - Aceito

  - Aguardando

  - Aguardando Análise

  - Aprovada

  - Chamado

  - Em análise

  - Reservado

![](media/image17.png)

![](media/image25.png)

Caso o status da reserva seja alterado ou criado com um dos status abaixo e paciente seja do sexo “Masculino” enviado uma flag “Male” com status inativo ou se for do sexo “Feminino” é enviado a flag “Female” com o status inativo.

  - Realizada

  - Transferência realizada

  - Acomodado

<!-- end list -->

  - Transferência recusada pelo paciente

  - Negada

  - Cancelada

  - Desistiu

![](media/image18.png)

![](media/image25.png)

### 4.9.5 Paciente detento:

22. Sempre que um atendimento for enviado e a pessoa vinculada ao atendimento possuir uma classificação ativa que possua o campo “Paciente detento” com valor “S” (Em azul) será enviado uma flag “Inmate”. Caso a classificação seja inativada e o paciente não possua nenhuma outra classificação ativa com o campo “Paciente detento” com valor “S” (Em azul) , será enviado uma flag “Inmate” com o status inativo. Também é enviado ao criar e liberar um diagnóstico.

![](media/image26.png)

![](media/image27.png)

### 4.9.6 Radioterapia:

Sempre que uma unidade ou leito receber um novo atendimento e está possuir o campo “Radioterapia” com valor “S” (Em azul), a flag “Radiation” será enviada. Sempre é enviado duas vezes, a primeira com status inativo e com o atendimento anterior e a segunda com status ativo e com o novo atendimento.

![](media/image28.png)

### 4.9.7 Unidade diálise:

Sempre que for criado uma reserva de leito para um paciente com o status abaixo, aonde o setor e unidade ou leito desejado exista dentro da tela Gestão de insuficiencia renal \> Cadastro \> Pontos de diálise, a flag “Dialysis room” será enviada.

  - Aceito

  - Aguardando

  - Aguardando Análise

  - Aprovada

  - Chamado

  - Em análise

  - Reservado

![](media/image17.png)

![](media/image29.png)

Caso o status da reserva seja alterado ou criado com um dos status abaixo, aonde o setor e unidade ou leito desejado, exista dentro da tela Gestão de insuficiencia renal \> Cadastro \> Pontos de diálise, a flag “Dialysis room” será enviada com o status inativo.

  - Realizada

  - Transferência realizada

  - Acomodado

<!-- end list -->

  - Transferência recusada pelo paciente

  - Negada

  - Cancelada

  - Desistiu

![](media/image18.png)

![](media/image29.png)

### 4.9.6 Leito adaptado:

Sempre que uma unidade ou leito receber um novo atendimento e está possuir o campo “Leito adaptado” com valor “S” (Em azul), a flag “Leito adaptado” será enviada. Sempre é enviado duas vezes, a primeira com status inativo e com o atendimento anterior e a segunda com status ativo e com o novo atendimento.

![](media/image30.png)

### 4.9.7 Risco de queda:

Sempre que uma nova escala for inserida e o atendimento esteja vinculado a um setor e leito e possua risco de queda, a flag “Fall Risk” é enviada. Caso a escala seja inativada e o atendimento não possua nenhuma outra escala ativa com risco de queda, a flag “Fall Risk” será enviada com o status inativo. Serão enviadas apenas as escalas abaixo. Logo após a lista de escalas, estão os exemplos de cadastro das escalas dentro da função Prontuário Eletrônico Paciente – PEP.

  - Escala de JH-FRAT

  - Escala EIF

  - Escala Score flex II

  - Escala Morse

  - Escala Stratify

  - Escala de Avaliação de Risco de Queda da NHS (EARQ)

  - Escala Morse

![](media/image31.png)

  - Escala Stratify

![](media/image32.png)

  - Escala de Avaliação de Risco de Queda da NHS (EARQ)

![](media/image33.png)

### 4.9.8 Disfunção cognitiva:

Sempre que uma unidade ou leito receber um novo atendimento e está possuir o campo “Leito próximo enfermagem” com valor “S” (Em azul), a flag “Wander risk/cognition” será enviada. Sempre é enviado duas vezes, a primeira com status inativo e com o atendimento anterior e a segunda com status ativo e com o novo atendimento. As escalas abaixo são

![](media/image34.png)

### 4.9.9 Paciente com deficiência:

24. Sempre que um atendimento for enviado e a pessoa vinculada ao atendimento possuir o campo “Dependente/paciente com deficiência” com valor “S” (Em azul) será enviado uma flag “Needy patient”. Caso o campo seja alterado para “N” (Em branco) será enviado uma flag “Needy patient” com o status inativo.

![](media/image35.png)

### 4.9.10 Agressivo:

25. Sempre que um atendimento for enviado e a pessoa vinculada ao atendimento possuir uma classificação ativa que possua o campo “Agressivo” com valor “S” (Em azul) será enviado uma flag “Aggressive/risk behavior”. Caso a classificação seja inativada e o paciente não possua nenhuma outra classificação ativa com o campo “Agressivo” com valor “S” (Em azul) , será enviado uma flag “Aggressive/risk behavior” com o status inativo. Também é enviado ao criar e liberar um diagnóstico.

![](media/image36.png)

![](media/image27.png)

## 4.10 Procedimentos

27. Os procedimentos serão enviados sempre que for cadastrado um novo registro ou quando ele for alterdo. Por padrão o status enviado é “in-progress”, porém caso possua data de suspensão, será enviado com status “entered-in-error” ou caso possua data de início e data de fim o status será “completed”. Nesse processo é necessário informar o médico responsável ou executor.
    
    ![](media/image37.png)

## 4.10 Gestão de Vagas

29. As solicitações de vagas serão enviadas ao cadastrar um registro sem atendimento, ao cadastrar um registro com atendimento, ao vincular um atendimento em um registro sem atendimento e ao desvincular um atendimento. Caso não seja escolhida uma unidade será enviado a unidade virtual do setor, sendo que o campo para enviar os dados da reservão são o: setor desejado, unidade básica e unidade complementar.
    
    ![](media/image38.png)
