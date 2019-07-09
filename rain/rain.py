import mercury

class Reader:
    command_list = ['GetInfo', 'SaveFields', 'ReadFields', 'Reboot', 'ActivateUpdateMode', 'GetCfg', 'SetCfg', 'GetRZ', 'SetRZ', 'AddRZ', 'DelRZ']

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
        if cmd['Cmd'] not in self.command_list:
            CmdID=''
            if 'CmdID' in cmd and cmd['CmdID']!='':
                CmdID=cmd['CmdID']
            return {
                'Report':cmd['Cmd'],
                'CmdID':CmdID,
                'ErrID':20,
                'ErrDesc':'Command not supported',
                'ErrInfo':''
            }
    
        CmdID=''
        if 'CmdID' in cmd and cmd['CmdID']!='':
            CmdID=cmd['CmdID']
        return {
            'Report':cmd['Cmd'],
            'CmdID':CmdID,
            'ErrID':0,
            'ErrDesc':'Success',
            'ErrInfo':''
        }
        
