import mercury

class Reader:
    def __init__(self, uri):
        self.uri = uri
    
    def command(self, cmd):
        if 'Cmd' not in cmd or cmd['Cmd'] is None or cmd['Cmd']=='':
            CmdID=''
            if 'CmdID' in cmd and cmd['CmdID']!='':
                CmdID=cmd['CmdID']
            return {
                'Report':'',
                'CmdID':CmdID,
                'ErrID':1,
                'ErrDesc':'Command not provided',
                'ErrInfo':''
            }
