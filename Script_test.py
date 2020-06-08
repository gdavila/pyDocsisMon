#!/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 17:43:47 2017

@author: gdavila
"""


'''Example

     - This example get some information about a CM by knowing its MAC address 
     and the CMTS that it belongs.

     - If you already know the CM IP address you can access it directly

                  ------                      -------
                 | myCM |--------------------| myCMTS |
                  ------                      ------- 
        MAC: 80d04a097cec              IP: 10.101.248.14
'''



from docsisMon.cmtsDevices import Cmts
from docsisMon.cmDevices import Cm
import time



# 1 Defining the CMTS  as an object through its IP.
myCmts=Cmts('10.101.248.14')

# 2 changing the default SNMP COMMUNITY
myCmts.snmpIf.SnmpAttr.COMMUNITY='private'


# 3 Getting a CM inside the CMTS as an object through its MAC
myVirtualCm=myCmts.getCm('80d04a097cec')
myIP = myVirtualCm.getIP()
print ("Virtual CM inside the CMTS:")
print ("CM IP:\t", myIP, "\t PtrCM in CMTS:\t", myVirtualCm.getPtr())


# 4 Defining the  CM as an object based on the IP obtained from de CMTS
myCm = Cm(myIP)
myCm.snmpIf.SnmpAttr.COMMUNITY='private'

# 5 getting the CM Model
myCmModel = myCm.getModel()
print ("CM acceded via SNMP Interface")
print ("CM IP:\t", myIP)
print ("CM Model:\t", myCmModel)

# 6 Accesing to Docsis Interfaces
myCmDocIf = myCm.DocsIf()

# 7 Getting the MAC address 
myCmMac = myCmDocIf.getMac()
print ("CM Mac:\t", myCmMac)

# 8 Getting the Channel list the CM is registered on
myCmChannels = myCmDocIf.getChFreq()
print ("CM Channel list:\t", myCmChannels )


# 9 Getting the list of channles who are in partial service status
PartialServ = myCmDocIf.getPartialSrvCh()
print ("PartiServ Channel list:\t", PartialServ )



