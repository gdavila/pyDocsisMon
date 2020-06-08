#!/bin/python3.4
# SNMP interface definitions

from docsisMon.snmp import get_snmp, getNext_snmp, getTable_snmp, set_snmp

class SnmpIf():
    def __init__(self, ipMgmt):
        self.__ipMgmt=ipMgmt
        self.SnmpAttr= SnmpAttr()
    
    def get(self,*Objnames): return get_snmp(self.__ipMgmt, self.SnmpAttr, *Objnames)
    def getNext(self, *Objnames): return getNext_snmp(self.__ipMgmt, self.SnmpAttr, *Objnames)
    def getTable(self, *Objnames): return getTable_snmp(self.__ipMgmt, self.SnmpAttr, *Objnames)
    def set(self,*Objnames ) : return set_snmp(self.__ipMgmt, self.SnmpAttr, *Objnames)

class SnmpAttr():
    def __init__(self):
        self.COMMUNITY='public'
        self.TIMEOUT=5
        self.RETRIES= 5
        self.BULKCOUNT= 1
        self.IgnoreNonIncreasingOid= False
        self.LookupMib= False
        self.PORT= 161
        self.MAXROWS = 0
      