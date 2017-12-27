#!/bin/python3.4
#Docsis Device Definition

from snmpIf import SnmpIf



class ipDevice():
    __id=0
    """Represents a Generic IP Device"""
    def __init__(self, ipMngmt):
        
        #Device Ip management  
        self.__ipMngmt = ipMngmt
        
        #Information About the device i.e., SysDescr, Model, Firmware, etc
        self.__about = None
        
        #Id ti identify each IP device
        self.__id = ipDevice.__id
        
        ipDevice.__id +=1
        
        
        #SNMP InterFace used to get all the infomation about the device
        self.snmpIf=SnmpIf(self.__ipMngmt)
        
        #Later could be possible to add more interfaces like ssh, telnet, tr-069 within a class
        #... 
        #self.sshIf
        #self.telnetIf
        #self.tr069If
        

      