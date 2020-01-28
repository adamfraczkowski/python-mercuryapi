import mercury
import time
import threading
import requests

class ReadThread(threading.Thread):
    reader = None
    def __init__(self, event, reader):
        self.reader = reader
        threading.Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(2):
            read = self.reader.reader.read(1000)
            for i in range(len(read)):
                epc = str(read[i].epc)[2:-1]
                if epc not in self.reader.resultTable:
                    print(epc)
                    self.reader.resultTable.append(epc)
                    self.reader.sendResult(epc)

class Reader:
    reader = None
    stopFlag = threading.Event()
    readThread = None
    resultTable = []
    sendUrl = ""
    reading = False
    readZones = {}
    spotProfiles = {}
    banks =   {
            0:"reserved",
            1:"epc",
            2:"tid",
            3:"user"
        }

    def sendResult(self, valToSend):
        if self.sendUrl != "":
            requests.get(url = self.sendUrl, params = {"value":valToSend})

    def Connect(self):
        if self.uri:
            del self.reader
            #if self.reader:
            #    return
            self.reader = mercury.Reader(self.uri)
            self.readThread = ReadThread(self.stopFlag, self)
            self.reader.set_region("open")
            #self.reader.set_read_plan([2], "GEN2", bank=["epc"], read_power=2200)
            #read = self.reader.read(1000)
            #for i in range(len(read)):
            #    print(str(read[i].epc)[2:-1])
    
    def getNextID(self, source):
        newkey = 1
        if len(source) == 0:
            return newkey
        for key,value in source.items():
            if key > newkey:
                newkey = key
        return newkey + 1

    def __init__(self, uri=None):
        self.uri = uri
        self.reader = None
        if uri:
            self.Connect()
    
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
    
        CmdID=''
        if 'CmdID' in cmd and cmd['CmdID']!='':
            CmdID=cmd['CmdID']
        method=getattr(self, cmd['Cmd'], "NotSupported")
        if method=="NotSupported":
            return {
                'Report':cmd['Cmd'],
                'CmdID':CmdID,
                'ErrID':20,
                'ErrDesc':'Command not supported',
                'ErrInfo':''
            }
        return method(cmd)

    ###################################################################
    # ThisTag
    ###################################################################

    def ThisTag(self, cmd):
        if ('Prof' in cmd) and (cmd['Prof']!='' and isinstance(cmd['Prof'], list)):                                 #if there's Spot Profile list in the command
            for prof_i in cmd['Prof']:                                                                              #for each Spot Profile 
                if prof_i in self.spotProfiles:
                    prof = self.spotProfiles[prof_i]
                    if ('ReadZone' in prof) and (prof['ReadZone']!='' and isinstance(prof['ReadZone'], list)):      
                        for rz_i in prof['ReadZone']:                                                                #for each Read Zone for that profile
                            if rz_i in self.spotProfiles:
                                rz = self.readZones[rz_i]
                                bankstoread = []
                                for bank in prof["Read"]:
                                    bankstoread.append(self.banks[bank[0]]) 
                                self.reader.set_read_plan(rz["Ants"], "GEN2", bank = bankstoread, read_power = (rz["ReadPwr"] * 100))
                                read = self.reader.read(1000)
                                print("read tags:")
                                for i in range(len(read)):
                                    epc = str(read[i].epc)[2:-1]
                                    self.reader.sendResult(epc)
                                    print(epc)
        return {
            'Report':cmd['Cmd'],
            'CmdID':cmd['CmdID'],
            'ErrID':0,
            'ErrDesc':'No error(s)',
            'ErrInfo':''
        }    

    ###################################################################
    # SPOT PROFILES
    ###################################################################
    
    def GetProf(self, cmd):
        if ('ID' in cmd) and (cmd['ID']!=None and isinstance(cmd['ID'], int)):
            prof = self.spotProfiles[cmd['ID']]
            prof['Report']:"GetProf"
            prof['ErrID']:0
            prof['ErrDesc']:'No error(s)'
            prof['ErrInfo']:''
            return prof
        else:
            return {
                'Report':cmd['Cmd'],
                'CmdID':cmd['CmdID'],
                'ID': cmd['ID'],
                'ErrID':32,
                'ErrDesc':'Illegal SpotProfile',
                'ErrInfo':[cmd['ID']]
            }
    
    def AddProf(self, cmd):
        cmd['ID'] = self.getNextID(self.spotProfiles)
        self.spotProfiles[cmd['ID']] = cmd
        return {
            'Report':cmd['Cmd'],
            'CmdID':cmd['CmdID'],
            'ID': cmd['ID'],
            'ErrID':0,
            'ErrDesc':'No error(s)',
            'ErrInfo':''
        }

    def DelProf(self, cmd):
        if ('ID' in cmd) and (cmd['ID']!='' and isinstance(cmd['ID'], list)):
            for id in cmd['ID']:
                self.spotProfiles.pop(id, None)
        else:            
            return {
                'Report':cmd['Cmd'],
                'CmdID':cmd['CmdID'],
                'ErrID':42,
                'ErrDesc':'SpotProfile definition error',
                'ErrInfo':['ID']
            }
            
        return {
            'Report':cmd['Cmd'],
            'CmdID':cmd['CmdID'],
            'ErrID':0,
            'ErrDesc':'No error(s)',
            'ErrInfo':''
        }

    ###################################################################
    # READ ZONES
    ###################################################################

    def AddRZ(self, cmd):
        cmd['ID'] = self.getNextID(self.readZones)
        self.readZones[cmd['ID']] = cmd            
        return {
            'Report':cmd['Cmd'],
            'CmdID':cmd['CmdID'],
            'ID': cmd['ID'],
            'ErrID':0,
            'ErrDesc':'No error(s)',
            'ErrInfo':''
        }

    def GetRZ(self, cmd):
        if ('ID' in cmd) and (cmd['ID']!=None and isinstance(cmd['ID'], int)):
            rz = self.readZones[cmd['ID']]
            rz['Report']:"GetRZ"
            rz['ErrID']:0
            rz['ErrDesc']:'No error(s)'
            rz['ErrInfo']:''
            return rz
        else:
            return {
                'Report':cmd['Cmd'],
                'CmdID':cmd['CmdID'],
                'ID': cmd['ID'],
                'ErrID':32,
                'ErrDesc':'Illegal SpotProfile',
                'ErrInfo':[cmd['ID']]
            }

    def DelRZ(self, cmd):
        if ('ID' in cmd) and (cmd['ID']!='' and isinstance(cmd['ID'], list)):
            for id in cmd['ID']:
                self.readZones.pop(id, None)
        else:            
            return {
                'Report':cmd['Cmd'],
                'CmdID':cmd['CmdID'],
                'ErrID':42,
                'ErrDesc':'ReadZone definition error',
                'ErrInfo':['ID']
            }
            
        return {
            'Report':cmd['Cmd'],
            'CmdID':cmd['CmdID'],
            'ErrID':0,
            'ErrDesc':'No error(s)',
            'ErrInfo':''
        }

    def StartRZ(self, cmd):
        self.resultTable.clear()
        if ('ID' in cmd) and (cmd['ID']!='' and isinstance(cmd['ID'], list)):
            for id in cmd['ID']:
                rz = self.readZones[id]

                for prof_i in self.spotProfiles:
                    prof = self.spotProfiles[prof_i]
                    if ('ReadZone' in prof) and (prof['ReadZone']!='' and isinstance(prof['ReadZone'], list)):      #check if read zone is included in one of spot profiles
                        bankstoread = []
                        for bank in prof["Read"]:
                            bankstoread.append(self.banks[bank[0]]) 
                        self.reader.set_read_plan(rz["Ants"], "GEN2", bank = bankstoread, read_power = (rz["ReadPwr"] * 100))

                        #read = self.reader.read(1000)
                        print("Start read thread")
                        self.readThread.start()

        else:            
            return {
                'Report':cmd['Cmd'],
                'CmdID':cmd['CmdID'],
                'ErrID':1,
                'ErrDesc':'Bad message',
                'ErrInfo':['ID']
            }

    def StopRZ(self, cmd):

        print("Stop read thread")
        self.stopFlag.set()
        return {
            'Report':cmd['Cmd'],
            'CmdID':cmd['CmdID'],
            'ID': cmd['ID'],
            'ErrID':0,
            'ErrDesc':'No error(s)',
            'ErrInfo':''
        }

    def GetInfo(self, cmd):
        return {
            'Report':cmd['Cmd'],
            'CmdID':cmd['CmdID'],
            'ErrID':0,
            'ErrDesc':'No error(s)',
            'ErrInfo':''
        }
        
