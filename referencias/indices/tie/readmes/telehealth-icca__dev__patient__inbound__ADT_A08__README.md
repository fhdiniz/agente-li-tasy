# ADT_A08

- ADT_A08 - Update patient information
   - event: patient.information.update
   - flow / route: inbound.patient.information.update.ADT_A08
   - json-to-json: patient.information.register.ADT_A04
<br>

- files
   - [event_adt_a08.bft](event_adt_a08.bft): contains only the 'event' artifact.
   - [flow_adt_a08.bft](flow_adt_a08.bft): contains only the 'flow' artifact.
   - [route_adt_a08.bft](route_adt_a08.bft): contains only the 'route' artifact.
   - [adt_a08.bft](adt_a08.bft): contains the event, flow, and route artifacts.
