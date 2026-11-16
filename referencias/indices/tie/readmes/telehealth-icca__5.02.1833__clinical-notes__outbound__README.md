# outbound MDM

Uses HL7 v2.4

- [Groups](outbound_clinical_notes_groups.bft)
   - eCM - Interoperability: all artifacts from all integrations.
   - eCM - Clinical Notes outbound: all artifacts of outbound Clinical Notes integrations.
   - eCM - Clinical Notes outbound - mappings: all outbound Clinical Notes integration mappings.
<br>

- [Mappings](mapping): outbound.gender, outbound.marital.status, outbound.observation.result.status
<br>

- [MDM_T02](MDM_T02) - Original document notification and content
   - event: clinical.notes.import
   - flow / route: outbound.clinical.notes.import.MDM_T02
   - json-to-hl7: eCM.MDM_T02.v2.4
- [MDM_T11](MDM_T11) - Original document notification / inactive
   - event: clinical.notes.inactive
   - flow / route: outbound.clinical.notes.inactive.MDM_T11
   - json-to-hl7: eCM.MDM_T11.v2.4
<br>

- Import sequence suggestion:
   - [Groups](outbound_clinical_notes_groups.bft)
   - [Mappings](mapping)
   - [MDM_T02](MDM_T02) and [MDM_T11](MDM_T11).
<br>

