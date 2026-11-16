# Audio/Video - Privacy

HTTP protocol

- [Groups](../video_groups.bft)
   - Audio/Video - Telehealth: all artifacts of all video integrations.
<br>

- Artifacts
   - connector: Audio/Video - API Privacy
      - path: api/telehealth/privacy
      - path: api/telehealth/privacy/control
   - event / flow / route: telemedicina.api.privacy
<br>

- files
   - [connector_privacy.bft](connector_privacy.bft): contains only the 'connector' artifact.
   - [event_privacy.bft](event_privacy.bft): contains only the 'event' artifact.
   - [flow_privacy.bft](flow_privacy.bft): contains only the 'flow' artifact.
   - [route_privacy.bft](route_privacy.bft): contains only the 'route' artifact.
   - [video_privacy.bft](video_privacy.bft): contains the connector, event, flow, and route artifacts.
<br>

- Import sequence suggestion:
   - [Groups](../video_groups.bft)
   - [Artifacts](video_privacy.bft)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/telehealth/video)
