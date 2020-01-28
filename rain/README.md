# **Reader** class
This class is a RAIN compliant API. Full documentation is available here: https://rainrfid.org/wp-content/uploads/2018/09/RAIN-RFID-RCI-v1.pdf

## 1. Create object:
``` 
reader = Reader("tmr:///com4")
```

## 2. Tag single read:
First you need to create read zone (RZ):
```
cmd =   {
    "Cmd":"AddRZ",
    "CmdID":"17263571356",
    "Ants":[2],
    "ReadPwr":22,
    "WritePwr":22,
    "DutyCycle":[100,1000,0],
    "ReadPwrAnt":[22,22],
    "WritePwrAnt":[22,22],
    "DutyCycleAnt":[[100,1000,0],[100,1000,0]],
    "StartTrigger":[[]],
    "StopTrigger":[[]],
    "Q":1,
    "Session":0,
    "Target":"NONE",
    "SelectFlag":"NONE"
}
response = self.reader.command(cmd)
RZ_ID = response['ID']
```
Now, having id of your new read zone in RZ_ID, you can create spot profile:
```
cmd =   {
    "Cmd":"AddProf",
    "CmdID":"17263571357",
    "DwnCnt":-1,
    "EncodingType":'ALL',
    "FirstSeen":True,
    "InterpretData":[],
    "LastSeen":False,
    "MBMask":[[]],
    "Priority":0,
    "Read":[[2,0,6,3]],         #banks: 00b = reserved, 01b = epc, 10b = tid, 11 = user | start word, word count, retries
    "ReadZone":[RZ_ID],
    "ReportPC":False,
    "ReportSensor":False,
    "Seen":False,
    "Write":[[]]
}
response = self.reader.command(cmd)
Prof_ID = response['ID']
```
Finally, you can trigger single read:
``` 
cmd =   {
    "Cmd":"ThisTag",
    'CmdID':'17263571358',
    "Prof":[Prof_ID]
}
self.reader.sendUrl = "http://localhost/tagread"
self.reader.command(cmd)
``` 
All readings will be send to reader.sendUrl as GET requests, one by one, using query param "value":  ?value=<read_value>

## 3. Tag continuous read:
First define spot profile and read zone as shown in single read example. Then use command "StartRZ" like this:
``` 
cmd =   {
    "Cmd":"StartRZ",
    'CmdID':'17263571358',
    "ID":[RZ_ID]
}
self.reader.sendUrl = "http://localhost/tagread"
self.reader.command(cmd)
time.sleep(30)
cmd =   {
    "Cmd":"StopRZ",
    'CmdID':'17263571358',
    "ID":[RZ_ID]
}
self.reader.command(cmd)
``` 
This example will activate read zone for 30 secs and send results to specified url.
You can find working examples in test .py files: testRead.py and testContinuousRead.py