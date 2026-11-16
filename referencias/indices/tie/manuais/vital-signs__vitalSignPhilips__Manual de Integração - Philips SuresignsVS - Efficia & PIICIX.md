                                       Manual de Integração             HISS EMR
                                                                        Código documento: ########
                                                                        Revisão: 00_
                                SureSignSVS – Efficia – PIICIX          Status: Aprovado




         INTERFACE MONITORIZAÇÃO SINAIS VITAIS – PHILIPS




                                                AVISO

O conteúdo deste documento é de propriedade exclusiva da Philips e está sujeito a alterações sem aviso
prévio.

Esta cópia deverá ser protegida contra divulgações indevidas, como cópia da documentação eletrônica,
impressa ou parte dela, não deverá ser emprestada, reproduzida ou vendida.

Todos os nomes de empresas, produtos, marcas comerciais, pessoas, personagens, dados ou situações,
citados neste documento são fictícios e tem somente objetivo didático.




 Confidencial da Companhia Philips                                                         Página 1 de 10
                                     CÓPIAS NÃO SÃO CONTROLADAS
                                                 Manual de Integração                         HISS EMR
                                                                                              Código documento: ########
                                                                                              Revisão: 00_
                                     SureSignSVS – Efficia – PIICIX                           Status: Aprovado




2 Sumário

1 Objetivo da interface monitorização de sinais vitais – Philips .............................................. 2
  1.1 Principais Características .................................................................................................. 2
2 Requisitos necessários para a interface monitorização de sinais vitais – Philips ..................... 2
3 Fluxo da interface Monitorização de sinais vitais – Philips .................................................. 3
4 Configurações e Parametrizações no Sistema ................................................................... 3
  4.1 Forma de Comunicação............................................................................................ 3
  4.2 Cadastros e Parametrizações .................................................................................... 3
5 Testes da interface monitorização de sinais vitais – Philips ................................................ 7
  5.1 Processo (Sugerido) ................................................................................................ 8
  5.2 Visualização de Resultados ....................................................................................... 8
6 – Outras configurações no Tasy ...................................................................................... 8
    6.1 Leito Monitorado .................................................................................................. 8
    6.1.1 Minutos para importar sinais vitais dos monitores Philips ........................................ 9
    6.1.2 Nome setor e leito da integração ......................................................................... 9


1 Objetivo da interface monitorização de sinais vitais – Philips

A integração tem como objetivo agilizar todo processo de recebimento de mensagens hl7, retirando toda regra de
negócio do TASY. Desta forma existe um ganho de performance por parte do TASY e também do processamento de
mensagens hl7.


              1.1 Principais Características

              •    Ganho de performance no TASY.
              •    Melhor recurso de rastreamento de dados.
              •    Manutenções de fácil acesso.



2 Requisitos necessários para a interface monitorização de sinais vitais – Philips

Para que a Integração ocorra com sucesso, será necessário a instalação dos ambientes:

              •    Tasy Interfaces
              •    Tasy Interfaces Engine




 Confidencial da Companhia Philips                                                                                Página 2 de 10
                                               CÓPIAS NÃO SÃO CONTROLADAS
                                            Manual de Integração                     HISS EMR
                                                                                     Código documento: ########
                                                                                     Revisão: 00_
                                 SureSignSVS – Efficia – PIICIX                      Status: Aprovado



3 Fluxo da interface Monitorização de sinais vitais – Philips

A integração inicia imediatamente quando o monitor de sinais vitais encaminha uma mensagem hl7
para o conector no Tasy Interfaces Engine.
Após receber a mensagem será aplicada toda regra de negócio programada no connector, e será
inserido os registros no TASY.

4 Configurações e Parametrizações no Sistema

Abaixo estão descritos as configurações e parametrizações necessárias a nível de sistema para o funcionamento da
Integração.

      4.1 Forma de Comunicação

      Esta integração espera uma Mensagem HL7.
      Desta forma não serão aceitos nenhum outro tipo de arquivo.


      4.2 Cadastros e Parametrizações

        Caso for necessário, deverá realizar a exportação da base oficial do Tasy Interfaces Engine todo fluxo da
        integração em questão conforme abaixo:

             •   Flow
             •   Connector
             •   Event
             •   Route
             •   JSON TO JSON



       O export será necessário solicitar a Philips através de ordem de serviço, desta forma assim que a Philips
encaminhar o arquivo basta importar o mesmo no Tasy Interfaces Engine.




Existe a opção “Import artifacts”, conforme imagem abaixo:




 Confidencial da Companhia Philips                                                                      Página 3 de 10
                                          CÓPIAS NÃO SÃO CONTROLADAS
                                            Manual de Integração       HISS EMR
                                                                       Código documento: ########
                                                                       Revisão: 00_
                                 SureSignSVS – Efficia – PIICIX        Status: Aprovado




Deve carregar o arquivo pelo botão “Load file”.




E depois confirmar a importação no botão “Import”




 Confidencial da Companhia Philips                                                        Página 4 de 10
                                          CÓPIAS NÃO SÃO CONTROLADAS
                                           Manual de Integração                     HISS EMR
                                                                                    Código documento: ########
                                                                                    Revisão: 00_
                                SureSignSVS – Efficia – PIICIX                      Status: Aprovado




Após a importação iremos obter a URL para configurar a integração posteriormente;




         A integração com os monitores da Philips modelos SureSignsVS & EfficiaCM podem ser realizados de 02 (duas)
formas. Sendo uma pelo número de pessoa física (prontuário) do paciente e a segunda pelo atendimento do paciente.
A forma a ser adotada dependera do tipo de mensagem HL7 recebida, quando conter a sequência de caractere Visit
Number na linha do PV1 da mensagem hl7, a integração disparada será por número de atendimento, caso contrário
será pelo número de prontuário.
         Para o modelo de monitor PIICIX, a integração se dará pelo número de de pessoa física.



Exemplo de mensagem HL7 dos monitores EfficiaCM:




 Confidencial da Companhia Philips                                                                     Página 5 de 10
                                         CÓPIAS NÃO SÃO CONTROLADAS
                                           Manual de Integração                  HISS EMR
                                                                                 Código documento: ########
                                                                                 Revisão: 00_
                                   SureSignSVS – Efficia – PIICIX                Status: Aprovado




Será necessário configurar os seguintes itens:
Connectors: Philips VitalSign PIIC IX / IBE
No connector você deverá informar a Porta Listener (Porta responsável por receber as mensagens HL7 dos monitores).
Essa porta deve possuir comunicação tanto com servidor do tasy-interfaces como o servidor dos monitores.




Flows: patient.vitalsigns.result


 Confidencial da Companhia Philips                                                                  Página 6 de 10
                                         CÓPIAS NÃO SÃO CONTROLADAS
                                           Manual de Integração                    HISS EMR
                                                                                   Código documento: ########
                                                                                   Revisão: 00_
                                 SureSignSVS – Efficia – PIICIX                    Status: Aprovado



Neste item você deve configurar os parâmetros tasy_context, tasy_host e tasy_port com o IP/Porta do Tasy-Interfaces.




Routes: patient.vitalsigns.result
Neste item você deve configurar os parâmetros tasy_context, tasy_host e tasy_port com o IP/Porta do Tasy-Interfaces.




5 Testes da interface monitorização de sinais vitais – Philips




 Confidencial da Companhia Philips                                                                    Página 7 de 10
                                          CÓPIAS NÃO SÃO CONTROLADAS
                                             Manual de Integração                     HISS EMR
                                                                                      Código documento: ########
                                                                                      Revisão: 00_
                                 SureSignSVS – Efficia – PIICIX                       Status: Aprovado



      5.1 Processo (Sugerido)

      Para realizar os testes da integração se faz necessário configurar o IP do Tasy-interfaces, juntamente com a Porta
      Listener definidos no connector e flow e posteriormente encaminhar uma mensagem HL7.


      5.2 Visualização de Resultados

      É possível visualizar o resultado dentro do Prontuário Eletrônico do Paciente, no item Sinais Vitais.


6 – Outras configurações no Tasy

      6.1 Leito Monitorado

A instituição deve marcar as unidades/leito que são monitorados para que os sinais vitais
possam ser integrados.




 Confidencial da Companhia Philips                                                                       Página 8 de 10
                                           CÓPIAS NÃO SÃO CONTROLADAS
                                             Manual de Integração                    HISS EMR
                                                                                     Código documento: ########
                                                                                     Revisão: 00_
                                  SureSignSVS – Efficia – PIICIX                     Status: Aprovado



      6.1.1 Minutos para importar sinais vitais dos monitores Philips

A instituição pode definir um tempo de intervalo para inserção nos registros de sinais vitais. Exemplo 120 minutos.




       6.1.2 Nome setor e leito da integração

A instituição pode definir (não obrigatório) a checagem da mensagem HL7 com o setor e leito que o paciente se encontra.
Para consistir a regra deve marcar a opção “Validar setor e leito monit Philips” na função “Cadastros Gerais > Parâmetros
PEP”.




 Confidencial da Companhia Philips                                                                      Página 9 de 10
                                           CÓPIAS NÃO SÃO CONTROLADAS
                                           Manual de Integração                  HISS EMR
                                                                                 Código documento: ########
                                                                                 Revisão: 00_
                                SureSignSVS – Efficia – PIICIX                   Status: Aprovado



Com esse cadastro somente será inserido o registro no sinal vital, se as informações do HL7 estejam de acordo com o
cadastro do setor e leito.




Confidencial da Companhia Philips                                                                Página 10 de 10
                                         CÓPIAS NÃO SÃO CONTROLADAS
