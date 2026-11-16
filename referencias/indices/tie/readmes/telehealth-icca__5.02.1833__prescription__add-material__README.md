# Prescription - Add Material

HTTP protocol

- [Groups](add_material_groups.bft)
   - Prescription - Telehealth: all artifacts of all Prescription integrations.
<br>

- Artifacts
   - event / flow / route: prescription.addMaterial
   - [templates](template):
      - prescription.addMaterial.Lexicomp
      - prescription.addMaterial.OntoDrug
      - prescription.addMaterial.Vidal
      - prescription.addMaterial.Micromedex
      - prescription.addMaterial.return.Micromedex
      - prescription.addMaterial.return.Lexicomp
      - prescription.addMaterial.return.OntoDrug
      - prescription.addMaterial.return.Vidal
      - prescription.addMaterial.names.Micromedex
<br>

- files
   - [event_prescr_add_material.bft](event_prescr_add_material.bft): contains only the 'event' artifact.
   - [flow_prescr_add_material.bft](flow_prescr_add_material.bft): contains only the 'flow' artifact.
   - [route_prescr_add_material.bft](route_prescr_add_material.bft): contains only the 'route' artifact.
   - [prescr_add_material.bft](prescr_add_material.bft): contains the event, flow, and route artifacts.
   - [integration_prescription_add_material.bft](integration_prescription_add_material.bft): contais all the artifacts related to the integration.

- Monograph

   - [event_add_Material_Monograph.bft](event_add_Material_Monograph.bft): contains only the 'event' artifact.
   - [flow_add_Material_Monograph.bft](flow_add_Material_Monograph.bft): contains only the 'flow' artifact.
   - [route_add_Material_Monograph.bft](route_add_Material_Monograph.bft): contains only the 'route' artifact.
   
<br>

- Import sequence suggestion:
   - [Groups](add_material_groups.bft)
   - [Templates](template)
   - [Artifacts](prescr_add_material.bft)
<br>

[Link tasy-interfaces](https://github.com/philips-internal/tasy-interfaces/tree/dev/telehealth-icca/src/main/java/com/philips/tasy/integration/icca/infusionpump/material)
