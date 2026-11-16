# order-import-01.00.00

This integration is meant receive data via MLLP or HTTP to import order data.

### Aritifact contains following components

Artifacts are grouped as "ICCA - Order Import"

1. Connectors
	API - ICCA (MLLP) - Order Import
	API - ICCA (HTTP) - Order Import 

1. Event list
	inbound.order.ORM_O01		
	inbound.order.RAS_O17		

2. Routes - every event has their own route and flow
	ICCA - Order Administration Import - RAS^O17 
	ICCA - Order Import - ORM^O01		

3. Flows - every flow belongs to their own route and event
	API - ICCA (MLLP) - Order Import		

4. Transformation - JSON to HL7 transformations
JSON to JSON	patient.information.register.ADT_A04_v2	
JSON to JSON	order.information.ORM_O01	
JSON to JSON	order.information.RDE_O11	
