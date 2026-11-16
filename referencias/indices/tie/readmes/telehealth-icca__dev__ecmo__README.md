# inbound Diagnosis

Uses HL7 versions 2.4

- [Groups](ecmo_groups.bft)
   - eCM - ECMO: all artifacts of inbound ECMO integrations.
<br>

- [Connectors](connector)
   - API Patient ECMO - eCM (HTTP)
      - path: api/patient-ecmo
   - API Patient ECMO - eCM (MLLP)
<br>

- [Transformations](transformation)
   - json-to-json (v2.4): patient.ecmo_2.4
<br>

- [ORU_R01](ORU_R01) - Unsolicited transmission of an observation message
   - event: patient.ecmo
   - flow / route: inbound.patient.ecmo.ORU_R01
<br>

- Import sequence suggestion:
   - [Groups](ecmo_groups.bft)
   - [Connectors](connector)
   - [Transformations](transformation)
   - [ORU_R01](ORU_R01)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/icca/ecmo)
