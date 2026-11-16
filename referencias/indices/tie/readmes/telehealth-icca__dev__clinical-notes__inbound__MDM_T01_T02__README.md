# MDM_T01 - MDM_T02

- MDM_T01 - Original document notification
   - event: clinical.notes.import
   - flow / route: inbound.clinical.notes.import.MDM_T01_T02
   - json-to-json: clinical.notes.import_2.4
- MDM_T02 - Original document notification and content
   - event: clinical.notes.import
   - flow / route: inbound.clinical.notes.import.MDM_T01_T02
   - json-to-json: clinical.notes.import_2.4
<br>

- files
   - [event_clinical_notes_imp.bft](event_clinical_notes_imp.bft): contains only the 'event' artifact.
   - [flow_clinical_notes_imp.bft](flow_clinical_notes_imp.bft): contains only the 'flow' artifact.
   - [route_clinical_notes_imp.bft](route_clinical_notes_imp.bft): contains only the 'route' artifact.
   - [clinical_notes_imp.bft](clinical_notes_imp.bft): contains the event, flow, and route artifacts.
