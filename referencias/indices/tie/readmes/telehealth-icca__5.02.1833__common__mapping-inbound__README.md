# common inbound mappings

- Mapping by constants, with predetermined values.
   - [gender](gender.bft)
      - integrations: [ADT](../../patient/inbound), [Clinical Notes](../../clinical-notes/inbound), [PDI](../../patient-data-import), [Laboratory/Microbiology](../../laboratory)
   - [message.identifier.type](message.identifier.type.bft)
      - integrations: [ADT](../../patient/inbound), [Clinical Notes](../../clinical-notes/inbound), [PDI](../../patient-data-import)
   - [patient.identification.segment](patient.identification.segment.bft)
      - integrations: [ADT](../../patient/inbound), [Clinical Notes](../../clinical-notes/inbound), [PDI](../../patient-data-import)
   - [observation.result.status](observation.result.status.bft)
      - integrations: [Clinical Notes](../../clinical-notes/inbound), [PDI](../../patient-data-import), [Laboratory/Microbiology](../../laboratory)
<br>

- It is necessary that the mapping is done by the client, informing the registration ID.
   - [doctor](doctor.bft)
      - integrations: [ADT](../../patient/inbound), [Clinical Notes](../../clinical-notes/inbound), [PDI](../../patient-data-import), [Laboratory/Microbiology](../../laboratory)
      - function: Physician Record