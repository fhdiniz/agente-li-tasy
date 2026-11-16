# PDI - patient data import

Uses HL7 v2.4

- [Groups](pdi_groups.bft)
   - eCM - Interoperability: all artifacts from all integrations.
   - eCM - PDI: all artifacts of inbound PDI integration.
   - eCM - PDI - mappings: all inbound PDI integration mappings.
<br>

- [Connectors](connector)
   - API Patient data import - eCM (HTTP)
   - API Patient data import - eCM (MLLP)
<br>

- [Mappings](mapping): doctor, gender, message.identifier.type, observation.result.status, patient.identification.segment
<br>

- [Transformations](transformation)
   - json-to-json: patient.data.import_2.4
<br>

- [ORU_R01](ORU_R01) - Unsolicited transmission of an observation message
   - event: patient.data.import
   - flow / route: inbound.patient.data.import.ORU_R01
   - json-to-json: patient.data.import_2.4
<br>

- Import sequence suggestion:
   - [Groups](pdi_groups.bft)
   - [Connectors](connector)
   - [Mappings](mapping)
   - [Transformations](transformation)
   - [ORU_R01](ORU_R01)
<br>

[Flowsheet tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/icca/flowsheet)
<br>
[Linked-data tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/icca/linkeddata)
