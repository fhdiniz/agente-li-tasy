# ADT_A12

- ADT_A12 - Cancel transfer
   - event: patient.transfer.cancel
   - flow / route: inbound.patient.transfer.cancel.ADT_A12
   - json-to-json: patient.information.register.ADT_A04
<br>

- files
   - [event_adt_a12.bft](event_adt_a12.bft): contains only the 'event' artifact.
   - [flow_adt_a12.bft](flow_adt_a12.bft): contains only the 'flow' artifact.
   - [route_adt_a12.bft](route_adt_a12.bft): contains only the 'route' artifact.
   - [adt_a12.bft](adt_a12.bft): contains the event, flow, and route artifacts.
