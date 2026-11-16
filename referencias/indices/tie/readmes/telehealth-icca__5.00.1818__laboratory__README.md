# laboratory / microbiology

Uses HL7 v2.4

- [Groups](laboratory_groups.bft)
   - eCM - Interoperability: all artifacts from all integrations.
   - eCM - Laboratory: all artifacts of inbound Laboratory integrations.
   - eCM - Laboratory - mappings: all inbound Laboratory integration mappings.
<br>

- [Connectors](connector)
   - API Laboratory - eCM (MLLP)
   - API Microbiology Sample 2 - eCM (MLLP)
   - API Microbiology Sample 3 - eCM (MLLP)
   - API Microbiology Sample 4 - eCM (MLLP)
<br>

- [Mappings](mapping): abnormal.flags, diagnostic.service.section, doctor, external.order.type, gender, lab.result.status, observation.result.status, specimen.source
<br>

- [Transformations](transformation)
   - json-to-json: laboratory.information.register
<br>

- [ORU_R01 - Laboratory](lab) - Unsolicited transmission of an observation message
   - event: laboratory.order.information
   - flow / route: inbound.laboratory.order.information.ORU_R01
   - json-to-json: laboratory.information.register
- [ORU_R01 - Microbiology](mic) - Unsolicited transmission of an observation message
   - event: microbiology.order.information
   - flow / route: inbound.microbiology.order.information.ORU_R01
   - json-to-json: laboratory.information.register
<br>

- Import sequence suggestion:
   - [Groups](laboratory_groups.bft)
   - [Connectors](connector)
   - [Mappings](mapping)
   - [Transformations](transformation)
   - [ORU_R01 - Laboratory](lab) and [ORU_R01 - Microbiology](mic)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/telehealth/laboratory)
