# ADT_A01

- ADT_A01 - Admit/visit notification
   - event: patient.admission
   - flow / route: inbound.patient.admission.ADT_A01
   - json-to-json: patient.information.register.ADT_A04
<br>

- files
   - [event_adt_a01.bft](event_adt_a01.bft): contains only the 'event' artifact.
   - [flow_adt_a01.bft](flow_adt_a01.bft): contains only the 'flow' artifact.
   - [route_adt_a01.bft](route_adt_a01.bft): contains only the 'route' artifact.
   - [adt_a01.bft](adt_a01.bft): contains the event, flow, and route artifacts.
