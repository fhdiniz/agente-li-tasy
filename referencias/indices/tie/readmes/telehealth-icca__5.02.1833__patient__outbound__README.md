# outbound ADT

Uses HL7 v2.4

- [Groups](outbound_adt_groups.bft)
   - eCM - Interoperability: all artifacts from all patient integrations.
   - eCM - ADT outbound: all artifacts of outbound ADT integrations.
   - eCM - ADT outbound - mappings: all outbound ADT integration mappings.
<br>

- [Mappings](mapping): outbound.gender, outbound.marital.status
<br>

- [ADT_A01](ADT_A01) - Admit/visit notification
   - event: patient.admission
   - flow / route: outbound.patient.admission.ADT_A01
   - json-to-hl7: eCM.ADT_A01.v2.4
- [ADT_A02](ADT_A02) - Transfer patient
   - event: patient.transfer
   - flow / route: outbound.patient.transfer.ADT_A02
   - json-to-hl7: eCM.ADT_A02.v2.4
- [ADT_A03](ADT_A03) - Discharge/end visit
   - event: patient.discharge
   - flow / route: outbound.patient.discharge.ADT_A03
   - json-to-hl7: eCM.ADT_A03.v2.4
- [ADT_A08](ADT_A08) - Update patient information
   - event: patient.registration.update
   - flow / route: outbound.patient.information.update.ADT_A08
   - json-to-hl7: eCM.ADT_A08.v2.4
- [ADT_A11](ADT_A11) - Cancel admit/visit
   - event: patient.admission.cancel
   - flow / route: outbound.patient.admission.cancel.ADT_A11
   - json-to-hl7: eCM.ADT_A11.v2.4
- [ADT_A12](ADT_A12) - Cancel transfer
   - event: patient.transfer.cancel
   - flow / route: outbound.patient.transfer.cancel.ADT_A12
   - json-to-hl7: eCM.ADT_A12.v2.4
- [ADT_A13](ADT_A13) - Cancel discharge/end visit
   - event: patient.discharge.cancel
   - flow / route: outbound.patient.discharge.cancel.ADT_A13
   - json-to-hl7: eCM.ADT_A13.v2.4
- [ADT_A47](ADT_A47) - Change patient identifier list
   - event: patient.identifier.update
   - flow / route: outbound.patient.identifier.update.ADT_A47
   - json-to-hl7: eCM.ADT_A47.v2.4
<br>

- Import sequence suggestion:
   - [Groups](outbound_adt_groups.bft)
   - [Mappings](mapping)
   - [ADT_A01](ADT_A01), [ADT_A02](ADT_A02), [ADT_A03](ADT_A03), etc.
