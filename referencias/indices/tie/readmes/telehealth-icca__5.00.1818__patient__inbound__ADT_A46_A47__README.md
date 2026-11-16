# ADT_A46 - ADT_A47

- ADT_A46 - Change patient id
   - event: patient.identifier.update
   - flow / route: inbound.patient.identifier.update.ADT_46_47
   - json-to-json: patient.identifier.update.ADT_46_47
- ADT_A47 - Change patient identifier list
   - event: patient.identifier.update
   - flow / route: inbound.patient.identifier.update.ADT_46_47
   - json-to-json: patient.identifier.update.ADT_46_47
<br>

- files
   - [event_adt_a46_a47.bft](event_adt_a46_a47.bft): contains only the 'event' artifact.
   - [flow_adt_a46_a47.bft](flow_adt_a46_a47.bft): contains only the 'flow' artifact.
   - [route_adt_a46_a47.bft](route_adt_a46_a47.bft): contains only the 'route' artifact.
   - [adt_a46_a47.bft](adt_a46_a47.bft): contains the event, flow, and route artifacts.
