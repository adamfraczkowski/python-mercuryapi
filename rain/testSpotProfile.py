import unittest
from rain import Reader
import time

ID1 = 0
ID2 = 0
class TestSpotProfile(unittest.TestCase):
    reader = Reader()

    cmd =   {
                "Cmd":"AddProf",
                "CmdID":"17263571356",
                "DwnCnt":-1,
                "EncodingType":'ALL',
                "FirstSeen":True,
                "ID":1,
                "InterpretData":[],
                "LastSeen":False,
                "MBMask":[[]],
                "Priority":0,
                "Read":[[]],
                "ReadZone":[0],
                "ReportPC":False,
                "ReportSensor":False,
                "Seen":False,
                "Write":[[]]
            }


    def test_AddProf_1(self):
        response = self.reader.command(self.cmd)
        global ID1
        ID1 = response['ID']
        self.assertEqual(
            response, 
            {
                'Report':'AddProf',
                'CmdID':'17263571356',
                'ID':ID1,
                'ErrID':0,
                'ErrDesc':'No error(s)',
                'ErrInfo':''
            }, 'AddProf first command')
        self.assertIn(response['ID'], self.reader.spotProfiles, 'AddProf profile saved')

    def test_AddProf_2(self):
        response = self.reader.command(self.cmd)
        global ID2
        ID2 = response['ID']
        self.assertEqual(
            response, 
            {
                'Report':'AddProf',
                'CmdID':'17263571356',
                'ID':ID2,
                'ErrID':0,
                'ErrDesc':'No error(s)',
                'ErrInfo':''
            }, 'AddProf second command')
        self.assertIn(response['ID'], self.reader.spotProfiles, 'AddProf profile saved')

    def test_AddProf_3(self):
        self.assertNotEqual(ID1, ID2, 'AddProf two consecutive IDs are same')

    def test_DelProf_misformed_SpotProfiles_list(self):
        self.assertEqual(
            self.reader.command(
                {
                    'Cmd':'DelProf',
                    'CmdID':'1234567890',
                    'ID': 123
                }
            ), 
            {
                'Report':'DelProf',
                'CmdID':'1234567890',
                'ErrID':42,
                'ErrDesc':'SpotProfile definition error',
                'ErrInfo':['ID']
            }, 'DelProf misformed command not detected')

    def test_DelProf(self):
        self.assertIn(ID1, self.reader.spotProfiles, 'DelProf profile not in profiles dict')
        self.assertIn(ID2, self.reader.spotProfiles, 'DelProf profile not in profiles dict')
        self.assertEqual(
            self.reader.command(
                {
                    'Cmd':'DelProf',
                    'CmdID':'1234567890',
                    'ID': [ID1, ID2]
                }
            ), 
            {
                'Report':'DelProf',
                'CmdID':'1234567890',
                'ErrID':0,
                'ErrDesc':'No error(s)',
                'ErrInfo':''
            }, 'DelProf command result')
        self.assertNotIn(ID1, self.reader.spotProfiles, 'DelProf profile not deleted')
        self.assertNotIn(ID2, self.reader.spotProfiles, 'DelProf profile not deleted')