# inbound ADT

Uses HL7 v2.4

- [Groups](adt_groups.bft)
   - eCM - Interoperability: all artifacts from all patient integrations.
   - eCM - ADT: all artifacts of inbound ADT integrations.
   - eCM - ADT - mappings: all inbound ADT integration mappings.
<br>

- [Connectors](connector)
   - API ADT - eCM (MLLP)
   - API ADT - eCM (HTTP)
<br>

- [Mappings](mapping): action.code, allergen.type, allergy.clinical.status, allergy.severity, care.type, contact.description, contact.type, doctor, gender, language, marital.status, message.identifier.type, nationality, patient.identification.segment, patient.profile, professional.responsible.allergy, race, religion, sensitivity.causative.agent, source.of.admission
<br>

- [Transformations](transformation)
   - json-to-json: patient.information.register.ADT_A04
   - json-to-json: patient.identifier.update.ADT_46_47
   - json-to-json: patient.swap.ADT_A17
<br>

- [ADT_A01](ADT_A01) - Admit/visit notification
   - event: patient.admission
   - flow / route: inbound.patient.admission.ADT_A01
   - json-to-json: patient.information.register.ADT_A04
- [ADT_A02](ADT_A02) - Transfer patient
   - event: patient.transfer
   - flow / route: inbound.patient.transfer.ADT_A02
   - json-to-json: patient.information.register.ADT_A04
- [ADT_A03](ADT_A03) - Discharge/end visit
   - event: patient.discharge
   - flow / route: inbound.patient.discharge.ADT_A03
   - json-to-json: patient.information.register.ADT_A04
- [ADT_A04](ADT_A04) - Register a patient
   - event: patient.information.register
   - flow / route: inbound.patient.information.register.ADT_A04
   - json-to-json: patient.information.register.ADT_A04
- [ADT_A08](ADT_A08) - Update patient information
   - event: patient.information.update
   - flow / route: inbound.patient.information.update.ADT_A08
   - json-to-json: patient.information.register.ADT_A04
- [ADT_A11](ADT_A11) - Cancel admit/visit
   - event: patient.admission.cancel
   - flow / route: inbound.patient.admission.cancel.ADT_A11
   - json-to-json: patient.information.register.ADT_A04
- [ADT_A12](ADT_A12) - Cancel transfer
   - event: patient.transfer.cancel
   - flow / route: inbound.patient.transfer.cancel.ADT_A12
   - json-to-json: patient.information.register.ADT_A04
- [ADT_A13](ADT_A13) - Cancel discharge/end visit
   - event: patient.discharge.cancel
   - flow / route: inbound.patient.discharge.cancel.ADT_A13
   - json-to-json: patient.information.register.ADT_A04
- [ADT_A17](ADT_A17) - Bed swap patients
   - event: patient.swap
   - flow / route: inbound.patient.swap.ADT_A17
   - json-to-json: patient.swap.ADT_A17
- [ADT_A31](ADT_A31) - Update person information
   - event: person.information.update
   - flow / route: inbound.person.information.update.ADT_A31
   - json-to-json: patient.information.register.ADT_A04
- [ADT_A46](ADT_A46_A47) - Change patient id
   - event: patient.identifier.update
   - flow / route: inbound.patient.identifier.update.ADT_46_47
   - json-to-json: patient.identifier.update.ADT_46_47
- [ADT_A47](ADT_A46_A47) - Change patient identifier list
   - event: patient.identifier.update
   - flow / route: inbound.patient.identifier.update.ADT_46_47
   - json-to-json: patient.identifier.update.ADT_46_47
- [ADT_A60](ADT_A60) - Update allergy information
   - event: allergy.information.update
   - flow / route: inbound.allergy.information.update.ADT_A60
   - json-to-json: patient.information.register.ADT_A04
<br>

- Import sequence suggestion:
   - [Groups](adt_groups.bft)
   - [Connectors](connector)
   - [Mappings](mapping)
   - [Transformations](transformation)
   - [ADT_A01](ADT_A01), [ADT_A02](ADT_A02), [ADT_A03](ADT_A03), etc.
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/telehealth/patient)
