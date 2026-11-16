# ADT_A11

- ADT_A11 - Cancel admit/visit
   - event: patient.admission.cancel
   - flow / route: inbound.patient.admission.cancel.ADT_A11
   - json-to-json: patient.information.register.ADT_A04
<br>

- files
   - [event_adt_a11.bft](event_adt_a11.bft): contains only the 'event' artifact.
   - [flow_adt_a11.bft](flow_adt_a11.bft): contains only the 'flow' artifact.
   - [route_adt_a11.bft](route_adt_a11.bft): contains only the 'route' artifact.
   - [adt_a11.bft](adt_a11.bft): contains the event, flow, and route artifacts.
