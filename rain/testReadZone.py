import unittest
from rain import Reader
import time

ID1 = 0
ID2 = 0
class TestReadZone(unittest.TestCase):
    reader = Reader()

    cmd =   {
                "Cmd":"AddRZ",
                "CmdID":"17263571356",
                "Ants":[1,2],
                "ReadPwr":32,
                "WritePwr":22,
                "DutyCycle":[100,1000,0],
                "ReadPwrAnt":[32,32],
                "WritePwrAnt":[22,22],
                "DutyCycleAnt":[[100,1000,0],[100,1000,0]],
                "StartTrigger":[[]],
                "StopTrigger":[[]],
                "Q":0,
                "Session":0,
                "Target":"NONE",
                "SelectFlag":"NONE"
            }


    def test_AddRZ_1(self):
        response = self.reader.command(self.cmd)
        global ID1
        ID1 = response['ID']
        self.assertEqual(
            response, 
            {
                'Report':'AddRZ',
                'CmdID':'17263571356',
                'ID':ID1,
                'ErrID':0,
                'ErrDesc':'No error(s)',
                'ErrInfo':''
            }, 'AddRZ first command')
        self.assertIn(response['ID'], self.reader.readZones, 'AddRZ read zone saved')

    def test_AddRZ_2(self):
        response = self.reader.command(self.cmd)
        global ID2
        ID2 = response['ID']
        self.assertEqual(
            response, 
            {
                'Report':'AddRZ',
                'CmdID':'17263571356',
                'ID':ID2,
                'ErrID':0,
                'ErrDesc':'No error(s)',
                'ErrInfo':''
            }, 'AddRZ second command')
        self.assertIn(response['ID'], self.reader.readZones, 'AddRZ read zone saved')

    def test_AddRZ_3(self):
        self.assertNotEqual(ID1, ID2, 'AddRZ two consecutive IDs are same')

    def test_DelRZ_misformed_RZ_list(self):
        self.assertEqual(
            self.reader.command(
                {
                    'Cmd':'DelRZ',
                    'CmdID':'1234567890',
                    'ID': 123
                }
            ), 
            {
                'Report':'DelRZ',
                'CmdID':'1234567890',
                'ErrID':42,
                'ErrDesc':'ReadZone definition error',
                'ErrInfo':['ID']
            }, 'DelRZ misformed command not detected')

    def test_DelRZ(self):
        self.assertIn(ID1, self.reader.readZones, 'DelRZ read zone not in zones dict')
        self.assertIn(ID2, self.reader.readZones, 'DelRZ read zone not in zones dict')
        self.assertEqual(
            self.reader.command(
                {
                    'Cmd':'DelRZ',
                    'CmdID':'1234567890',
                    'ID': [ID1, ID2]
                }
            ), 
            {
                'Report':'DelRZ',
                'CmdID':'1234567890',
                'ErrID':0,
                'ErrDesc':'No error(s)',
                'ErrInfo':''
            }, 'DelRZ command result')
        self.assertNotIn(ID1, self.reader.readZones, 'DelRZ read zone not deleted')
        self.assertNotIn(ID2, self.reader.readZones, 'DelRZ read zone not deleted')