# Document Data Export

Uses HL7 v2.4

- [Groups](doc_exp_groups.bft)
   - eCM - Interoperability: all artifacts from all integrations.
   - eCM - Document Data Export: all artifacts of outbound Document Data Export integration.
   - eCM - Document Data Export - mappings: all outbound Document Data Export integration mappings.
<br>

- [Mappings](mapping): outbound.gender, outbound.marital.status
<br>

- [Transformations](transformation)
   - json-to-hl7: eCM.MDM_T01.v2.4
   - json-to-hl7: eCM.MDM_T07.v2.4
<br>

- [MDM_T01](MDM_T01_T07) - Original document notification
   - event: document.data.export
   - flow / route: outbound.document.data.export.MDM_T01_T07
   - json-to-hl7: eCM.MDM_T01.v2.4
- [MDM_T07](MDM_T01_T07) - Document edit notification
   - event: document.data.export
   - flow / route: outbound.document.data.export.MDM_T01_T07
   - json-to-hl7: eCM.MDM_T07.v2.4
<br>

- Import sequence suggestion:
   - [Groups](doc_exp_groups.bft)
   - [Mappings](mapping)
   - [Transformations](transformation)
   - [MDM_T01/MDM_T01](MDM_T01_T07)
<br>
