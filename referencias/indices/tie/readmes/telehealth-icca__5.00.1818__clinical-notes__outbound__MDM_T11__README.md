# MDM_T11

- MDM_T11 - Original document notification / inactive
   - event: clinical.notes.inactive
   - flow / route: outbound.clinical.notes.inactive.MDM_T11
   - json-to-hl7(v2.4): eCM.MDM_T11.v2.4
<br>

- files
   - [outbound_event_clinical_notes_inactive.bft](outbound_event_clinical_notes_inactive.bft): contains only the 'event' artifact.
   - [outbound_flow_clinical_notes_inactive.bft](outbound_flow_clinical_notes_inactive.bft): contains only the 'flow' artifact.
   - [outbound_route_clinical_notes_inactive.bft](outbound_route_clinical_notes_inactive.bft): contains only the 'route' artifact.
   - [eCM.MDM_T11.v2.4.bft](eCM.MDM_T11.v2.4.bft): contains only the json-to-hl7 transformation.
   - [outbound_clinical_notes_inactive.bft](outbound_clinical_notes_inactive.bft): contains the event, flow, route and json-to-hl7 artifacts.
