import unittest
from rain import Reader
import time

RZ_ID = 0
Prof_ID = 0

class TestContinuousRead(unittest.TestCase):
    reader = Reader("tmr:///com4")

    #**********************************************
    # Add Read Zone
    #**********************************************
    def test_Read(self):
        #Add new Read Zone
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
        global RZ_ID
        RZ_ID = response['ID']
        self.assertEqual(
            response, 
            {
                'Report':'AddRZ',
                'CmdID':'17263571356',
                'ID':RZ_ID,
                'ErrID':0,
                'ErrDesc':'No error(s)',
                'ErrInfo':''
            }, 'AddRZ first command')
        self.assertIn(RZ_ID, self.reader.readZones, 'AddRZ read zone saved')        
        #**********************************************
        # Add Spot Profile
        #**********************************************
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
        global Prof_ID
        Prof_ID = response['ID']
        self.assertEqual(
            response, 
            {
                'Report':'AddProf',
                'CmdID':'17263571357',
                'ID':Prof_ID,
                'ErrID':0,
                'ErrDesc':'No error(s)',
                'ErrInfo':''
            }, 'AddRZ first command')
        self.assertIn(Prof_ID, self.reader.spotProfiles, 'AddProf spot profile saved')

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


        #self.reader.set_region("open")
        #self.reader.set_read_plan([2], "GEN2", bank=["epc"], read_power=2200)
        #read = self.reader.read(1000)
        #for i in range(len(read)):
        #    print(str(read[i].epc)[2:-1])
        #self.reader.set_read_plan()