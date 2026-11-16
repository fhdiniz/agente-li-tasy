# MDM_T08 - MDM_T10

- MDM_T08 - Document edit notification and content
   - event: clinical.notes.update
   - flow / route: inbound.clinical.notes.update.MDM_T08_T10
   - json-to-json: clinical.notes.import_2.4
- MDM_T10 - Document replacement notification and content
   - event: clinical.notes.update
   - flow / route: inbound.clinical.notes.update.MDM_T08_T10
   - json-to-json: clinical.notes.import_2.4
<br>

- files
   - [event_clinical_notes_up.bft](event_clinical_notes_up.bft): contains only the 'event' artifact.
   - [flow_clinical_notes_up.bft](flow_clinical_notes_up.bft): contains only the 'flow' artifact.
   - [route_clinical_notes_up.bft](route_clinical_notes_up.bft): contains only the 'route' artifact.
   - [clinical_notes_up.bft](clinical_notes_up.bft): contains the event, flow, and route artifacts.
