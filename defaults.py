#!/bin/python3.4

class snmp:	
    SNMP_COMMUNITY='public'
    SNMP_TIMEOUT=5
    SNMP_RETRIES=5
    SNMP_BULKCOUNT=1 #Max repetitions
    #SNMP_BULKCOUNT=1000
    SNMP_ignoreNonIncreasingOid=False
    SNMP_lookupMib=False
    SNMP_PORT=161
    #MAX_ROWS=100
    MAX_ROWS=0 #no limit to interaction for snmpwalk


