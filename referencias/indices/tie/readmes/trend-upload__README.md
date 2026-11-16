# trend-upload-01.00.00

### Aritifact contains following components

1. VitalSign TrendUpload Connector - The connector is designed to receive inbound request with payload containing HL7 standard json message format. The connector checks for the message type (MSH-9) and then triggers the event.
2. Event - There is a singular event that is mapped to the flow.
3. Flow - There is a singular flow that processes the message. The flow checks the hl7 message version before transforming it's json structure. The json, that has both vital sign and patient data, is submitted to Tasy Interfaces so it can be properly logged in the system.
4. Transformation - Json to Json transformation structure to prepare the received data.