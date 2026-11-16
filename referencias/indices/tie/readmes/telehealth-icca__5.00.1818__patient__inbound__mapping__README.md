# mappings

- file with the mappings of this integration: [mappings_adt.bft](mappings_adt.bft)
<br>

- Uses common mappings with other integrations
   - [doctor](../../../common/mapping-inbound/doctor.bft)
   - [gender](../../../common/mapping-inbound/gender.bft)
   - [message.identifier.type](../../../common/mapping-inbound/message.identifier.type.bft)
   - [patient.identification.segment](../../../common/mapping-inbound/patient.identification.segment.bft)
<br>

- Mapping by constants, with predetermined values.
   - [action.code](action.code.bft)
   - [allergy.clinical.status](allergy.clinical.status.bft)
   - [allergy.severity](allergy.severity.bft)
   - [care.type](care.type.bft)
   - [contact.description](contact.description.bft)
   - [contact.type](contact.type.bft)
   - [marital.status](marital.status.bft)
   - [sensitivity.causative.agent](sensitivity.causative.agent.bft)
<br>

- It is necessary that the mapping is done by the client, informing the registration ID.
   - [allergen.type](allergen.type.bft)
      - function: Core tables Settings > Main Application > Physician > Allergens
   - [language](language.bft)
      - function: Core tables Settings > Main Application > Core tables Settings > Languages
   - [nationality](nationality.bft)
      - function: Core tables Settings > Main Application > Core tables Settings > Nationality
   - [patient.profile](patient.profile.bft)
      - function: ?
   - [professional.responsible.allergy](professional.responsible.allergy.bft)
      - function: Master Person Index
   - [race](race.bft)
      - function: Core tables Settings > Main Application > Core tables Settings > Skin Color
   - [religion](religion.bft)
      - function: Core tables Settings > Main Application > Core tables Settings > Religion
   - [source.of.admission](source.of.admission.bft)
      - function: ?