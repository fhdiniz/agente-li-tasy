"# 

### My Health record

Integration with My health record system.  
Uses SOAP Calls with https4 Protocol for the communication between TASY and My health record system.

Communication will start from Tasy and then data in JSON will be sent to Direct Control which inturn DirectControl
will send Success or Failure to Tasy

The following are the messages which we will be part of the integration between TASY and MHR
1.create.file.EventSummary-Flow for processing and saving the Event Summary file, which will be used later to upload to My Health Records System.
2.send.EventSummaryUploadDocument-This flow is to upload patient Event Summary details to a patient's My Health record.
3.send.EventSummary.SupersedDocument-This flow is to supersed the  patient Event Summary details to a patient's My Health record.
4.create.DischargeSummaryFile-This flow is to upload patient Discharge Summary details to a patient's My Health record
5.send.DischargeSummaryUploadDocument-This flow is to upload patient Discharge summary details to a patient's My Health record
6.send.DischargeSummarySupersedeDocument-This flow is to supersed the  patient Discharge Summary details to a patient's My Health record
7.downloadDocument-this flow is to download the patient health summary documents from my health record database
8.removeMhrDocument- this flow is to remove the uploaded health summary document from my health record database
"









