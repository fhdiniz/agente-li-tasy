# ADT_A13

- ADT_A13 - Cancel discharge/end visit
   - event: patient.discharge.cancel
   - flow / route: inbound.patient.discharge.cancel.ADT_A13
   - json-to-json: patient.information.register.ADT_A04
<br>

- files
   - [event_adt_a13.bft](event_adt_a13.bft): contains only the 'event' artifact.
   - [flow_adt_a13.bft](flow_adt_a13.bft): contains only the 'flow' artifact.
   - [route_adt_a13.bft](route_adt_a13.bft): contains only the 'route' artifact.
   - [adt_a13.bft](adt_a13.bft): contains the event, flow, and route artifacts.
