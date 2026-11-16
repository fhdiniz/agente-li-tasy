# ORU_R01 - Laboratory

- ORU_R01 - Unsolicited transmission of an observation message
   - event: laboratory.order.information
   - flow / route: inbound.laboratory.order.information.ORU_R01
   - json-to-json: laboratory.information.register
<br>

- files
   - [event_laboratory.bft](event_laboratory.bft): contains only the 'event' artifact.
   - [flow_laboratory.bft](flow_laboratory.bft): contains only the 'flow' artifact.
   - [route_laboratory.bft](route_laboratory.bft): contains only the 'route' artifact.
   - [laboratory.bft](laboratory.bft): contains the event, flow, and route artifacts.
