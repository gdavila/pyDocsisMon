#!/bin/python3.4
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 17:43:47 2017

@author: gdavila
"""


'''Example

     This example get some information about a CM by knowing its MAC address 
     and the CMTS the CM belongs.
                  ------                      -------
                 | myCM |--------------------| myCMTS |
                  ------                      ------- 
        MAC: 14987d310c6f              IP: 10.100.150.119
'''



from cmtsDevices import Cmts
from cmDevices import Cm

#Defining the CMTS  as an object
#Be sure to had loaded the right communities of your network in private.py/default.py
myCmts=Cmts('10.100.150.199')

#Defining a CM inside the CMTS as an object
myVirtualCm=myCmts.getCm('c8fb26869cf5')
myIP = myVirtualCm.getIP()
print ("Virtual CM inside the CMTS: \n")
print ("CM IP:\t", myIP, "\nPtrCM in CMTS:\t", myVirtualCm.getPtr())




# Defining the  CM as an object based on the IP obtained from de CMTS
# The method uses the given IP address to acces to the CM through SNMP interface
myCm = Cm(myIP)

#getting the CM Model
myCmModel = myCm.getModel()
print ("CM acceded via SNMP Interface")
print ("CM IP:\t", myIP)
print ("CM Model:\t", myCmModel)

#Accesing to Docsis Interfaces
myCmDocIf = myCm.DocsIf()

#Getting the MAC address of Docsis Interfaces (CM)
myCmMac = myCmDocIf.getMac()
print ("CM Mac:\t", myCmMac)

#Getting the CHannel list
myCmChannels = myCmDocIf.getChFreq()
print ("CM Channel list:\t", myCmChannels )


#Getting the Channel list in partial services;
    # This method is just an aproximation/estimation for real partial service channels.
    # based on the up/down flap on the channel table entry
PartialServ = myCmDocIf.getPartialSrvCh()
print ("PartiServ Channel list:\t", PartialServ )



'''fbc = myCm.fbc()
fbc.config()
fbc.inactivityTimeout = 480
fbc.firstFrequency = 50000000
fbc.lastFrequency =  70000000
fbc.span =  10000000
fbc.binsPerSegment = 1024
fbc.noisebandwidth = 150
fbc.numberOfAverages = 1
time.sleep(0.5)
iniTime = time.time()
data = fbc.get()
result = 'OK'
if data == {}: result = 'FAIL'
endTime = time.time()
print("Modelo\t\t Fullband Response \t\t Result")
print(cm.getModel() +'\t\t' + str(endTime-iniTime) + '\t\t'+ result)

'''