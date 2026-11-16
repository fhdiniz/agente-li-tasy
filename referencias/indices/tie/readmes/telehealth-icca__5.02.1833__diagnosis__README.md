# inbound Diagnosis

Uses HL7 versions 2.4

- [Groups](diagnosis_groups.bft)
   - eCM - Diagnosis: all artifacts of inbound Diagnosis integrations.
<br>

- [Connectors](connector)
   - API Patient Diagnosis - eCM (HTTP)
      - path: api/patient-diagnosis
   - API Patient Diagnosis - eCM (MLLP)
<br>

- [Transformations](transformation)
   - json-to-json (v2.4): patient.diagnosis_2.4
<br>

- [ORU_R01](ORU_R01) - Unsolicited transmission of an observation message
   - event: patient.diagnosis
   - flow / route: inbound.patient.diagnosis.ORU_R01
<br>

- Import sequence suggestion:
   - [Groups](diagnosis_groups.bft)
   - [Connectors](connector)
   - [Transformations](transformation)
   - [ORU_R01](ORU_R01)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/icca/diagnosis)
