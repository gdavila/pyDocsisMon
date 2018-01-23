# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 12:16:14 2018

@author: gdavila
"""

import cmDevices
import time
from snmp import SnmpError

#'10.82.170.204'

myIP= '10.32.173.143'
myCm = cmDevices.Cm(myIP)

#getting the CM Model
myCmModel = myCm.getModel()
print ("CM acceded via SNMP Interface")
print ("CM IP:\t", myIP)
print ("CM Model:\t", myCmModel)
print ("CM Firmware:\t", myCm.getSw_rev())
#Accesing to Docsis Interfaces
myCmDocIf = myCm.DocsIf()

#Getting the MAC address of Docsis Interfaces (CM)
myCmMac = myCmDocIf.getMac()
print ("CM Mac:\t", myCmMac)

#Getting the CHannel list
#myCmChannels = myCmDocIf.getChFreq()
#print ("CM Channel list:\t", myCmChannels )


#Getting the Channel list in partial services;
    # This method is just an aproximation/estimation for real partial service channels.
    # based on the up/down flap on the channel table entry
#PartialServ = myCmDocIf.getPartialSrvCh()
#print ("PartiServ Channel list:\t", PartialServ )



print ("Full Band Capture Information:")
#Gettingfull band capture information;
fbc = myCm.fbc()

fbc.inactivityTimeout = 30
fbc.firstFrequency = 500000000
fbc.lastFrequency =  700000000
fbc.span =  100000000
fbc.binsPerSegment = 250
fbc.noisebandwidth = 150
fbc.numberOfAverages = 1
fbc.config()
time.sleep(1)
iniTime = time.time()
result = 'data OK'
try:
    data = fbc.get()
    if data == {}: 
        result = 'data FAIL'
except SnmpError as e:
    result = e

endTime = time.time()
print("Modelo\t\t Fullband Response Time\t\t Result")
print(myCm.getModel() +'\t\t' + str(endTime-iniTime) + '\t\t'+ str(result))
