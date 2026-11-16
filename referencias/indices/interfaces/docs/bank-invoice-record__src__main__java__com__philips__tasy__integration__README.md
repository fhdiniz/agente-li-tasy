# Bank Invoice Record Integration

Bank Invoice Record is an integration for making new bank invoice records (table TITULO_RECEBER_HIS_BOL_ON) data in Tasy available to third party systems.

# Usage

Using the online bill registration process - Banco Bradesco

- Check parameters:

        System Menu Function

            Parameter 216 - Must have the Tasy Interfaces address

        Integration Function

            Parameter 10 - Must be enabled

            Parameter 11 - Must have the Tasy Interfaces address

            Parameter 12 - Choose the request method, HTTP or Polling (internal tests use HTTP)

            Parameter 13 - Only for Polling mode, enter the Polling server address

        Maintenance of Accounts Receivable  Function

            Parameter 40 - If enabled, the bill must have a collection portfolio informed.

            Parameter 133 - If the Bill Issuance mouse option does not appear, check if the portfolio informed is valid for issuing a bill.

Step by step activation in TASY EMR:

- Generate a new bill receivable in Tasy, with sufficient data to generate a bill.
The following values are required:
 
       NR_SEQ_BANK_CONTACT - Check if the selected account is enabled to generate payment slips, using the Financial Records > Bank > Establishment Bank function.
       NR_SEQ_CARTEIRA_COBR - Required if param 40 is enabled, check the validity of the payment slip if param 133 is also in use.

- Use the mouse option "Pay slips > Issue", which will start the entire process. If the payment slip has already been created in Tasy, use the option "Pay slips > Register payment slip online".


- When using the mouse option, the operation will be performed by tasy-interfaces and tie. After a while, a record in the panel on the right called "Online payment slip history" should appear, with details of the communication.

The available endpoints for this API are:

<details>
<summary>Click to expand</summary>

## /api/bankinvoicerecord/signBBDCInvoice (POST)

### Example:

````
curl --location 'http://localhost:50001/tasy-interfaces/resources/api/bankinvoicerecord/signBBDCInvoice?throwExceptionOnFailure=false' \
-H 'CamelHttpMethod: POST -H 'Content-Type: application/json;charset=UTF-8' \
````

### Parameters:

```markdown
| Parameter                             | Type   | Description                             |
|---------------------------------------|--------|-----------------------------------------|
| userName                              | String | Name of the Tasy user                   |
| nrTitulo                              | String | Document number                         |
| nuCpfCnpj                             | String | CPF/CNPJ of our company                 |
| filialCpfCnpj                         | String | Filial part of the CNPJ ex: 0001        |
| ctrlCpfCnpj                           | String | Verification digits of the CNPJ         |
| cdTipoAcesso                          | String | Type of access                          |
| clubBanco                             | String | Banking code                            |
| cdTipoContrato                        | String | Contract type code                      |
| nuSequenciaContrato                   | String | Contract sequence code                  |
| idProduto                             | String | Product ID                              |
| nuNegociacao                          | String | Negotiation code                        |
| cdBanco                               | String | Bank number in FEBRABAN                 |
| eNuSequenciaContrato                  | String | Electronic Contract sequence code       |
| tpRegistro                            | String | Type of Register                        |
| cdProduto                             | String | Product code                            |
| nuTitulo                              | String | Our company number                      |
| nuCliente                             | String | Our company client code                 |
| dtEmissaoTitulo                       | String | Emission date                           |
| dtVencimentoTitulo                    | String | Expiration date                         |
| tpVencimento                          | String | Type of exprirarion                     |
| vlNominalTitulo                       | String | Nominal value of document               |
| cdEspecieTitulo                       | String | Type of document code                   |
| tpProtestoAutomaticoNegativacao       | String | Type of automatic protest of deny       |
| prazoProtestoAutomaticoNegativacao    | String | Days for the automatic protest for deny |
| controleParticipante                  | String | Participant control                     |
| cdPagamentoParcial                    | String | Parcial payment code                    |
| qtdePagamentoParcial                  | String | Parcial payment quantity                |
| percentualJuros                       | String | Interest rate                           |
| vlJuros                               | String | Interest value                          |
| qtdeDiasJuros                         | String | Quantity of interest days               |
| percentualMulta                       | String | Fine rate                               |
| vlMulta                               | String | Fine value                              |
| qtdeDiasMulta                         | String | Quantity of fine days                   |
| percentualDesconto1                   | String | First discount rate                     |
| vlDesconto1                           | String | First discount value                    |
| dataLimiteDesconto1                   | String | First max date for discount             |
| percentualDesconto2                   | String | Second discount rate                    |
| vlDesconto2                           | String | Second discount value                   |
| dataLimiteDesconto2                   | String | Second max date for discount            |
| percentualDesconto3                   | String | Third discount rate                     |
| vlDesconto3                           | String | Third discount value                    |
| dataLimiteDesconto3                   | String | Third max date for discount             |
| prazoBonificacao                      | String | Deadline for bonus                      |
| percentualBonificacao                 | String | Rate of bonus                           |
| vlBonificacao                         | String | Value of bonus                          |
| dtLimiteBonificacao                   | String | Max data of bonus                       |
| vlAbatimento                          | String | Rebate value                            |
| vlIOF                                 | String | IOF value                               |
| nomePagador                           | String | Payer's name                            |
| logradouroPagador                     | String | Payers's address                        |
| nuLogradouroPagador                   | String | Payers's address                        |
| complementoLogradouroPagador          | String | Payers's address complement             |
| cepPagador                            | String | Payers's postal code                    |
| complementoCepPagador                 | String | Payers's complement                     |
| bairroPagador                         | String | Payers's neighbourhood                  |
| municipioPagador                      | String | Payers's city                           |
| ufPagador                             | String | Payers's state                          |
| cdIndCpfcnpjPagador                   | String | Payers's CPF/CNPJ                       |
| nuCpfcnpjPagador                      | String | Payers's CPF/CNPJ                       |
| endEletronicoPagador                  | String | Payers's email                          |
| nomeSacadorAvalista                   | String | Guarantor's name                        |
| logradouroSacadorAvalista             | String | Guarantor's address                     |
| nuLogradouroSacadorAvalista           | String | Guarantor's address                     |
| complementoLogradouroSacadorAvalista  | String | Guarantor's address complement          |
| cepSacadorAvalista                    | String | Guarantor's postal code                 |
| complementoCepSacadorAvalista         | String | Guarantor's complement                  |
| bairroSacadorAvalista                 | String | Guarantor's neighbourhood               |
| municipioSacadorAvalista              | String | Guarantor's city                        |
| ufSacadorAvalista                     | String | Guarantor's state                       |
| cdIndCpfcnpjSacadorAvalista           | String | Guarantor's CPF/CNPJ                    |
| nuCpfcnpjSacadorAvalista              | String | Guarantor's CPF/CNPJ                    |
| endEletronicoSacadorAvalista          | String | Guarantor's email                       |
```

## /api/bankinvoicerecord/saveLogInfo?bridgeEndpoint=true&throwExceptionOnFailure=false (POST) 

### Example:

````
curl --location 'http://localhost:50001/tasy-interfaces/resources/api/bankinvoicerecord/saveLogInfo?bridgeEndpoint=true&throwExceptionOnFailure=false' \
-H 'CamelHttpMethod: POST -H 'Content-Type: application/json;charset=UTF-8' \
````

### Parameters:

```markdown
| Parameter      | Type      | Description                         |
|----------------|-----------|-------------------------------------|
| accountNumber  | Long      | Account Receivable code             |
| userName       | String    | Name of the Tasy user               |
| logInfo        | String    | Readable message of information     |
| status         | String    | Integration status                  | 
| description    | String    | Obtained from the endpoint return   |
| jsonRequest    | String    | Original JSON request sent to       |
```

</details>

## Configurations

These configurations are available for this integration and must be defined on application.properties file.

```text
# Connector
bankinvoicerecord.host = *include host
bankinvoicerecord.hostInterfaces = *include host of interfaces
bankinvoicerecord.port = *include port
bankinvoicerecord.portInterfaces = *include port interfaces
bankinvoicerecord.protocol = *include protocol
bankinvoicerecord.protocolInterfaces = *include protocol of interfaces
bankinvoicerecord.token = *include token
bankinvoicerecord.endpointBoleto = *include endpoint of banking pay-slip 
```
