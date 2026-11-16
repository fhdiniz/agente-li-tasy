# inbound Vital Signs

Uses HL7 versions 2.3, 2.4 and 2.6

- [Groups](vital_signs_groups.bft)
   - eCM - Interoperability: all artifacts from all integrations.
   - eCM - Vital Signs: all artifacts of inbound Vital Signs integrations.
<br>

- [Connectors](connector)
   - API Vital Signs - eCM (HTTP)
      - path: api/vital-sign/ihe
      - path: api/vital-sign/ge
      - path: api/vital-sign/mdil
      - path: api/vital-sign/ph
   - API Vital Signs IHE - eCM (MLLP)
      - Company interface: IHE
   - API Vital Signs PIIC iX / MDIL - eCM (MLLP)
      - Company interface: PH
   - API Vital Signs GE - eCM (MLLP)
      - Company interface: GE
<br>

- [Transformations](transformation)
   - json-to-json (v2.3): vital.signs.interface.ORU_R01.v2.3
   - json-to-json (v2.4): vital.signs.interface.ORU_R01.v2.4
   - json-to-json (v2.6): vital.signs.interface.ORU_R01.v2.6
<br>

- [ORU_R01](ORU_R01) - Unsolicited transmission of an observation message
   - event: vital.signs.interface
   - flow / route: inbound.vital.signs.interface.ORU_R01
<br>

- Import sequence suggestion:
   - [Groups](vital_signs_groups.bft)
   - [Connectors](connector)
   - [Transformations](transformation)
   - [ORU_R01](ORU_R01)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/patient/src/main/java/com/philips/tasy/integration/patient/inbound/vitalsign)
