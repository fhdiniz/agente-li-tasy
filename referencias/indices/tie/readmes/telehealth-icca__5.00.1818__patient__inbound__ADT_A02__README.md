# ADT_A02

- ADT_A02 - Transfer patient
   - event: patient.transfer
   - flow / route: inbound.patient.transfer.ADT_A02
   - json-to-json: patient.information.register.ADT_A04
<br>

- files
   - [event_adt_a02.bft](event_adt_a02.bft): contains only the 'event' artifact.
   - [flow_adt_a02.bft](flow_adt_a02.bft): contains only the 'flow' artifact.
   - [route_adt_a02.bft](route_adt_a02.bft): contains only the 'route' artifact.
   - [adt_a02.bft](adt_a02.bft): contains the event, flow, and route artifacts.
