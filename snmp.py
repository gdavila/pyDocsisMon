#!/bin/python3.4
#Snmp attributes defaults
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902

class SnmpError(Exception):
    """Class to manage SNMP errors"""
    pass

class SnmpSetError(Exception):
    """Class to manage SNMP errors"""
    pass

def makeSnmpObj_rfc1902(*args):
    oid_type=[]
    for oid, type, value in args:
        #print(oid, type, value)
        if type == 'Integer':
            obj = rfc1902.Integer(value)
        else:
            if type == 'Gauge':
                obj = rfc1902.Gauge32(value)
            else:
                raise SnmpSetError
        oid_type.append((oid, obj))   
    return(oid_type)
    
def set_snmp(ip, SnmpAttr, *oid_type_value):
    ObjSetNames = makeSnmpObj_rfc1902(*oid_type_value);
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
        cmdgen.CommunityData(SnmpAttr.get_community()),
        cmdgen.UdpTransportTarget((ip, SnmpAttr.get_port()),timeout=int(SnmpAttr.get_timeout()), retries=int(SnmpAttr.get_retries())),
        *ObjSetNames,
        lookupMib=SnmpAttr.get_lookupmib()
    )
    # Check for errors and print out results
    if errorIndication:
         raise SnmpError(errorIndication)
    else:
        if errorStatus:
            raise SnmpError(errorStatus,errorIndex,varBinds)   
        else:
            vars = {}
            for val, name in varBinds:
                vars[val.prettyPrint()] = name.prettyPrint()
    return(vars)
           

def get_snmp(ip, SnmpAttr, *Objnames):
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
        cmdgen.CommunityData(SnmpAttr.get_community()),
        cmdgen.UdpTransportTarget((ip, SnmpAttr.get_port()),timeout=int(SnmpAttr.get_timeout()), retries=int(SnmpAttr.get_retries())),
        *Objnames,
        lookupMib=SnmpAttr.get_lookupmib()
    )
    # Check for errors and print out results
    if errorIndication:
         raise SnmpError(errorIndication)
    else:
        if errorStatus:
            raise SnmpError(errorStatus,errorIndex,varBinds)
        else:
            vars = {}
            for val, name in varBinds:
                vars[val.prettyPrint()] = name.prettyPrint()
    return(vars)      
    
def getNext_snmp(ip, SnmpAttr, *Objnames):
    cmdGen = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.nextCmd(
        cmdgen.CommunityData(SnmpAttr.get_community()),
        cmdgen.UdpTransportTarget((ip, SnmpAttr.get_port()),timeout = int(SnmpAttr.get_timeout()), retries= int(SnmpAttr.get_retries())),
        maxRows=SnmpAttr.get_maxrows(),
        ignoreNonIncreasingOid=SnmpAttr.get_ignorenonincreasingoid(),
        lookupMib=SnmpAttr.get_lookupmib(),
        *Objnames
    )
    # Check for errors and print out results
    if errorIndication:
        raise SnmpError(errorIndication)
    else:
        if errorStatus:
            raise SnmpError(errorStatus,errorIndex,varBindTable)  
        else:
            vars = {}
            #print(varBindTable)
            for varBindTableRow in varBindTable:
                for val, name in varBindTableRow:
                    vars[val.prettyPrint()] = name.prettyPrint()
    return(vars)
   
def getTable_snmp(ip, SnmpAttr, *Objnames):
    
    cmdGen = cmdgen.CommandGenerator()
    #print ("******")
    #print (ip, *Objnames)
    #print ("******")
    #print (SnmpAttr.get_bulkcount())
    errorIndication, errorStatus, errorIndex, varBindTable = cmdGen.bulkCmd(
        cmdgen.CommunityData(SnmpAttr.get_community()),
        cmdgen.UdpTransportTarget((ip, SnmpAttr.get_port()),timeout = int(SnmpAttr.get_timeout()), retries= int(SnmpAttr.get_retries())),
        0, SnmpAttr.get_bulkcount(),
        *Objnames,
        lookupMib=SnmpAttr.get_lookupmib(),
    )
    # Check for errors and print out results
    if errorIndication:
        raise SnmpError(errorIndication)
    else:
        if errorStatus:
            raise SnmpError(errorStatus,errorIndex,varBindTable[-1][int(errorIndex)-1])
        else:
            vars = {}
            for varBindTableRow in varBindTable:
                for ObjectName, ObjectValue in varBindTableRow:
                    vars[ObjectName.prettyPrint()] = ObjectValue.prettyPrint()
                    #print('%s.... %s' % (( ObjectName.prettyPrint(), ObjectValue.prettyPrint() )))
    #print (vars)
    return(vars)    

