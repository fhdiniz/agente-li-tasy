# Audio/Video - Soft Button

HTTP protocol

- [Groups](../video_groups.bft)
   - Audio/Video - Telehealth: all artifacts of all video integrations.
<br>

- Artifacts
   - connector: Audio/Video - API Soft Button
      - path: api/telehealth/softbutton/setup
   - event / flow / route: telemedicina.api.softbtn
<br>

- files
   - [connector_soft_button.bft](connector_soft_button.bft): contains only the 'connector' artifact.
   - [event_soft_button.bft](event_soft_button.bft): contains only the 'event' artifact.
   - [flow_soft_button.bft](flow_soft_button.bft): contains only the 'flow' artifact.
   - [route_soft_button.bft](route_soft_button.bft): contains only the 'route' artifact.
   - [video_soft_button.bft](video_soft_button.bft): contains the connector, event, flow, and route artifacts.
<br>

- Import sequence suggestion:
   - [Groups](../video_groups.bft)
   - [Artifacts](video_soft_button.bft)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/telehealth/video)
