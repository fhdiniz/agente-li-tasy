# ADT_A60

- ADT_A60 - Update allergy information
   - event: allergy.information.update
   - flow / route: inbound.allergy.information.update.ADT_A60
   - json-to-json: patient.information.register.ADT_A04
<br>

- files
   - [event_adt_a60.bft](event_adt_a60.bft): contains only the 'event' artifact.
   - [flow_adt_a60.bft](flow_adt_a60.bft): contains only the 'flow' artifact.
   - [route_adt_a60.bft](route_adt_a60.bft): contains only the 'route' artifact.
   - [adt_a60.bft](adt_a60.bft): contains the event, flow, and route artifacts.
