# -*- coding: utf-8 -*-
from docsisDevice import DocsisDevice
from ipDevices import  ipDevice
from mibs import mibs

import private as defaults


class Cmts(ipDevice):
    """ Represents a CMTS
        
    """
    
    def __init__(self, ip):
        #inheritance from IP_device
        ipDevice.__init__(self,ip)
        #Setting SNMP community
        self.snmpIf.SnmpAttr.set_community(defaults. communities.COMM_CMTS)
        
        #setting deviceType to CMTS type
        self.__deviceType=DocsisDevice.cmts()
        
        #cm virtual is a CM object in a CMTS
        self.cm=CmInCmts
    
    def getCm(self, cmMac): 
        return self.cm(self.snmpIf, cmMac)



class CmInCmts():
    """Represents a CM in a CMTS acceced via snmpIf"""        
    def __init__(self,snmpIf, cmMac):
        self.snmpIf=snmpIf
        self.__deviceType=DocsisDevice.cmInCmts()
        self.__mac=cmMac
        self.__ptr=self.getPtr()
        self.__ip=self.getIP()
        
                
    def getPtr(self):
        oid = (mibs.oid['docsIfCmtsCmPtr']+'.'+getMacDec(self.__mac),)
        SnmpObj = self.snmpIf.get(*oid)
        return SnmpObj[mibs.oid['docsIfCmtsCmPtr']+'.'+getMacDec(self.__mac)]

    def getIP(self):
        if self.__ptr == None: return None
        oid = (mibs.oid['docsIfCmtsCmStatusIpAddress']+'.'+self.__ptr,)
        SnmpObj = self.snmpIf.get( *oid)
        return SnmpObj[mibs.oid['docsIfCmtsCmStatusIpAddress']+'.'+self.__ptr]
    
    def getStatus(self):
        if self.__ptr == None: return None
        oid = (mibs.oid['docsIfCmtsCmStatusValue']+'.'+self.__ptr,)
        SnmpObj = self.snmpIf.get( *oid)
        return SnmpObj[mibs.oid['docsIfCmtsCmStatusValue']+'.'+self.__ptr]

def getMacDec(cmMac):
    macDec= str(int('0x'+cmMac[0:2],16))+\
                    '.'+ str(int('0x'+cmMac[2:4],16))+\
                    '.'+str(int('0x'+cmMac[4:6],16))+\
                    '.'+str(int('0x'+cmMac[6:8],16))+\
                    '.'+str(int('0x'+cmMac[8:10],16))+\
                    '.'+str(int('0x'+cmMac[10:12],16))
    return macDec