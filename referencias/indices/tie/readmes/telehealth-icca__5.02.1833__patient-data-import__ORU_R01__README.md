# ORU_R01

- ORU_R01 - Unsolicited transmission of an observation message
   - event: patient.data.import
   - flow / route: inbound.patient.data.import.ORU_R01
   - json-to-json: patient.data.import_2.4
<br>

- files
   - [event_pdi.bft](event_pdi.bft): contains only the 'event' artifact.
   - [flow_pdi.bft](flow_pdi.bft): contains only the 'flow' artifact.
   - [route_pdi.bft](route_pdi.bft): contains only the 'route' artifact.
   - [pdi.bft](pdi.bft): contains the event, flow, and route artifacts.
