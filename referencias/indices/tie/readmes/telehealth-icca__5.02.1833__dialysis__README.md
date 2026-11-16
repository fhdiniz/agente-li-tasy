# inbound Diagnosis

Uses HL7 versions 2.4

- [Groups](dialysis_groups.bft)
   - eCM - Dialysis: all artifacts of inbound Dialysis integrations.
<br>

- [Connectors](connector)
   - API Patient Dialysis - eCM (HTTP)
      - path: api/patient-dialysis
   - API Patient Dialysis - eCM (MLLP)
<br>

- [Transformations](transformation)
   - json-to-json (v2.4): patient.dialysis_2.4
<br>

- [ORU_R01](ORU_R01) - Unsolicited transmission of an observation message
   - event: patient.dialysis
   - flow / route: inbound.patient.dialysis.ORU_R01
<br>

- Import sequence suggestion:
   - [Groups](dialysis_groups.bft)
   - [Connectors](connector)
   - [Transformations](transformation)
   - [ORU_R01](ORU_R01)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/icca/dialysis)
