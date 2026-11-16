# Integração com Banco de Sangue – FSFB

Este projeto define e implementa a integração entre o sistema Tasy e o Banco de Sangue FSFB, utilizando mensagens HL7 para automatizar a comunicação de ordens de hemoterapia.

## Objetivo

Enviar automaticamente, via protocolo MLLP, ordens de produtos sanguíneos para o Banco de Sangue, sempre que uma bolsa for liberada para um paciente no sistema clínico.

## Funcionamento da Integração

1. O profissional libera uma bolsa de sangue no sistema Tasy.
2. O evento aciona a geração de uma mensagem HL7 do tipo `OMB^O27`.
3. O conteúdo é transformado conforme a estrutura esperada pelo banco de sangue.
4. A mensagem é enviada via MLLP para o endpoint configurado da FSFB.

## Componentes

| Tipo          | Nome                              | Descrição                                                                 |
|---------------|-----------------------------------|---------------------------------------------------------------------------|
| **Evento**    | `OMB.O27`                         | Evento responsável por disparar a geração da mensagem HL7.                |
| **Fluxo**     | `Blood.Product.Order_OMB-->FSFB`  | Fluxo outbound configurado para envio da mensagem para a FSFB.            |
| **Host MLLP** | `mllp_host`                       | Parâmetro configurável com o endereço do servidor da FSFB.                |
| **Porta MLLP**| `mllp_port`                       | Parâmetro configurável com a porta do servidor MLLP da FSFB.              |
| **Script**    | `JavaScript` embutido no fluxo    | Realiza transformações no corpo da mensagem para preenchimento correto.   |

## Transformações Importantes

- Define `sendingApplication` como `TASY` e `receivingApplication` como `IBE`.
- Extrai o identificador do paciente do tipo `PI` para preencher `SSNNumberPatient`.
- Define autoridade de atribuição como `SYSTEM` para o identificador selecionado.

## Requisitos

- Conectividade com o endpoint MLLP da FSFB.
- Evento `OMB.O27` habilitado no sistema de integração.
- Configurações de `mllp_host` e `mllp_port` corretamente definidas.

## Considerações

- A estrutura da mensagem segue o padrão HL7 v2.x, com base no esquema personalizado JSON.
- O fluxo utiliza roteamento Apache Camel (`direct:start`) com transformação JavaScript embutida.
- É recomendável validar as mensagens enviadas com um validador HL7 antes de produção.
