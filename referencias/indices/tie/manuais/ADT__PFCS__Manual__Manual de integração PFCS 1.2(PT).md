# Índice

[1. Estrutura Organizacional 3](#section)

[1.1. Empresa 3](#empresa)

[1.2. Estabelecimento 4](#estabelecimento)

[1.3. Departamentos e Leitos 4](#setores-e-leitos)

[1.3.1. Tipos de leitos/departamentos 5](#tipos-de-leitossetores)

[2. Definições gerais 6](#definições-gerais)

[2.1. Estado operacional dos leitos 6](#status-operacional-dos-leitos)

[2.2. Combinações do recurso ServiceRequest 6](#combinações-do-recurso-servicerequest)

[3. Demanda Corporativa 7](#demanda-corporativa)

[3.1. Censo e Capacidade Geral 7](#censo-e-capacidade-geral)

[3.2. Censo PA 9](#censo-pa)

[3.3. Tempo de espera no PA 9](#tempo-de-espera-pa)

[3.4. Leitos disponíveis 9](#leitos-disponíveis)

[3.5. Leitos bloqueados 9](#leitos-bloqueados)

[3.6. Leitos disponíveis de UTI 9](#leitos-disponíveis-de-uti)

[3.7. Leitos de telemetria disponíveis 10](#leitos-de-telemetria-disponíveis)

[3.8. Admissões (últimas 24hrs) 10](#admissões-últimas-24h)

[3.9. Altas (últimas 24hrs) 10](#altas-últimas-24h)

[4. Priorização de Admissões 10](#priorização-de-admissões)

[4.1. Censo e Capacidade do PA 11](#censo-e-capacidade-do-pa)

[4.2. Pedidos de internação no PA 11](#pedidos-de-internação-no-pa)

[4.3. *Status* do PA 12](#status-do-pa)

[4.3.1. Admissões potenciais 12](#admissões-potenciais)

[4.3.2. Paciente casual no PA 12](#paciente-casual-no-pa)

[4.3.3. Em observação/Aguardando 13](#em-observaçãoaguardando)

[5. Critical Care 14](#critical-care)

[6. Telemetria 15](#_Toc69991866)

# 

# Estrutura Organizacional

A estrutura organizacional se refere a forma com que a estrutura hospitalar está organizada, como empresa, estabelecimento, setores e leitos. Este item é a base para o PFCS funcionar de maneira correta, pois, a partir destas informações, é possível realizar cálculos de ocupação, analisar estado do leito, entre outros.

O primeiro passo, para se ter uma precisão nos dados, então, é realizar o envio dos pacotes contendo toda a estrutura hospitalar, conforme imagem a seguir:

![](media/image2.png)

Os itens do pacote serão abordados de maneira individual. Todavia, é possível enviar toda a estrutura em um único pacote, podendo enviar diversos leitos, empresas e estabelecimentos de maneira simultânea.

## Empresa

O pacote para se inserir uma empresa no sistema necessita apenas do recurso FHIR *Organization*. Os dados obrigatórios para este pacote são:

  - **id:** chave de identificação única da empresa

  - **identifier.value:** mesmo valor utilizado em *id*

  - **name:** nome da empresa

  - **active: *status* do registro da empresa**

A seguir, um exemplo de pacote:

Após o envio do pacote, será possível visualizar a empresa inserida no PFCS, conforme a seguinte imagem:

![](media/image4.png)

## Estabelecimento

O pacote para envio do estabelecimento é semelhante ao da empresa. A diferença está em um campo adicional, o qual faz referência a empresa em que o estabelecimento pertence. Seguem os dados obrigatórios:

  - **id:** chave de identificação única do estabelecimento

  - **identifier.value:** mesmo valor utilizado em *id*

  - **name:** nome do estabelecimento

  - **active: *status* do estabelecimento**

  - **partOf.reference: chave de identificação única da empresa a qual o estabelecimento pertence**

A seguir, um exemplo de pacote:

Após o envio do pacote, será possível visualizar o estabelecimento inserido no PFCS, conforme a seguinte imagem:

![](media/image4.png)

## Setores e Leitos

O pacote utilizado para enviar setores, quartos e leitos é integrado e utiliza o recurso FHIR *Location*. Na prática, o que é enviado é o leito, porém, junto ao leito, estão o setor e o quarto. Os campos obrigatórios são os seguintes:

  - **id:** chave de identificação única da localização, composta pelo nome do setor, nome do quarto e nome do leito (Setor.Quarto.Leito)

  - **identifier.value:** mesmo valor utilizado em *id*

  - **name:** nome da localização

  - **status: *status* do registro do leito**

  - **operationalStatus.code: código do *status* operacional do leito**

  - **operationalStatus.display: descrição do *status* operacional do leito**

  - **type.coding.code: código do tipo do leito**

  - **type.coding.display: descrição do tipo do leito**

  - **managingOrganization.reference: chave de identificação única do estabelecimento o qual o leito pertence**

A seguir, um exemplo de pacote:

Após o envio do pacote, será possível visualizar o setor e o leito, conforme apresentado a seguir:

![](media/image7.png)

###  Tipos de leitos/setores

Ao realizar o envio do pacote do tipo *Location*, existe um campo (**type.coding.code**) que define o tipo de setor (UTI, Pronto Atendimento, Unidade de internação, etc.) ao qual o leito pertence. A relação entre as categorias é demonstrada na tabela a seguir (baseado na referência [ServiceDeliveryLocationRoleType - FHIR v4.0.1 (hl7.org)](http://hl7.org/fhir/v3/ServiceDeliveryLocationRoleType/vs.html)):

| Tipo | Descrição                          | Códigos FHIR                   | Contabiliza como ocupação |
| ---- | ---------------------------------- | ------------------------------ | ------------------------- |
| 1    | Pronto Socorro                     | ER / ETU                       | Sim                       |
| 2    | Centro cirúrgico                   | NS / CRS / OMS / SU / PLS / OR | Não**<sup>1</sup>**       |
| 3    | Unidade de Internação              | HU / RHU                       | Sim                       |
| 4    | UTI - Unidade de Terapia Intensiva | ICU / PEDICU / PEDNICU         | Sim                       |
| 5    | Recém-nascido                      | PEDU                           | Sim                       |

Tabela 1: Relação FHIR x Tipos de setores

**1 -** A categoria “Centro Cirúrgico” não é contabilizada na ocupação geral (censo e capacidade), uma vez que não é possível internar um paciente em um leito cirúrgico.

# Definições gerais

Neste tópico, serão apresentados itens gerais de apoio necessários nos demais tópicos.

## *Status* operacional dos leitos

Neste tópico, será apresentado brevemente o conceito de *status* operacional do leito, o qual influencia em diversos cálculos e envio de pacotes. Os *status* operacionais definidos pelo FHIR podem ser verificados no endereço [0116 - FHIR v4.0.1 (hl7.org)](http://hl7.org/fhir/v2/0116/index.html).

Apesar de existirem diversos *status* operacionais, o PFCS permite ao usuário definir o que será considerado como leito bloqueado, disponível ou o que será considerado para cálculo de censo e capacidade. A configuração padrão é a seguinte:

![](media/image8.png)

Independente do *status* operacional do leito, caso haja um paciente vinculado ao mesmo, este será considerado como “ocupado”. Para ser considerado no cálculo do censo e capacidade, a *checkbox* “Total bed” precisa estar marcada. Por sua vez, o item “Census” define se o *status* será considerado como bloqueado, disponível ou não será considerado. Um *status* “bloqueado” não deve ser utilizado para internar pacientes.

O *status* operacional padrão para um leito ocupado, conforme definido no FHIR, é o *status* “O”. Este *status* não permite configuração.

## Combinações do recurso ServiceRequest

Este tópico é utilizado como referência para as combinações de solicitação (*ServiceRequest*) necessárias para que sejam apresentados os dados de maneira correta no PFCS. Existem três códigos principais que definem o tipo de solicitação que está sendo realizada, sendo:

**E0401:** Admissão (pedido de leito)

**E0402:** Transferência (movimentação entre leitos)

**E0405:** Alta (saída do leito)

Este código deve estar no item **code.coding.code** do *ServiceRequest***.** Por sua vez, o que define se a solicitação é apenas um pedido ou se foi concluída é a combinação ***status/intent***. A seguir, uma tabela resumida das possíveis combinações.

| **Tipo**   | **code.coding.code** | **status** | **intent** |
| ---------- | -------------------- | ---------- | ---------- |
| **ADTA05** | E0401                | ACTIVE     | PLAN       |
| **ADTA01** | E0401                | COMPLETED  | ORDER      |
| **ADTA15** | E0402                | ACTIVE     | PLAN       |
| **ADTA02** | E0402                | COMPLETED  | ORDER      |
| **ADTA16** | E0405                | ACTIVE     | PLAN       |
| **ADTA03** | E0405                | COMPLETED  | ORDER      |

Tabela 2: Tipos de solicitações

É importante destacar que, para enviar um **ADTA15** ou **ADTA02** é necessário que, previamente, o paciente já esteja no estabelecimento (**ADTA01**), pois estes tipos se tratam de uma transferência de um leito para outro. O mesmo se aplica para **ADTA16** e **ADTA03**, pois não é possível realizar a alta de um paciente que não esteja previamente internado.

# Demanda Corporativa

Nesta sessão, serão abordados os dados necessários para apresentar informações na função Demanda Corporativa.

![](media/image9.png)

## Censo e Capacidade Geral

O censo e a capacidade geral são, basicamente, a mesma informação, apresentada em dois formatos diferentes. Sendo assim, o mesmo pacote irá afetar ambas. Para exibir as informações em questão é utilizado o pacote de admissão do paciente, o qual, por sua vez, necessita dos recursos *Patient,* *Encounter*, *Location* e *ServiceRequest*. Seguem os campos obrigatórios de cada recurso:

**Patient**

  - **id:** chave de identificação única do paciente. Normalmente utiliza-se o MRN (*Medical Record Number*)

  - **identifier.value:** mesmo valor utilizado em *id*

  - **active:** *status* do registro do paciente

  - **name.family:** sobrenome do paciente

  - **name.given:** nome do paciente

  - **gender:** gênero do paciente

  - **birthdate:** data de nascimento do paciente no formato YYY-MM-DD

  - **maritalStatus.coding.code:** código do estado civil do paciente

  - **managingOrganization.reference:** **chave de identificação única do estabelecimento o qual o paciente está vinculado**

**Encounter**

  - **id:** chave de identificação única do atendimento. Normalmente utiliza-se o número do atendimento

  - **identifier.value:** mesmo valor utilizado em *id*

  - **status:** *status* geral do atendimento

  - **class.code:** código do tipo de atendimento

  - **subject.reference:** chave de identificação única do paciente relacionado ao atendimento

  - **subject.display:** nome completo do paciente relacionado ao atendimento

  - **period.start:** data/hora de início do atendimento

  - **location.location.reference:** chave de identificação única do leito em que o paciente se encontra

  - **location.location.status:** *status* da relação paciente x leito

  - **location.period.start:** data/hora em que o paciente entrou no leito

<!-- end list -->

  - **serviceProvider.reference:** chave de identificação única do estabelecimento o qual o atendimento está vinculado

**Location**

  - Neste caso, utiliza-se os mesmos campos descritos no tópico 1.3.

  - **operationalStatus.code**: deve estar consistente com a configuração descrita no tópico 2.1.

**ServiceRequest**

  - **id:** chave de identificação única do item

  - **identifier.value:** mesmo valor utilizado em *id*

  - **status:** *status* da solicitação

  - **intent:** tipo de solicitação

  - **code.coding.code:** código da solicitação

  - **subject.reference:** chave de identificação única do paciente relacionado a solicitação

  - **encounter.reference:** chave de identificação única do atendimento relacionado a solicitação

  - **authoredOn:** data/hora da solicitação

  - **locationReference.reference:** **chave de identificação única da localização no qual a solicitação está vinculada**

  - **requester.reference:** **chave de identificação única do estabelecimento o qual a solicitação está vinculada**

Verificar a tabela 2, item **ADTA05**, para a combinação de valores necessárias em *ServiceRequest*.

A seguir, um exemplo de pacote:

Após o envio do pacote, será possível visualizar os dados nos campos em destaque na imagem a seguir:

![](media/image11.png)

## Censo PA

Verificar tópico 4.1.1 para inserir os dados. Na sequência, será possível visualizar a informação no campo em destaque na imagem a seguir:

![](media/image12.png)

## Tempo de espera PA

Verificar tópico 4.1.2 para inserir os dados. Na sequência, será possível visualizar a informação no campo em destaque na imagem a seguir:

![](media/image13.png)

## Leitos disponíveis

Verificar tópico 1.3 para inserir os dados e o tópico 2.1 para verificar os *status* dos leitos. Na sequência, será possível visualizar a informação no campo em destaque na imagem a seguir:

![](media/image14.png)

## Leitos bloqueados

O item “leitos bloqueados” apresenta o total geral de leitos que, de acordo com a regra do tópico 2.1, estão definidos para contabilizar como “bloqueados”. No tópico 1.3 é mencionado como enviar pacotes contendo novos leitos.

![](media/image15.png)

## Leitos disponíveis de UTI

Este item remete à mesma lógica do item 3.4, porém com a diferença de ser um totalizador específico da UTI. Sendo assim, serão contabilizados apenas leitos que, no recurso *Location* possuam **type.coding.code com uma das classificações do tipo UTI, conforme descrição da tabela 1.**

![](media/image16.png)

## Leitos de telemetria disponíveis

Este item representa o total de leitos disponíveis que possuam um dispositivo vinculado do tipo “Monitor”. Segue a mesma lógica do tópico 3.4, porém com a adição de um recurso do tipo *Device*, o qual estará vinculado ao leito.

**Device**

  - **id:** chave de identificação única do item

  - **identifier.value:** mesmo valor utilizado em *id*

  - **status:** *status* de uso do dispositivo (inativo, neste caso, significa que não está em uso)

  - **type.text:** descrição do tipo de dispositivo (neste caso, utiliza-se “Monitor”)

  - **location.reference:** chave de identificação única do leito ao qual o dispositivo está vinculado

  - **owner.reference:** chave de identificação única do estabelecimento ao qual o dispositivo está vinculado

A seguir, um exemplo de pacote:

Os leitos disponíveis serão contabilizados conforme exemplificado na imagem a seguir:

 

![](media/image18.png) 

## Admissões (últimas 24h)

Para contabilizar uma admissão como realizada nas últimas 24 horas, é utilizado o mesmo pacote do tópico 3.1. Todavia, serão contabilizados apenas atendimentos que possuam o início do atendimento dentro do prazo (últimas 24h).

**Encounter**

  - **period.start:** data/hora precisa estar dentro do intervalo

![](media/image19.png)

## Altas (últimas 24h)

Para que uma alta seja contabilizada como realizada nas últimas 24h é necessário que o atendimento possua uma data de fim dentro do intervalo em questão. Além disso, só é possível realizar alta de pacientes previamente internados, conforme fluxo descrito no tópico 2.2.

Sendo assim, é necessário um pacote de admissão ter sido enviado previamente, conforme o exemplo a seguir:

Na sequência, é possível enviar um pacote de transferência ou diretamente um pacote de realização de alta. Importante se atentar a algumas diferenças no momento de envio do pacote de alta. Os recursos obrigatórios são *Encounter* e *ServiceRequest*.

**Encounter**

  - **period.end:** data/hora de fim do atendimento

  - **location.period.end:** data/hora em que o paciente deixou o leito

**ServiceRequest**

Utilizar a combinação **ADTA03** informada na tabela 2.

A seguir, o exemplo de um pacote de alta:

Será possível visualizar a quantidade de altas realizadas no período, conforme campo em destaque na imagem a seguir:

![](media/image22.png)

## Capacidade (Histograma)

O histograma apresenta a ocupação hospitalar geral das últimas cinco horas, ocupação atual e predição de ocupação para as próximas 12 horas. Para ser possível visualizar as informações, é necessário enviar pacotes do tipo internação de tempo em tempo ou validar a data/hora de início/fim do recurso *Encounter* e data/hora do recurso *ServiceRequest*. Para isso, utiliza-se o mesmo pacote do tópico 3.1, atentando-se aos itens descritos na sequência.

**Encounter**

  - **period.start:** data/hora de início do atendimento (necessita estar dentro do itervalo)

  - **period.end:** data/hora de fim do atendimento – em caso de alta (necessita estar dentro do intervalo)

**ServiceRequest**

  - **dtAuthoredOn:** data/hora em que a solicitação foi realizada (necessita estar dentro do intervalo)

A seguir, uma imagem de exemplo do histograma:

> ![](media/image23.png)

# Priorização de Admissões 

Nesse modulo, serão abordados os dados sobre todos as admissões dentro do hospital, bem como dados referente ao Pronto Atendimento e ao Centro Cirúrgico.

![](media/image24.png)

## *Card* de informações gerais

Esse *card* exibe as informações úteis para a Priorização de Admissões. Algumas dessas informações são relacionadas apenas ao PA, como por exemplo, o censo PA e a quantidade de leitos disponíveis no PA. Além disso, também é possível visualizar o total de admissões que é uma informação relacionado a todos os departamentos do hospital selecionado. Assim, no próximo tópico os itens serão abordados de maneira detalhada, pois, conforme são enviados pacotes para exibir itens na tela central do módulo, as informações deste *card* são atualizadas.

![](media/image25.png)

### Capacidade e Censo

Capacidade e Censo do PA, como havia sido referenciado, são, relativamente, as mesmas informações, porém, apresentadas de formas diferentes, sendo assim o mesmo pacote irá impactar em ambas.

![](media/image26.png)

Para exibir as informações em questão é utilizado o pacote de admissão do paciente, o qual, por sua vez, necessita dos recursos *Patient,* *Encounter*, *Location* e *ServiceRequest*. Seguem os campos obrigatórios de cada recurso:

**Patient**

  - Nesse caso, utilizam-se os mesmos campos descritos no tópico 3.1

**Location**

  - **operationStatus.code (O-Occupied):** especifica o *status* do leito

  - **type.coding.code (ER – Emergency room):** especifica o setor correspondente do leito

**Encounter**

  - **status (Arrived):** *status* geral do atendimento

  - **class.code (Inpatient or emergency):** código do tipo de atendimento

**Server Request**

  - utilizar a referência **ADTA01** da tabelala 1

A seguir, um exemplo de pacote:

### Tempo de espera PA

Nesse indicador é apresentado o tempo médio de permanência atual de pacientes do PA. O pacote utilizado é o mesmo pacote do tópico 4.1.1. Será analisado o início do atendimento em relação ao horário atual. É importante salientar que são considerados apenas pacientes que estejam em leitos do tipo Pronto Socorro, conforme tabela 1.

![](media/image28.png)

### Leitos disponíveis no PA

Verificar tópico 4.1.1 para inserir os dados. Na sequência, será possível visualizar a informação no campo, em destaque na imagem a seguir:

![](media/image29.png)

### Total admissiões

Representa todas as solicitações de pacientes que pretendem entrar no hospital, com código do tipo do atendimento ***Inpatient***.

![](media/image30.png)

Para exibir as informações em questão, tem que solicitar a admissão do paciente (ADTA05). Serão necessários os recursos *Patient,* *Encounter*, *Location* e *ServiceRequest*. Seguem os campos obrigatórios de cada recurso:

**Patient**

  - Nesse caso, utilizam-se os mesmos campos descritos no tópico 3.1

**Location**

  - **operationStatus.code (U-Unoccupied):** especifica o *status* do leito

**Encounter**

  - **status (Planned or Arrived):** *status* geral do atendimento

  - **class.code (Inpatient):** código do tipo de atendimento

  - **Não** contém **location** no recurso, pois o paciente ainda não está no leito

**Service Request**

  - utilizar a referência **ADTA05** da tabela 2

A seguir, um exemplo de pacote:

## Pronto Atendimento

Nesse módulo, são tratadas as admissões unicamente de setores de Pronto Atendimento. Em seguida, serão apresentados os *cards* pertencentes a essa região.

![](media/image31.png)

### Censo e Capacidade do PA

Verificar tópico 4.1.1 para inserir os dados. Na sequência, será possível visualizar a informação no campo, em destaque na imagem a seguir:

![](media/image32.png)

###  Pedidos de internação no PA

São todos os pedidos de transferência para o PA.

![](media/image33.png)

Para exibir as informações em questão, tem que admitir o paciente (ADTA01), em seguida, solicitar a transferência (ADTA15) para o PA. Sendo assim, é necessário um pacote de admissão ter sido enviado previamente, conforme o exemplo a seguir:

Na sequência, é possível enviar um pacote de tranferência. Importante atentar a algumas diferenças no momento de envio do pacote de transferência. Os recursos obrigatórios são: Location e ServiceRequest.

Seguem os campos obrigatórios de cada recurso:

**Location**

  - **operationStatus.code (U-Unoccupied):** especifica o *status* do leito

  - **type.coding.code (ER – Emergency room):** especifica o setor correspondente do leito

**Service Request**

  - utilizar a referência **ADTA15** da tabela 2

A seguir, um exemplo de pacote:

### *Status* do PA

O comportamento do card “*Status* do PA” abarca quatro indicadores, “Admissões potenciais”, “Paciente casual no PA”, “Em observação/Aguardando” e “Capacidade”. Cada indicador tem o seu recurso correspondente.

![](media/image36.png)

#### Admissões potenciais

Trata de todos os pacientes admitidos que contêm a informação do nível de urgência no atendimento (ESI).

![](media/image37.png)

Para exibir as informações em questão, por exemplo, para admissão do paciente (ADTA01), deverá ser acompanhado com um valor do ESI no recurso do *Encounter*. Serão necessários os recursos *Patient,* *Encounter*, *Location* e *ServiceRequest*. Seguem os campos obrigatórios de cada recurso:

**Patient**

  - Nesse caso, utiliza-se os mesmos campos descritos no tópico 3.1

**Location**

  - **operationStatus.code (O-Occupied):** especifica o *status* do leito

  - **type.coding.code (ER – Emergency room):** especifica o setor correspondente do leito

**Encounter**

  - **status (Arrived):** *status* geral do atendimento

  - **class.code (Inpatient):** código do tipo de atendimento

  - **extension.value.code:** especifica o nível de urgência do atendimento (ESI), os valores estão entre 0 e 5

**Server Request**

  - utilizar a referência **ADTA01** da tabela 2

A seguir, um exemplo de pacote:

#### Paciente casual no PA

Representa todos os possíveis pacientes que poderão pertencer ao PA, contabilizado por um intervalo de tempo configurável na função “pfcs\_configurações” na *tab* “configurações” opção “cadastro de regras de tempo máximo de admissão em leito”.

![](media/image39.png)

Para exibir as informações em questão, tem que solicitar a admissão do paciente (ADTA05), que será considerado dentro do intervalo configurado. Serão necessários os recursos *Patient,* *Encounter*, *Location* e *ServiceRequest*. Seguem os campos obrigatórios de cada recurso:

**Patient**

  - Nesse caso, utiliza-se os mesmos campos descritos no tópico 3.1

**Location**

  - **operationStatus.code (U-Unoccupied):** especifica o *status* do leito

  - **type.coding.code (ER – Emergency room):** especifica o setor correspondente do leito

**Encounter**

  - **status (Planned or Arrived):** *status* geral do atendimento

  - **class.code (Inpatient):** código do tipo de atendimento

**Service Request**

  - utilizar a referência **ADTA05** da tabela 2

A seguir, um exemplo de pacote:

#### Em observação/Aguardando

São todos os pacientes que já foram admitidos com alguma observação prévia.

![](media/image41.png)

Para exibir as informações em questão, por exemplo, para admissão do paciente (ADTA01), deverá ser acompanhado com o recurso do *Observation*. Serão necessários os recursos *Patient,* *Encounter*, *Location, Observation* e *ServiceRequest*. Seguem os campos obrigatórios de cada recurso:

**Patient**

  - Nesse caso, utiliza-se os mesmos campos descritos no tópico 3.1

**Location**

  - **operationStatus.code (O-Occupied):** especifica o *status* do leito

  - **type.coding.code (ER – Emergency room):** especifica o setor correspondente do leito

**Encounter**

  - Nesse caso, utiliza-se os mesmos campos descritos no tópico 3.1

**Observation**

  - **id:** chave de identificação única do item

  - **identifier.value:** mesmo valor utilizado em *id*

  - **status:** estado da solicitação

  - **code.coding.code:** código da observação

  - **subject.reference:** chave de identificação única do paciente relacionado a observação

  - **encounter.reference:** chave de identificação única do atendimento relacionado a observação

  - **effectiveDateTime:** data/hora da observação

**Service Request**

  - utilizar a referência **ADTA01** da tabela 2

A seguir, um exemplo de pacote:

#### Capacidade

Verificar tópico 3.10 para inserir os dados. Na sequência, será possível visualizar a informação no campo em destaque na imagem a seguir:

![](media/image43.png)

## Admissões no hospital

Nesse módulo, trata-se sobre as admissões referentes a todo o hospital. Em seguida, serão apresentados os *cards* pertencentes a essa região

![](media/image44.png)

### Admissões diretas

Todos os pacientes admitidos diretamente no PA

![](media/image45.png)

Para exibir as informações em questão, tem que admitir o paciente (ADTA01) diretamente, independente do setor. Serão necessários os recursos *Patient,* *Encounter*, *Location* e *ServiceRequest*. Os campos obrigatórios são os mesmos que o censo, descritos no tópico 3.1, com exceção do código do tipo do atendimento que tem que ser ***Inpatient***.

**Encounter**

  - **class.code (Inpatient):** código do tipo de atendimento

A seguir, um exemplo de pacote:

### Transferências

Todos os pacientes admitidos que foram transferidos de um outro estabelecimento.

![](media/image47.png)

Para exibir as informações em questão, tem que admitir o paciente (ADTA01), deverá ser acompanhado com o campo *Encounter.hospitalization.admitSource* igual a ***hosp-trans***, recurso do *Encounter*. Serão necessários os recursos *Patient,* *Encounter*, *Location* e *ServiceRequest*.

Seguem os campos obrigatórios de cada recurso:

**Patient**

  - Nesse caso, utilizam-se os mesmos campos descritos no tópico 3.1

**Location**

  - **operationStatus.code (O-Occupied):** especifica o *status* do leito

  - **type.coding.code (ER – Emergency room):** especifica o setor correspondente do leito

**Encounter**

  - **status (Arrived or Planned):** *status* geral do atendimento

  - **class.code (Inpatient):** código do tipo de atendimento

  - **hospitalization.admitSource(host-trans):** de onde o paciente foi admitido, referente à transferência

**Server Request**

  - utilizar a referência **ADTA01** da tabela 2

A seguir, um exemplo de pacote:

### Total de leitos disponíveis

Verificar tópico 3.4 para inserir os dados. Na sequência, será possível visualizar a informação no campo em destaque na imagem a seguir:

![](media/image49.png)

### Admissões

O card admissões abrange quatro indicadores, separadamente, que são: Capacidade, Leitos disponíveis, Admissões e Altas, agrupandos por departamentos.

![](media/image50.png)

#### Capacidade 

Verificar tópico 3.1 para inserir os dados. Na sequência, será possível visualizar a informação no campo em destaque na imagem a seguir:

![](media/image51.png)

#### Leitos disponíveis

Verificar tópico 3.4 para inserir os dados. Na sequência, será possível visualizar a informação no campo em destaque na imagem a seguir:

![](media/image52.png)

#### Admissões

Verificar tópico 4.1.4 para inserir os dados. Na sequência, será possível visualizar a informação no campo em destaque na imagem a seguir:

![](media/image53.png)

#### Altas

Verificar tópico 3.9 para inserir os dados, contudo, deve ser desconsiderado o intervalo de 24 horas. Na sequência, será possível visualizar a informação no campo em destaque na imagem a seguir:

![](media/image54.png)

## Status PA card esquerdo

Este modulo abarca diversos indicadores que já foram descritos anteriormente, portanto, será feita referência somente dos cards que ainda não foram descritos.

![](media/image55.png)

### Atraso na admissão do paciente

Apresenta pacientes com pedido de transferência (tópico 4.2.2) em atraso, conforme regra definida pelo usuário na função **PFCS – Configurações**. É analisado a diferença entre a data/hora da realização da solicitação e a data/hora atual e, então, comparada a informação com a configuração definida. Caso esteja dentro da regra, os pacientes serão contabilizados e apresentados na interface, conforme exemplo a seguir:

![](media/image56.png)

### Admissões no centro cirúrgico

Apresenta pacientes com solicitações de admissão no centro cirúrgico (CC) (tópico 4.3.4.3), neste caso é importante reforçar que o leito que o paciente irá solicitar será um leito do departamento do centro cirúrgico.

![](media/image57.png)

Os recursos obrigatórios são: *Patient,* *Encounter*, *Location* e *ServiceRequest*. Seguem os campos obrigatórios de cada recurso:

**Location**

  - **operationStatus.code (U- Unoccupied):** especifica o *status* do leito

  - **type.coding.code (SU – Surgery clinic):** especifica o setor correspondente do leito

**Encounter**

  - **status (Arrived or Planned):** *status* geral do atendimento

  - **class.code (Inpatient):** código do tipo de atendimento

**Server Request**

  - utilizar a referência **ADTA01** da tabela 2

A seguir, um exemplo de pacote:

### Atraso no PA

Apresenta pacientes com pedido de alta (tópico 4.3.4.4) em atraso, correspondente ao departamento do Pronto Atendimento, conforme regra definida pelo usuário na função **PFCS – Configurações**. É analisado a diferença entre a data/hora de realização da solicitação e a data/hora atual e, então, comparada a informação com a configuração definida. Caso esteja dentro da regra, os pacientes serão apresentados na interface, conforme exemplo a seguir:

![](media/image59.png)

Sendo assim, é necessário um pacote de admissão ter sido enviado previamente, conforme o exemplo a seguir:

Na sequência, é possível enviar um pacote de realização de alta. Importante se atentar a algumas diferenças no momento de envio do pacote de alta. O recurso obrigatório é *ServiceRequest*, utilizar ainda a combinação **ADTA16** informada na tabela 2.

A seguir, o exemplo de um pacote de alta:

Será possível visualizar a quantidade de altas realizadas no período, conforme campo em destaque na imagem a seguir:

### Atrasos de Alta

Apresenta pacientes com pedido de alta (tópico 4.4.3). Caso esteja dentro da regra, os pacientes serão contabilizados e apresentados na interface, conforme exemplo a seguir:

![](media/image62.png)

### Disposição média para o tempo de admissão

Representa a média de tempo de solicitações de internação, considerando somente leitos de classificações do tipo emergência, do tipo 3, 4 e 5 conforme descrição da tabela 1.

![](media/image63.png)

Portanto, será enviado uma solicitação de admissão ADTA05, que deverá ser acompanhada com o campo *Encounter.hospitalization.admitSource* igual a ***emd***, recurso do *Encounter*. Serão necessários os recursos *Patient,* *Encounter*, *Location* e *ServiceRequest*.

Seguem os campos obrigatórios de cada recurso:

**Location**

  - **operationStatus.code (U-Unoccupied):** especifica o *status* do leito

  - **type.coding.code: tipo 3, 4 e 5 conforme descrição da tabela 1**

**Encounter**

  - **status (Arrived or Planned):** *status* geral do atendimento

  - **class.code (Inpatient):** código do tipo de atendimento

  - **hospitalization.admitSource(emd):** de onde o paciente foi admitido, referente à transferência

  - **Não** contém **location** no recurso, pois o paciente ainda não está no leito

**Server Request**

  - **dtAuthoredOn:** data do pedido

<!-- end list -->

  - utilizar a referência **ADTA05** da tabela 2

A seguir, um exemplo de pacote:

### Tempo médio para o centro cirúrgico

Representa a média de tempo entre a transferência do departamento do PA para um departamento do centro cirúrgico.

![](media/image65.png)

Para inserir valores no *card*, previamente precisa internar o paciente num leito pertencente ao departamento do PA (ADTA01), conforme tópico 4.4.3.

Na sequência, é possível enviar um pacote de transferência para o Centro Cirúrgico. Importante se atentar a algumas diferenças no momento de envio do pacote de transferência. Os recursos obrigatórios são *Location* e *ServiceRequest*.

**Location**

  - **operationStatus.code (O-Occupied):** especifica o *status* do leito

  - **type.coding.code: tipo 2 conforme descrição da tabela 1**

**ServiceRequest**

  - Utilizar a combinação **ADTA02** informada na tabela 2.

A seguir, o exemplo de um pacote de alta:

### Tempo médio de permanência

Apresenta o tempo médio de pacientes com pedido de internação (tópico 4.3.4.3) em atraso, conforme regra definida pelo usuário na função **PFCS – Configurações**. É analisado a diferença entre a data/hora da realização da solicitação e a data/hora atual e, então, comparada a informação com a configuração definida. Caso esteja dentro da regra, a média de tempo será apresentada na interface, conforme exemplo a seguir:

![](media/image67.png)

# *Critical Care*

O módulo Critical Care tem foco em apresentar informações gerais sobre setores do tipo UTI. Ao entrar no módulo, são apresentados dados em destaque no *card* localizado na região esquerda da tela e informações específicas por setor na região principal.

## *Card* de informações gerais

Este *card* exibe as informações gerais de ocupação dos setores do tipo UTI. Basicamente um agrupamento das informações exibidas na lista de setores. Sendo assim, no próximo tópico os itens serão abordados de maneira detalhada, pois, conforme são enviados pacotes para exibir itens na tela central do módulo, por consequência, as informações deste *card* são atualizadas.

![](media/image68.png)

## Lista de setores

No módulo Critical Care, a região central exibe diversas informações de cada um dos setores do tipo UTI do estabelecimento selecionado e, ao selecionar o setor, será exibida uma tela com mais detalhes das informações. Neste tópico serão detalhados os pacotes utilizados para apresentar cada item e seus respectivos detalhes.

![](media/image69.png)

### Capacidade e censo

Conforme mencionado no tópico 3.1, a capacidade e o censo trabalham em conjunto e há regras que impactam os cálculos, conforme descrito no tópico 2.1. Os campos obrigatórios são os mesmos, porém, para apresentar alguns detalhes adicionais, serão necessários outros recursos no pacote. Sendo assim, os itens “extra” com relação ao tópico 3.1, serão detalhados a seguir.

**Encounter**

  - **reasonCode.coding.code:** código do diagnóstico

  - **reasonCode.coding.display:** diagnóstico de forma descritiva

  - **participant.individual.reference:** chave de identificação única de um profissional responsável pelo atendimento (geralmente o médico principal)

**Flag**

O recurso Flag pode ser utilizado de várias maneiras e, para cada caso, a informação será exibida em uma coluna diferente. Também é possível enviá-lo diversas vezes no mesmo pacote, como todo recurso. Os campos obrigatórios e necessários se mantêm os mesmos. No exemplo de pacote mais adiante será possível perceber que o recurso está sendo utilizado duas vezes, sendo uma para o item *Code Status* e outra para o item Requisição Especial.

A requisição especial abrange qualquer informação que esteja na categoria **SR100 (category.coding.code)**. A descrição da requisição, por sua vez, encontra-se em **code.coding.display** e pode ser qualquer texto.

Já o *Code Status* possui, no momento, apenas 4 opções, sendo: *DNI*, *DNR*, *OTHER* e *FULL.*

  - **id:** chave de identificação única do item

  - **identifier.value:** mesmo valor utilizado em *id*

  - **status:** *status* da *flag*

  - **category.coding.code:** código da categoria

  - **category.coding.display:** descrição da categoria

  - **code.coding.code:** código da *flag*

  - **code.coding.display:** descrição da *flag*

  - **subject.reference:** chave de identificação única do paciente vinculado à *flag*

  - **subject.identifier.value:** valor do item *subject.reference*

  - **encounter.reference:** chave de identificação única do atendimento vinculado à *flag*

**Procedure**

O recurso *Procedure* é utilizado para enviar procedimentos gerais realizados (como, por exemplo, exames laboratoriais) e o *status* do procedimento (em progresso, completo, etc.). É possível enviar diversos itens para o mesmo paciente/atendimento. Todavia, apenas as categorias dos procedimentos serão apresentadas no PFCS.

  - **id:** chave de identificação única do item

  - **identifier.value:** mesmo valor utilizado em *id*

  - **status:** *status* do progresso geral do procedimento

  - **category.coding.code:** código da categoria

  - **category.coding.display:** descrição da categoria

  - **code.coding.code:** código do procedimento

  - **code.coding.display:** descrição do procedimento

  - **subject.reference:** chave de identificação única do paciente vinculado ao procedimento

  - **encounter.reference:** chave de identificação única do atendimento vinculado ao procedimento

  - **performedPeriod.start:** data/hora de início do procedimento

  - **performedPeriod.end:** data/hora de fim do procedimento (apenas necessário para prever a finalização ou quando realmente foi finalizado)

  - **reasonCode.coding.code:** código do motivo de realização do procedimento

  - **reasonCode.coding.display:** descrição do motivo de realização do procedimento

**Practitioner**

Como visto no recurso *Encounter*, é possível referenciar um profissional responsável pelo atendimento. Esta referência está diretamente ligada ao recurso *Practitioner*.

  - **id:** chave de identificação única do item

  - **identifier.value:** mesmo valor utilizado em *id*

  - **name.family:** sobrenome do médico

  - **name.given:** nome do médico

  - **name.prefix:** pronome de tratamento (abreviatura)

**PhysicianRoleID**

Além de adicionar o profissional responsável, como visto, é necessário vinculá-lo a um cargo, ou seja, definir que aquele profissional é um médico, enfermeiro, etc. Para isso, utiliza-se este recurso.

  - **practitioner.reference:** chave de identificação única do profissional vinculado à este cargo

  - **organization.reference:** chave de identificação única do estabelecimento vinculado à este cargo

  - **code.coding.code:** código responsável por definir o tipo do cargo (para médico principal do atendimento utiliza-se o código 405279007)

A seguir, um exemplo de pacote:

Após envio do pacote, será possível visualizar a informação geral na tela central, conforme imagem a seguir:

![](media/image71.png)

Na tela de detalhes, por sua vez, estarão presentes as informações de todas as colunas:

![](media/image72.png)

### Leitos disponíveis

Este item remete à mesma lógica do item 3.4, porém com a diferença de ser um totalizador específico da UTI. Sendo assim, serão contabilizados apenas leitos que, no recurso *Location* possuam **type.coding.code com uma das classificações do tipo UTI, conforme descrição da tabela 1.**

![](media/image73.png)

### Leitos bloqueados

Este item remete à mesma lógica do item 3.5, porém com a diferença de ser um totalizador específico da UTI. Sendo assim, serão contabilizados apenas leitos que, no recurso *Location* possuam **type.coding.code com uma das classificações do tipo UTI, conforme descrição da tabela 1.**

![](media/image74.png)

### Pedidos de admissão

O pedido de admissão se baseia na combinação do recurso *ServiceRequest* **ADTA01** descrito na tabela 2. O pacote é bem semelhante ao pacote utilizado no tópico 5.2.1, com pequenas modificações. Em um fluxo convencional, este pacote seria enviado primeiro e, na sequência, a admissão seria efetivada alterando-se a combinação dos itens em *ServiceRequest*.

Apenas alguns itens requerem maior atenção, sendo o *status* operacional do leito, a data do pedido de admissão e a ausência do item *location* no recurso *Encounter*, que são informações “extra” que serão apresentadas na interface.

São contabilizados pedidos de admissão diretos ou pedidos de transferência de outra unidade qualquer para esta. O pedido de transferência será abordado com maiores detalhes no tópico 5.2.7.

**ServiceRequest**

  - **dtAuthoredOn:** data do pedido

**Location**

  - **operationalStatus.code:** código do *status* operacional atual do leito

**Encounter**

  - **Não** contém **location** no recurso, pois o paciente ainda não está no leito

Segue um exemplo de pacote:

Os registros serão visíveis conforme imagem a seguir:

![](media/image76.png)

Importante lembrar que a coluna Paciente Recorrente é uma informação que vem dos algoritmos e a coluna Tempo de Espera é a diferença entre a data/hora atual e o momento em que o pedido foi realizado.

### Tempo média de espera

O tempo médio de espera está diretamente relacionado ao item anterior. Aqui é apresentada uma média do tempo em que os pacientes estão esperando por um leito. Na tela de detalhes de “Pedidos de admissão”, existe uma coluna chamada “Tempo de espera”. O tempo médio é diretamente a média geral da soma dos itens daquela coluna. A seguir, um exemplo:

![](media/image77.png)

### Requisições especiais

A tela de requisições especiais do módulo *Critical Care* apresenta um agrupamento de todos os pacientes atuais internados em um setor do tipo UTI ou que possuem um pedido de admissão no setor e possuem, ao menos, uma requisição especial. Para isso, basta o pacote conter uma *Flag* com a categoria correta, conforme já mencionado no tópico 5.2.1.

A seguir, um exemplo da interface:

![](media/image78.png)

### Pedidos de transferência

Este item apresenta todos os pacientes internados nos setores do tipo UTI que possuem um pedido de transferência ativo, ou seja, ainda estão aguardando a transferência para outro leito e/ou setor. Sendo assim, como mencionado, o paciente precisa estar previamente internado para que o pedido de transferência seja realizado, conforme fluxo descrito ao final do tópico 2.2.

O primeiro pacote, então, segue o mesmo padrão do pacote utilizado no tópico 5.2.1. Na sequência, o pacote de pedido de transferência, necessita ter, obrigatoriamente, o recurso *ServiceRequest*, contendo a combinação **ADTA15**, conforme tabela 2.

Segue um exemplo simples de transferência:

Os pacientes com pedido de transferência ativo poderão ser visualizados conforme a imagem a seguir:

![](media/image80.png)

### Atrasos

O item “Atrasos” apresenta pacientes com pedido de transferência (tópico 5.2.7) em atraso, conforme regra definida pelo usuário na função **PFCS – Configurações**. É analisado a diferença entre a data/hora de realização do período e a data/hora atual e, então, comparada a informação com a configuração definida. Caso esteja dentro da regra, os pacientes serão apresentados na interface, conforme exemplo a seguir:

![](media/image81.png)
