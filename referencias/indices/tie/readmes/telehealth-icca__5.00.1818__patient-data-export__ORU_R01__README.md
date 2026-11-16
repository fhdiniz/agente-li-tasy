# ORU_R01

- ORU_R01 - Unsolicited transmission of an observation message
   - event: patient.data.export
   - flow / route: outbound.patient.data.export.ORU_R01
   - json-to-hl7(v2.4): eCM.ORU_R01.v2.4
<br>

- files
   - [outbound_event_pde.bft](outbound_event_pde.bft): contains only the 'event' artifact.
   - [outbound_flow_pde.bft](outbound_flow_pde.bft): contains only the 'flow' artifact.
   - [outbound_route_pde.bft](outbound_route_pde.bft): contains only the 'route' artifact.
   - [eCM.ORU_R01.v2.4.bft](eCM.ORU_R01.v2.4.bft): contains only the json-to-hl7 transformation.
   - [outbound_pde.bft](outbound_pde.bft): contains the event, flow, route and json-to-hl7 artifacts.
