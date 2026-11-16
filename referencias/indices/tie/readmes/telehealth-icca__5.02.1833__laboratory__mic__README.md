# ORU_R01 - Microbiology

- ORU_R01 - Unsolicited transmission of an observation message
   - event: microbiology.order.information
   - flow / route: inbound.microbiology.order.information.ORU_R01
   - json-to-json: laboratory.information.register
<br>

- files
   - [event_microbiology.bft](event_microbiology.bft): contains only the 'event' artifact.
   - [flow_microbiology.bft](flow_microbiology.bft): contains only the 'flow' artifact.
   - [route_microbiology.bft](route_microbiology.bft): contains only the 'route' artifact.
   - [microbiology.bft](microbiology.bft): contains the event, flow, and route artifacts.
