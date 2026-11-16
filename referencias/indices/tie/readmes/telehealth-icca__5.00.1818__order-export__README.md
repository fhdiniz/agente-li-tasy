# order-export-01.00.00

This integration is meant send data via MLLP in HL7 format.

The data is based on the CPOE

### Aritifact contains following components

Artifacts are grouped as "ICCA - Order Export"

No connector is being sent. This integration is activated through direct use of the events.


1. Connectors - None

2. Event list
	prescription.recommendation.order.request		
	prescription.diet.order.request		
	prescription.gas.order.request		
	prescription.medicine.order.request		
	prescription.hemotherapy.order.request		
	prescription.dialysis.order.request		
	prescription.procedure.order.request	

2. Routes - every event has their own route and flow
	prescription.recommendation.order.request		
	prescription.diet.order.request		
	prescription.gas.order.request		
	prescription.medicine.order.request		
	prescription.hemotherapy.order.request		
	prescription.dialysis.order.request		
	prescription.procedure.order.request

3. Flows - every flow belongs to their own route and event
	prescription.recommendation.order.request		
	prescription.diet.order.request		
	prescription.gas.order.request		
	prescription.medicine.order.request		
	prescription.hemotherapy.order.request		
	prescription.dialysis.order.request		
	prescription.procedure.order.request		


4. Transformation - JSON to HL7 transformations
JSON to HL7	ORM_O01_Recommendation_Order		
JSON to HL7	ORM_O01_Diet_Order		
JSON to HL7	OMP_O09_Diet_Order		
JSON to HL7	ORM_O01_Gas_Order		
JSON to HL7	OMP_O09_Medicine_Order		
JSON to HL7	OMP_O09_Hemo_Order		
JSON to HL7	ORM_O01_Hemo_Order		
JSON to HL7	OMP_O09_Dial_Order		
JSON to HL7	ORM_O01_Proced_Order		
JSON to HL7	OMP_O09_Proced_Order		
