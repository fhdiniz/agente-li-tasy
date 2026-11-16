# inbound ORU_R40

Register flags integration using the HL7 standard, below are the supported events.
Uses HL7 v2.8

- [Connectors](connector)
   - API - Register Flags (HTTP)
<br>

- [Mappings](mapping): alert.event.type
<br>

- [Transformations](transformation)
   - json-to-json: patient.alerts_2.8
<br>

- [ORU_R40](ORU_R40) - Unsolicited Alert Observation Message
   - event: register.flags
   - flow / route: inbound.register.flags.ORU_R40
   - json-to-json: patient.alerts_2.8
<br>

- Import sequence suggestion:
   - [Connectors](connector)
   - [Mappings](mapping)
   - [Transformations](transformation)
   - [ORU_R40](ORU_R40).
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/icca/registerflags)
