"# 

### Direct Control

Integration with Direct Control system.  
Uses REST Calls with https4 Protocol for the communication between TASY and Direct Control

Communication will start from Tasy and then data in JSON will be sent to Direct Control which inturn DirectControl
will send Success or Failure to Tasy

The following are the messages which we will be part of the integration between TASY and Direct Control

1. Create Client - Patient Registered in TASY will be sent to Direct Control System 
2. Update Client - Modified Patient Details in Tasy will be sent to Direct Control System 
3. Verify Medicare - Patient Medicare number stored in Tasy will be Sent and Verified, Validated by DC.

-- Billing Process will start from here based on the procedures (MBS type) prescribed for the patient --

4. Transmit IHC - In Hospital Claims process will be performed in TASY and then DC will take care of billing.
5. Transmit PC 	- Patient Client process will be performed in TASY and then DC will take care of billing.
6. Transmit DVA/BB - DVA, Bulk Bill process will be performed in TASY and then DC will take care of billing.
7. OEC - Online Eligibility Check will be performed by Direct Control based on the data sent by TASY.
8. Private fund- Private Insurance Check will be performed by Direct Control based on the data sent by TASY.
9. ERA - ERA process will be handled by DirectControl based on the data sent by TASY.
"









