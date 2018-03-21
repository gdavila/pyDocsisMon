# -*- coding: utf-8 -*-


from docsisDevice import DocsisDevice
from ipDevices import ipDevice
from mibs import mibs
import re
import private as defaults


class Cm(ipDevice):
    """Represents a CM"""
    
    #initialization based on cm IPv4
    def __init__(self,ip):
        #Inheritancee from class IP_device
        ipDevice.__init__(self, ip)
        self.__hw_rev = None
        self.__vendor = None
        self.__bootr = None
        self.__sw_rev = None
        self.__model = None
        
        #Setting device type to "CM"
        self.__deviceType=DocsisDevice.cm()
        
        #Setting the snmp cm community
        self.snmpIf.SnmpAttr.set_community(defaults.communities.COMM_CM)
        
        #Pass to DocsisIf the snmpIf used to get all the data
        self.__DocsIf=DocsIf(self.snmpIf)
        self.__fbc = fullbandCapture(self.snmpIf)
        self.updateSysdescr()
    
    #method: Interfaces Docsis active in cm
    def DocsIf(self):
        return self.__DocsIf
    
    def fbc(self):
        return self.__fbc
    
    def updateSysdescr(self):
       oid = (mibs.oid['sysdescr.0'],)
       SnmpObj = self.snmpIf.get( *oid) 
       if SnmpObj== None: return None
       sysdescr=list(SnmpObj.values())[0]
       result = re.search('HW_REV:(?P<hw_rev>[^;<>]+); VENDOR:(?P<vendor>[^;<>]+); '\
                          'BOOTR:(?P<bootr>[^;<>]+); SW_REV:(?P<sw_rev>[^;<>]+); '\
                           'MODEL:(?P<model>[^;<>]+)',sysdescr)
       self.__hw_rev = result.group('hw_rev').lstrip()
       self.__vendor = result.group('vendor').lstrip()
       self.__bootr = result.group('bootr').lstrip()
       self.__sw_rev = result.group('sw_rev').lstrip()
       self.__model = result.group('model').lstrip()
       return
   
    def getInOctets(self): 
        oid = (mibs.oid['ifHCInOctets']+'.'+self.__DocsIf.getIfMacIndex(), )
        SnmpObj = self.snmpIf.get( *oid)
        #if SnmpObj == None: return None
        return SnmpObj[mibs.oid['ifHCInOctets']+'.'+self.__DocsIf.getIfMacIndex()]
    
    def getModel(self): return self.__model
    def getSw_rev(self): return self.__sw_rev 
    def getVendor(self): return self.__vendor
    
    #method: Propietary SA mib
    def getLANdevices(self):
        oid = (mibs.oid['saRgIpMgmtLanAddrHostName'],)
        SnmpObj = self.snmpIf.getNext( *oid)
        #if SnmpObj == None: return None
        return (list(SnmpObj.values()))
    
    
class fullbandCapture():
    
    def __init__(self, snmpIf):
        self.__snmpIf=snmpIf
        self.inactivityTimeout = 480 
        self.firstFrequency = 50000000
        self.lastFrequency = 1000000000
        self.span = 10000000
        self.binsPerSegment = 250
        self.noisebandwidth = 150
        self.windowsFunction = 0
        self.numberOfAverages = 1
    
    def turnOff(self):
        setValues = [ (mibs.oid['docsIf3CmSpectrumAnalysisEnable'], 'Integer', 2),]
        self.__snmpIf.set(*setValues)
        return True
        
    def config(self):
        setValues = [ (mibs.oid['docsIf3CmSpectrumAnalysisInactivityTimeout'], 'Integer', self.inactivityTimeout),
                      (mibs.oid['docsIf3CmSpectrumAnalysisFirstSegmentCenterFrequency'],'Gauge', self.firstFrequency),
                      (mibs.oid['docsIf3CmSpectrumAnalysisLastSegmentCenterFrequency'],'Gauge', self.lastFrequency),
                      (mibs.oid['docsIf3CmSpectrumAnalysisSegmentFrequencySpan'],'Gauge', self.span),
                      (mibs.oid['docsIf3CmSpectrumAnalysisBinsPerSegment'],'Gauge',self.binsPerSegment),
                      (mibs.oid['docsIf3CmSpectrumAnalysisEquivalentNoiseBandwidth'], 'Gauge', self.noisebandwidth),
                      (mibs.oid['docsIf3CmSpectrumAnalysisNumberOfAverages'], 'Gauge', self.numberOfAverages), 
                      (mibs.oid['docsIf3CmSpectrumAnalysisEnable'], 'Integer', 1),
                    ] 
        self.__snmpIf.set(*setValues)
        return True
        
    def get(self):
        oids = (mibs.oid['docsIf3CmSpectrumAnalysisMeasAmplitudeData'],)
        #try:
        SnmpObj = self.__snmpIf.getTable(*oids)
        #except SnmpError as e: return e
        if SnmpObj == None: return None
        oid = mibs.oid['docsIf3CmSpectrumAnalysisMeasAmplitudeData']+'.'
        pattern = re.compile(oid)
        data = {}
        for key in SnmpObj.keys():
            if  pattern.match(key):
                freq = re.sub(pattern, '', key, count=0, flags=0)
                data[freq] = SnmpObj[key]
        return data

    
class DocsIf():
       """Represents Docsis Interfaces in a CM"""
       downstream_id="DS"
       upstream_id="US"
       
       #init
       def __init__(self,snmpIf):
           
           self.__snmpIf=snmpIf #Passing snmpif to access Docsis Interface
           self.__macIfIndex=None
           self.__index=[] #DocsisIf OID Index 
           self.__type={} #DocsusIf type: UP/DOWN
           self.__downSnr={} #SNR values for all DownDocsIf
           self.__corrCodewords = {}
           self.__uncorrCodewords = {}
           self.__unerrCodewords = {}
           self.__upSnr={} #SNR values for all DownDocsIf
           self.__chId={} #Channel ID values for all DocsIf
           self.__chFreq={} #Channel ID values for all DocsIf
           self.__downPower={}  #Power values for all DownDocsIf
           self.__partialSrvCh={}
           self.__operStatus={} #Operational status of all DocsIf
           self.__usRangingStatus={}  #Operational status of all UpstreamDocsIf
           self.update()
           self.__mac=self.__updateMac()
           self.updatePartialSrv()
           
       
       def __updateMac(self):
           oid =  (mibs.oid['ifPhysAddress']+'.'+ self.__macIfIndex,)
           SnmpObj = self.__snmpIf.get( *oid)
           if SnmpObj==None: return None
           return SnmpObj[mibs.oid['ifPhysAddress']+'.'+self.__macIfIndex]
           
       ################
       #Private Methods
       ################
       
       def __updateDownChValues(self, oid, value):
           SnmpObj = self.__snmpIf.getNext( *oid)
           if SnmpObj == None: return
           for i in self.__getDownChIndex():
               value[i]=SnmpObj[oid[0]+'.'+i]   
           return
       
       def __updateUpChValues(self, oid, value):
           SnmpObj = self.__snmpIf.getNext( *oid)
           if SnmpObj == None: return
           for i in self.__getUpChIndex():
               value[i]=SnmpObj[oid[0]+'.'+i]   
           return
       
       def __getDownChIndex(self):
           DownChIndex=[]
           if self.__index==[]: self.updateIndex()
           for i in self.__index:
               if self.__type[i]==DocsIf.downstream_id:
                   DownChIndex.append(i)
           return DownChIndex
     
       def __getUpChIndex(self):
           UpChIndex=[]
           if self.__index==[]: self.updateIndex()
           for i in self.__index:
               if self.__type[i]==DocsIf.upstream_id:
                   UpChIndex.append(i)
           return UpChIndex  
       
       def __updateDownChId(self):
           if self.__index==[]: self.updateIndex()
           self.__updateDownChValues((mibs.oid['docsIfDownChannelId'],), self.__chId)
           return
       
       def __updateDownChFreq(self):
           if self.__index==[]: self.updateIndex()
           self.__updateDownChValues((mibs.oid['docsIfDownChannelFrequency'],), self.__chFreq)
           return
       
       def __updateUpChId(self):
           if self.__index==[]: self.updateIndex()
           self.__updateUpChValues((mibs.oid['docsIfUpChannelId'],), self.__chId)
           return
       
       def __updateUpChFreq(self):
           if self.__index==[]: self.updateIndex()
           self.__updateUpChValues((mibs.oid['docsIfUpChannelFrequency'],), self.__chFreq)
           return
               
        ###############
        #Public Methods
        ###############
        
       def update(self):
           self.updateIndex()
           self.updateChId()
           self.updateChFreq()
           self.updateDownSnr()
           self.updateDownPower()
           self.updateOperStatus()
           self.updateCorrCodewords()
           self.updateUncorrCodewords()
           self.updateUnerrCodewords()
           return
           
       def updateIndex(self):
           self.__index=[]
           self.__type={}
           oid =  (mibs.oid['ifIndex'],)
           SnmpObj = self.__snmpIf.getNext( *oid)
           index=list(SnmpObj.values())
           oid =  (mibs.oid['ifType'],)
           SnmpObj = self.__snmpIf.getNext( *oid)
           for i in index:
               if SnmpObj[mibs.oid['ifType']+'.'+i]== '128' or SnmpObj[mibs.oid['ifType']+'.'+i]== '129':
                   self.__index.append(i)
                   if SnmpObj[mibs.oid['ifType']+'.'+i]== '128': self.__type[i]=DocsIf.downstream_id
                   if SnmpObj[mibs.oid['ifType']+'.'+i]== '129': self.__type[i]=DocsIf.upstream_id
               if SnmpObj[mibs.oid['ifType']+'.'+i]== '127':
                   self.__macIfIndex=i
           return
       
       def getIfMacIndex(self): return self.__macIfIndex
       
       def updateOperStatus(self): 
           self.__operStatus={}
           self.__usRangingStatus={}
           if self.__index==[]: self.updateIndex()
           oid =  (mibs.oid['ifOperStatus'],)
           SnmpObj = self.__snmpIf.getNext( *oid)
           for i in self.__index:
               self.__operStatus[i]=SnmpObj[mibs.oid['ifOperStatus']+'.'+i]
           oid =  (mibs.oid['docsIf3CmStatusUsRangingStatus'],)
           SnmpObj = self.__snmpIf.getNext( *oid)
           for i in self.__index:
               if self.__type[i]==DocsIf.upstream_id: 
                   self.__usRangingStatus[i]=SnmpObj[mibs.oid['docsIf3CmStatusUsRangingStatus']+'.'+i]
           return 
           
       def updateChId(self):
           self.__chId={}
           self.__updateDownChId()
           self.__updateUpChId()
           return self.__chId
       
       def updateChFreq(self):
           self.__chFreq={}
           self.__updateDownChFreq()
           self.__updateUpChFreq()
           return self.__chFreq
       
       def updateDownSnr(self):
           self.__downSnr={}
           if self.__index==[]: self.updateIndex()
           self.__updateDownChValues((mibs.oid['docsIfSigQSignalNoise'],), self.__downSnr)
           return self.__downSnr
       
       def updateDownPower(self):   
           self.__downPower={}
           if self.__index==[]: self.updateIndex()
           self.__updateDownChValues((mibs.oid['docsIfDownChannelPower'],), self.__downPower)
           return self.__downPower
                
       def updateCorrCodewords (self):
           self.__corrCodewords = {}
           if self.__index==[]: self.updateIndex()
           self.__updateDownChValues((mibs.oid['docsIfSigQCorrecteds'],), self.__corrCodewords)
           return self.__corrCodewords
       
       def updateUnerrCodewords (self):
           self.__unerrCodewords = {}
           if self.__index==[]: self.updateIndex()
           self.__updateDownChValues((mibs.oid['docsIfSigQUnerroreds'],), self.__unerrCodewords)
           return self.__unerrCodewords
        
       def updateUncorrCodewords (self):
           self.__uncorrCodewords = {}
           if self.__index==[]: self.updateIndex()
           self.__updateDownChValues((mibs.oid['docsIfSigQUncorrectables'],), self.__uncorrCodewords)
           return  self.__uncorrCodewords
        
       def updatePartialSrv(self):
           self.__partialSrvCh={}
           for index in self.__type.keys():
               if self.__type[index]==DocsIf.downstream_id:
                   if self.__downSnr[index]=='0' or  self.__operStatus[index]=='2':
                       self.__partialSrvCh[index]=self.__chId[index]
               if self.__type[index]==DocsIf.upstream_id:
                   if self.__usRangingStatus[index]!='4':
                       self.__partialSrvCh[index]=self.__chId[index]
           return self.__partialSrvCh
       
       def getPartialSrvCh(self): return self.__partialSrvCh
       
       def getPartialSrvStatus(self): 
           if self.__partialSrvCh=={}: return False
           else: return True
       def getIndex(self): return self.__index
       def getType(self): return self.__type
       def getDownSnr(self): return self.__downSnr
       def getDownPower(self): return self.__downPower
       def getCorrCodewords(self): return self.__corrCodewords
       def getUncorrCodewords(self): return self.__uncorrCodewords
       def getUnerrCodewords(self): return self.__unerrCodewords
       def getChId(self): return self.__chId
       def getChFreq(self): return self.__chFreq
       def getOperStatus(self): return self.__operStatus
       def getMac(self): return self.__mac


