# PDE - patient data export

Uses HL7 v2.4

- [Groups](pde_groups.bft)
   - eCM - Interoperability: all artifacts from all integrations.
   - eCM - PDE: all artifacts of outbound PDE integration.
   - eCM - PDE - mappings: all outbound PDE integration mappings.
<br>

- [Mappings](mapping): field.bed, field.point.of.care, field.room, outbound.gender, outbound.marital.status
<br>

- [ORU_R01](ORU_R01) - Unsolicited transmission of an observation message
   - event: patient.data.export
   - flow / route: outbound.patient.data.export.ORU_R01
   - json-to-hl7: eCM.ORU_R01.v2.4
<br>

- Import sequence suggestion:
   - [Groups](pde_groups.bft)
   - [Mappings](mapping)
   - [ORU_R01](ORU_R01)
<br>
