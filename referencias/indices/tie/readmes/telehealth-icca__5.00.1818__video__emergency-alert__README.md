# Audio/Video - Emergency Alert

HTTP protocol

- [Groups](../video_groups.bft)
   - Audio/Video - Telehealth: all artifacts of all video integrations.
<br>

- Artifacts
   - connector: Audio/Video - Emergency Alert
      - path: api/telehealth/emergency-alert
   - event / flow / route: telemedicina.api.callback
<br>

- files
   - [connector_emergency_alert.bft](connector_emergency_alert.bft): contains only the 'connector' artifact.
   - [event_emergency_alert.bft](event_emergency_alert.bft): contains only the 'event' artifact.
   - [flow_emergency_alert.bft](flow_emergency_alert.bft): contains only the 'flow' artifact.
   - [route_emergency_alert.bft](route_emergency_alert.bft): contains only the 'route' artifact.
   - [video_emergency_alert.bft](video_emergency_alert.bft): contains the connector, event, flow, and route artifacts.
<br>

- Import sequence suggestion:
   - [Groups](../video_groups.bft)
   - [Artifacts](video_emergency_alert.bft)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/telehealth/video)
