# Infusion Pump - Interface

Uses HL7 v2.4

- [Groups](../infusion_pump_groups.bft)
   - eCM - Interoperability: all artifacts from all integrations.
   - eCM - Infusion Pump: all artifacts of Infusion Pump integrations.
<br>

- [Connectors](connector)
   - API Infusion Pump - eCM (HTTP)
   - API Infusion Pump - eCM (MLLP)
   - API Infusion Pump - eCM (Client Server)
<br>

- [ORU_R01](ORU_R01) - Unsolicited transmission of an observation message
   - event: InfusionPump.Delivery.ORU_R01
   - flow / route: InfusionPump.Delivery.ORU_R01
   - flow / route (MDIL): InfusionPump.Delivery.ORU_R01.MDIL
<br>

- Import sequence suggestion:
   - [Groups](../infusion_pump_groups.bft)
   - [Connectors](connector)
   - [ORU_R01](ORU_R01)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/icca/infusionpump)
