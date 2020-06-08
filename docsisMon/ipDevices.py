#!/bin/python3.4
#Docsis Device Definition

from docsisMon.snmpIf import SnmpIf



class ipDevice():
    __id=0
    """Represents a Generic IP Device
        private atributes:
         - id: increase by each created ip device

        public atributes:
        - ipMngmt: Device Ip management
        - snmpIf: SNMP InterFace used to get all the infomation about the device
        
    
    """
    def __init__(self, ipMngmt):

        self.__id = ipDevice.__id
        ipDevice.__id +=1
        
        self.ipMngmt = ipMngmt
        self.snmpIf=SnmpIf(self.ipMngmt)
        
        

      