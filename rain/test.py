import unittest
from rain import Reader

class TestCommandParams(unittest.TestCase):
    reader_uri = 'adres_czytnika'
    def test_class_init(self):
        self.assertEqual(Reader(self.reader_uri).uri, self.reader_uri, 'Class init')

    def test_zero_length_command(self):
        reader = Reader(self.reader_uri)
        self.assertEqual(reader.command(
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
        reader = Reader(self.reader_uri)
        self.assertEqual(reader.command(
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
        reader = Reader(self.reader_uri)
        self.assertEqual(reader.command(
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

if __name__ == '__main__':
    unittest.main()
