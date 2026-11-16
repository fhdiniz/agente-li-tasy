![](media/image1.jpeg)

> **AVISO**
> 
> O conteúdo deste documento é de propriedade exclusiva da Philips e está sujeito a alterações sem aviso prévio.
> 
> Esta cópia deverá ser protegida contra divulgações indevidas, como cópia da documentação eletrônica, impressa ou parte dela, não deverá ser emprestada, reproduzida ou vendida.
> 
> Todos os nomes de empresas, produtos, marcas comerciais, pessoas, personagens, dados ou situações, citados neste documento são fictícios e tem somente objetivo didático.
> 
> **2 Sumário**

[1 Objetivo do documento 3](#objetivo-do-documento)

[1.1 Público 3](#público)

[2 Requisitos Necessários para a Integração 3](#requisitos-necessários-para-a-integração)

[2.1 Infraestrutura 3](#infraestrutura)

[3 Configurações e Parametrizações no Sistema 4](#configurações-e-parametrizações-no-sistema)

[3.1 Importar 4](#_Toc145059688)

[3.2 Configurar rotas 6](#configurar-rotas-tie)

[4 Possiveis problemas TIE 8](#possiveis-problemas-tie)

[4.1 Problema ao importar os arquivos philips-tie-siapi.bft 8](#problema-ao-importar-os-arquivos-philips-tie-siapi.bft)

[4.2 Problema na chamada da API retornando erro 404 8](#problema-na-chamada-da-api-retornando-erro-404)

[5 Configurar Mappers 8](#configurar-mappers)

[5.1 TARGET 8](#target)

[5.2 SOURCE 9](#source)

[5.3 Mappings 9](#mappings)

[6 Funcionamento integração 10](#funcionamento-integração)

[6.1 JOB INTERNACAO\_API\_TIE 10](#job-internacao_api_tie)

[6.2 Processo e controle dos dados 10](#processo-e-controle-dos-dados)

[6.3 Eventos de logs da integração no Tasy 11](#eventos-de-logs-da-integração-no-tasy)

# Objetivo do documento

> Disponibilizar as informações no formato passo a passo de como configurar o TIE – Bifrost, após receber o pacote com os arquivos de API para importação no ambiente desejado.

# Público

> Setor que mantem e configura o ambiente de sistemas Philips.

# Requisitos Necessários para a Integração

> Abaixo estão descritos os requisitos mínimos necessários a nível de infraestrutura e sistema para que as Integrações ocorram com sucesso.

# Infraestrutura

> Tasy Interface Engine e Tasy Interfaces.

# Configurações e Parametrizações no Sistema

> Os sistemas Tasy, Tasy Interface Engine e Tasy Interfaces devem estar funcionando com IP e PORT liberados constando o status de 200 OK. Essa verificação poderá ser realizada ao concluir toda instalação e configuração seguindo os manuais de apoio.

<span id="_Toc145059688" class="anchor"></span>

# Cadastros PEP

> Através do sistema Tasy, realizar a importação do template na função Cadastros PEP, aba Templates, conforme imagens abaixo.
> 
> ![A screenshot of a computer Description automatically generated](media/image3.png)
> 
> ![A screenshot of a computer Description automatically generated](media/image4.png)
> 
> ![A screenshot of a computer Description automatically generated](media/image5.png)

# Gerenciamento para Integração

> Através da função Gerenciamento para Integração \> Conversão de dados no sistema Tasy, realizar o cadastro da Regra de conversão para o SIAPI, utilizando das sequências geradas na importação do template na etapa anterior (Cadastros PEP).
> 
> ![A screenshot of a computer Description automatically generated](media/image6.png)

# Importar artefatos TIE

> Através do sistema TIE realizar a importação dos artefatos, anexados na OS ao concluir o projeto.

1.  Opção de importar:

> Abrir o TIE pelo navegador e clicar na opção importar, como destacado em amarelo na [Figura 1](#_bookmark6).
> 
> <span id="_bookmark6" class="anchor"></span>Figura 1 – Importar

![](media/image7.png)

2.  Carregar arquivo e importar no TIE:

> Clicar na opção Load file, escolher o arquivo philips-tie-siapi.bft com o pacote de importação, clicar em Importar e verificar a mensagem de importação realizada com sucesso, assim como destacado na [Figura 2](#_bookmark7).
> 
> <span id="_bookmark7" class="anchor"></span>Figura 2 – Carregar arquivo e importar

![](media/image8.png)

# Configurar rotas TIE

> Toda vez que novas API forem liberadas via pacote de importação do TIE, as rotas devem ser configuradas conforme endereçamento interno.

1.  Configuração da rota:

> Clicar na opção Manegement do menu lateral esquerdo, clicar em Routes, na aba que abrir clicar na opção Configure da rota desejada, assim como destacado na [Figura 3](#_bookmark9).
> 
> <span id="_bookmark9" class="anchor"></span>Figura 3 - Rotas

![](media/image9.png)

2.  Página de configuração da rota:

> Veirifcar se a opção Active está como Yes, alterar e/ou adiconar o host e port, para o host configurar o IP referente ao endereço do tasy-interfaces, na port configurar a porta do IP/Endereço http do tasy-interfaces, também a url da API externa para configuração do endpoint SIAPI assim como destacado na [Figura 4](#_bookmark10).
> 
> Figura 4 – Configuração da rota

![](media/image10.png)

# Possiveis problemas TIE

> Durante o processo de importação e/ou testes das API poderá ocorrer possiveis problemas, essa seção destina-se a identifica-los e soluciona-los.

# Problema ao importar os arquivos philips-tie-siapi.bft

> Caso ocorra algum problema na importação dos arquivos, provavelmente poderá estar relacionado a arquivos faltantes no pacote.
> 
> Necessário enviar via OS o problema documentado e solicitar novo pacote de arquivos, descrevendo os arquivos faltantes, informados na tela no momento do erro.

# Problema na chamada da API retornando erro 404

> Ao chamar uma API poderá ocorrer erro de 404 not found, esse problema poderá estar atrelado ao TIE e/ou tasy-interfaces, sendo eles:

1.  Rota não configurada ou com HOST/PORT incorretos: Verificar instrução como visto na [Figura 4](#_bookmark10).

# Configurar Mappers

> Os mappings são necessários para que haja compatibilidade entre alguns tipos que são diferentes entre o cliente e o Tasy.
> 
> Os mappings em questão foram baseados de acordo com o arquivo de tabelas informados pelo cliente na documentação e na LI.
> 
> Para que o ID de um determinado campo seja equivalente ao ID no Tasy é feito esse mapping e, dessa forma, tanto do cliente para o Tasy quanto ao contrário, a informação chegue de forma precisa para o banco de dados.
> 
> Há dois tipos de mappgins: target e souce.

# TARGET

> É o tipo de mapping o qual leva em consideração o dado terceiro origem do cliente para o Tasy destino, assim sendo, tendo que passar qual o tipo valor chegará e qual será o tipo de valor que será enviado ao Tasy.
> 
> Na figura a seguir se refere a configuração inicial (já feita) que informa que esse mapping será do cliente para o Tasy.

![](media/image11.png)

> Na figura, na aba "mapping table", temos:

1.  O valor de input origem que será o valor que virá do cliente conforme sua própria base.

2.  O valor de output destino que será o valor correspondente no Tasy para aquele tipo do cliente.

3.  A descrição do referido valor.

![](media/image12.png)

# SOURCE

> É tipo de dado que, ao contrário do Target, recebe a informação correspondente na base do Tasy e converte para o tipo correspondente na base do cliente.
> 
> O processo ocorre igual ao Target, com a diferença de:

1.  No valor de input irá o valor do Tasy conforme a sua base.

2.  No output irá o valor correspondente na base do cliente.

> Preencha os valores de acordo com a necessidade de cada mapping. Sempre haverá um exemplo para poder ser seguido.

# Mappings

> Do Cliente no Input Value para o Tasy no Output Value:
> 
> api.siapi.sexo.target
> 
> api.siapi.estadoCivil.target
> 
> api.siapi.tipoTelefone.target
> 
> api.siapi.motivoInternacao.target
> 
> api.siapi.justificativaInvoluntariedade.target
> 
> api.siapi.diasInternacao.target
> 
> api.siapi.capacidadeCivilPacienteInterditadoCuratelado.target
> 
> api.siapi.tipoBeneficio.target
> 
> api.siapi.faixaDeValor.target
> 
> api.siapi.status.target
> 
> api.siapi.justificativaAlta.target
> 
> api.siapi.responsavelSolicitacaoAlta.target
> 
> api.siapi.motivoSaidaEstabelecimentoSaude.target
> 
> api.siapi.nacionalidade.target
> 
> api.siapi.siglasUFs.target
> 
> Do Tasy no Input Value para o Cliente no Output Value:
> 
> api.siapi.sexo.source
> 
> api.siapi.estadoCivil.source
> 
> api.siapi.tipoTelefone.source
> 
> api.siapi.motivoInternacao.source
> 
> api.siapi.justificativaInvoluntariedade.source
> 
> api.siapi.diasInternacao.source
> 
> api.siapi.capacidadeCivilPacienteInterditadoCuratelado.source
> 
> api.siapi.tipoBeneficio.source
> 
> api.siapi.faixaDeValor.source
> 
> api.siapi.status.source
> 
> api.siapi.justificativaAlta.source
> 
> api.siapi.responsavelSolicitacaoAlta.source
> 
> api.siapi.motivoSaidaEstabelecimentoSaude.source
> 
> api.siapi.nacionalidade.source
> 
> api.siapi.siglasUFs.source

6.  # Funcionamento integração
    
    1.  # JOB INTERNACAO\_API\_TIE

> O job INTERNACAO\_API\_TIE deverá ser configurado conforme necessidade, parâmetros a serem configurados na chamada da procedure - CONS\_ATENDPAC\_INTERALTA:

1)  NR\_SEQ\_CLASSIFICACAO\_P – Sequência da Classificação do atendimento, pode ser enviado no formato de lista texto - String com as sequências separadas por vírgula, exemplo ‘1,2,3,4,5’.

2)  IE\_TIPO\_ATENDIMENTO\_P – Tipo do atendimento desejado, pode ser enviado no formato de lista texto - String com as sequências separadas por vírgula, exemplo ‘1,2,3,4,5’.

3)  QT\_DIAS\_P – Quantidade dejada de dias iniciais anteriores a data atual para buscar os dados de internação, exemplo 30 dias, caso não informado será considerado 1 dia.
    
    1.  #  Processo e controle dos dados

> Os dados de internações, altas e retificações serão controlador e gravados na pool para posteriormente
> 
> serem processados.
> 
> A cada entrada de uma internação, alta, alteração de dados na internação ou alta, os dados serão gravados na pool de requisições, ao executar o job supracitado essa pool será processada e para cada registro será requisitado o endpoint externo correspondente da API SIAPI. O retorno será tratado e gravado log com as infomações de atendimento, sequência da internação/alta/retificação, assim como informações de erros caso ocorram.

# Eventos de logs da integração no Tasy

> Acesso a tela com os logs da integração, caminho Regulação de Atendimentos \> Regulação SIAPI.

1)  Filtro por Número do atendimento;

2)  Filtro por Data da internação;

3)  Filtro por Data do envio;

4)  Filtro por Data do erro;

5)  Filtro por Número da internação (SIAPI);

6)  Filtro por Número da alta (SIAPI);

7)  Filtros por encaminhamento/retificação de internação e alta;

8)  Filtro por Ação pendente (necessário informar a justificativa do atraso ou retificação).

Tela de Log integração - SIAPI

# ![A screenshot of a computer Description automatically generated](media/image13.png)
