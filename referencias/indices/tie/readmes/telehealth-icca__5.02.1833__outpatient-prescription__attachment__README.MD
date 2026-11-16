# PDI - OutPatient Prescription base64 attachment document import

<br>

This API was developed to allow the third-party system to attach documents to the outpatient prescription in attachment tab.

<br>

Uses HTTP POST API

- [Groups](outpatient_prescription_attachment.bft)
   - Interoperability: all artifacts from all integrations.
   - Mappings: all inbound PDI integration mappings.
<br>

- [Connectors](connector)
   - API OutPatient Prescription attachment document import (HTTP)

- [Transformations](transformation)
   - json-to-json: Prescription_Document_Attachment_JSON
<br>

- [API](HTTP_POST) - Unsolicited transmission of an observation message
   - connector: prescription.document.attachment
   - event: save_document_attachment_prescription
   - flow / route: prescription.document.save.attachment -> TASY
   - json-to-json: Prescription_Document_Attachment_JSON
<br>

- Import sequence suggestion:
   - [Groups](outpatient_prescription_attachment.bft)
   
<br>

[tasy-backend](https://github.com/philips-emr/tasy-backend/blob/art_clinical_records/Integrations/src/main/java/com/philips/tasy/app/inbound/clinical/prescription/attachment/RegisterAttachmentEndpoint.java)
<br>
