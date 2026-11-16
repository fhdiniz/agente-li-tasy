# MDM_T02

- MDM_T02 - Original document notification and content
   - event: clinical.notes.import
   - flow / route: outbound.clinical.notes.import.MDM_T02
   - json-to-hl7(v.2.4): eCM.MDM_T02.v2.4
<br>

- files
   - [outbound_event_clinical_notes_imp.bft](outbound_event_clinical_notes_imp.bft): contains only the 'event' artifact.
   - [outbound_flow_clinical_notes_imp.bft](outbound_flow_clinical_notes_imp.bft): contains only the 'flow' artifact.
   - [outbound_route_clinical_notes_imp.bft](outbound_route_clinical_notes_imp.bft): contains only the 'route' artifact.
   - [eCM.MDM_T02.v2.4.bft](eCM.MDM_T02.v2.4.bft): contains only the json-to-hl7 transformation.
   - [outbound_clinical_notes_imp.bft](outbound_clinical_notes_imp.bft): contains the event, flow, route and json-to-hl7 artifacts.
