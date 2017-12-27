#!/bin/python3.4
# SNMP interface definitions

import defaults
from snmp import get_snmp, getNext_snmp, getTable_snmp, set_snmp

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
        self.COMMUNITY=defaults.snmp.SNMP_COMMUNITY
        self.TIMEOUT=defaults.snmp.SNMP_TIMEOUT
        self.RETRIES= defaults.snmp.SNMP_RETRIES
        self.BULKCOUNT=defaults.snmp.SNMP_BULKCOUNT
        self.IgnoreNonIncreasingOid=defaults.snmp.SNMP_ignoreNonIncreasingOid
        self.LookupMib= defaults.snmp.SNMP_lookupMib
        self.PORT= defaults.snmp.SNMP_PORT
        self.MAXROWS = defaults.snmp.MAX_ROWS
        
    def get_community(self): return self.COMMUNITY
    def get_timeout(self): return self.TIMEOUT
    def get_retries(self): return self.RETRIES
    def get_bulkcount(self): return self.BULKCOUNT
    def get_ignorenonincreasingoid(self): return self.IgnoreNonIncreasingOid
    def get_lookupmib(self): return self.LookupMib
    def get_port(self): return self.PORT
    def get_maxrows(self): return self.MAXROWS
    
    def set_community(self,comm): self.COMMUNITY=comm
    def set_timeout(self, timeout): self.TIMEOUT=timeout
    def set_retries(self, retries): self.RETRIES=retries
    def set_bulkcount(self, bulkcount): self.BULK_COUNT=bulkcount
    def set_ignorenonincreasingoid(self): self.IgnoreNonIncreasingOid=True
    def unset_ignorenonincreasingoid(self): self.IgnoreNonIncreasingOid=False
    def set_lookupmib(self): self.LookupMib=True
    def unset_lookupmib(self): self.LookupMib=False
    def set_port(self, port): self.PORT=port
    def set_maxrows(self, maxrows): self.MAXROWS=maxrows