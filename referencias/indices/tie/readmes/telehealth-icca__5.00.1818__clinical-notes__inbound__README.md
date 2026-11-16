# inbound MDM

Uses HL7 v2.4

- [Groups](clinical_notes_groups.bft)
   - eCM - Interoperability: all artifacts from all integrations.
   - eCM - Clinical Notes: all artifacts of inbound Clinical Notes integrations.
   - eCM - Clinical Notes - mappings: all inbound Clinical Notes integration mappings.
<br>

- [Connectors](connector)
   - API Clinical Notes - eCM (MLLP)
<br>

- [Mappings](mapping): patient.identification.segment, message.identifier.type, doctor, gender, observation.result.status, type.clinical.note
<br>

- [Transformations](transformation)
   - json-to-json: clinical.notes.import_2.4
<br>

- [MDM_T01](MDM_T01_T02) - Original document notification
   - event: clinical.notes.import
   - flow / route: inbound.clinical.notes.import.MDM_T01_T02
   - json-to-json: clinical.notes.import_2.4
- [MDM_T02](MDM_T01_T02) - Original document notification and content
   - event: clinical.notes.import
   - flow / route: inbound.clinical.notes.import.MDM_T01_T02
   - json-to-json: clinical.notes.import_2.4
- [MDM_T08](MDM_T08_T10) - Document edit notification and content
   - event: clinical.notes.update
   - flow / route: inbound.clinical.notes.update.MDM_T08_T10
   - json-to-json: clinical.notes.import_2.4
- [MDM_T10](MDM_T08_T10) - Document replacement notification and content
   - event: clinical.notes.update
   - flow / route: inbound.clinical.notes.update.MDM_T08_T10
   - json-to-json: clinical.notes.import_2.4
- [MDM_T11](MDM_T11) - Original document notification / inactive
   - event: clinical.notes.inactive
   - flow / route: inbound.clinical.notes.inactive.MDM_T11
   - json-to-json: clinical.notes.import_2.4
<br>

- Import sequence suggestion:
   - [Groups](clinical_notes_groups.bft)
   - [Connectors](connector)
   - [Mappings](mapping)
   - [Transformations](transformation)
   - [MDM_T01](MDM_T01_T02), [MDM_T08](MDM_T08_T10), [MDM_T11](MDM_T11), etc.
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/telehealth/clinicalnotes)
