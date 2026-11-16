# ADT_A03

- ADT_A03 - Discharge/end visit
   - event: patient.discharge
   - flow / route: inbound.patient.discharge.ADT_A03
   - json-to-json: patient.information.register.ADT_A04
<br>

- files
   - [event_adt_a03.bft](event_adt_a03.bft): contains only the 'event' artifact.
   - [flow_adt_a03.bft](flow_adt_a03.bft): contains only the 'flow' artifact.
   - [route_adt_a03.bft](route_adt_a03.bft): contains only the 'route' artifact.
   - [adt_a03.bft](adt_a03.bft): contains the event, flow, and route artifacts.
