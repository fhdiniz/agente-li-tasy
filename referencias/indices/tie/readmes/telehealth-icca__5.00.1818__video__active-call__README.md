# Audio/Video - Active Call

Scheduler

- [Groups](../video_groups.bft)
   - Audio/Video - Telehealth: all artifacts of all video integrations.
<br>

- Artifacts
   - connector: Audio/Video - Active Call
      - scheduler: AudioVideoActiveCall
   - event / flow / route: telemedicina.api.active.call
<br>

- files
   - [connector_active_call.bft](connector_active_call.bft): contains only the 'connector' artifact.
   - [event_active_call.bft](event_active_call.bft): contains only the 'event' artifact.
   - [flow_active_call.bft](flow_active_call.bft): contains only the 'flow' artifact.
   - [route_active_call.bft](route_active_call.bft): contains only the 'route' artifact.
   - [video_active_call.bft](video_active_call.bft): contains the connector, event, flow, and route artifacts.
<br>

- Import sequence suggestion:
   - [Groups](../video_groups.bft)
   - [Artifacts](video_active_call.bft)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/telehealth/video)
