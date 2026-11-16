# ADT_A03

- ADT_A03 - Discharge/end visit
   - event: patient.discharge
   - flow / route: outbound.patient.discharge.ADT_A03
   - json-to-hl7(v2.4): eCM.ADT_A03.v2.4
<br>

- files
   - [outbound_event_adt_a03.bft](outbound_event_adt_a03.bft): contains only the 'event' artifact.
   - [outbound_flow_adt_a03.bft](outbound_flow_adt_a03.bft): contains only the 'flow' artifact.
   - [outbound_route_adt_a03.bft](outbound_route_adt_a03.bft): contains only the 'route' artifact.
   - [eCM.ADT_A03.v2.4.bft](eCM.ADT_A03.v2.4.bft): contains only the json-to-hl7 transformation.
   - [outbound_adt_a03.bft](outbound_adt_a03.bft): contains the event, flow, route and json-to-hl7 artifacts.
