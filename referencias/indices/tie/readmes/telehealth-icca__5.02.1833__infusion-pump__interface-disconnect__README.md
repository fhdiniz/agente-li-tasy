# Infusion Pump - Disconnect Schedule

Scheduler

- [Groups](../infusion_pump_groups.bft)
   - eCM - Interoperability: all artifacts from all integrations.
   - eCM - Infusion Pump: all artifacts of Infusion Pump integrations.
<br>

- Artifacts
   - connector: API Infusion Pump Disconnect Schedule - eCM
      - scheduler: InfusionPumpDisconnect
   - event / flow / route: infusion.pump.disconnect.schedule
<br>

- files
   - [connector_infusion_pump_disconnect.bft](connector_infusion_pump_disconnect.bft): contains only the 'connector' artifact.
   - [event_infusion_pump_disconnect.bft](event_infusion_pump_disconnect.bft): contains only the 'event' artifact.
   - [flow_infusion_pump_disconnect.bft](flow_infusion_pump_disconnect.bft): contains only the 'flow' artifact.
   - [route_infusion_pump_disconnect.bft](route_infusion_pump_disconnect.bft): contains only the 'route' artifact.
   - [infusion_pump_disconnect.bft](infusion_pump_disconnect.bft): contains the connector, event, flow, and route artifacts.
<br>

- Import sequence suggestion:
   - [Groups](../infusion_pump_groups.bft)
   - [Artifacts](infusion_pump_disconnect.bft)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/icca/infusionpump)
