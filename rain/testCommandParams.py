import unittest
from rain import Reader
import time

class TestCommandParams(unittest.TestCase):
    reader = Reader()

    def test_class_init(self):
        self.assertEqual(Reader().uri, None, 'Class init')

    def test_zero_length_command(self):
        self.assertEqual(self.reader.command(
            {
                'Cmd':'',
                'CmdID':'1234567890'
            }), 
            {
                'Report':'',
                'CmdID':'1234567890',
                'ErrID':1,
                'ErrDesc':'Command not provided',
                'ErrInfo':''
            }, 'Zero length command')

    def test_no_command(self):
        self.assertEqual(self.reader.command(
            {
                'CmdID':'1234567890'
            }), 
            {
                'Report':'',
                'CmdID':'1234567890',
                'ErrID':1,
                'ErrDesc':'Command not provided',
                'ErrInfo':''
            }, 'No command')

    def test_no_cmdid(self):
        self.assertEqual(self.reader.command(
            {
                'Cmd':''
            }), 
            {
                'Report':'',
                'CmdID':'',
                'ErrID':1,
                'ErrDesc':'Command not provided',
                'ErrInfo':''
            }, 'No CmdID')

    def test_command_not_supported(self):
        self.assertEqual(self.reader.command(
            {
                'Cmd':'qwe'
            }), 
            {
                'Report':'qwe',
                'CmdID':'',
                'ErrID':20,
                'ErrDesc':'Command not supported',
                'ErrInfo':''
            }, 'Command not supported')

    def test_command_supported(self):
        self.assertEqual(self.reader.command(
            {
                'Cmd':'GetInfo',
                'CmdID':'1234567890'
            }), 
            {
                'Report':'GetInfo',
                'CmdID':'1234567890',
                'ErrID':0,
                'ErrDesc':'No error(s)',
                'ErrInfo':''
            }, 'Command supported')
