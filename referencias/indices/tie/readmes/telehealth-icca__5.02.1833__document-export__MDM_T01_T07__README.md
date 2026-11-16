# MDM_T01 MDM_T07

- MDM_T01 - Original document notification
   - event: document.data.export
   - flow / route: outbound.document.data.export.MDM_T01_T07
   - json-to-hl7: eCM.MDM_T01.v2.4
- MDM_T07 - Document edit notification
   - event: document.data.export
   - flow / route: outbound.document.data.export.MDM_T01_T07
   - json-to-hl7: eCM.MDM_T07.v2.4
<br>

- files
   - [outbound_event_doc_exp.bft](outbound_event_doc_exp.bft): contains only the 'event' artifact.
   - [outbound_flow_doc_exp.bft](outbound_flow_doc_exp.bft): contains only the 'flow' artifact.
   - [outbound_route_doc_exp.bft](outbound_route_doc_exp.bft): contains only the 'route' artifact.
   - [outbound_doc_exp.bft](outbound_doc_exp.bft): contains the event, flow and route artifacts.
