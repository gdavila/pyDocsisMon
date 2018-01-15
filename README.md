# pyDocsisMon

Python Docsis Monitoring

# Summary

PyDocsisMon is a very draft library/tool to work in estraightfoward maner with Docsis atribbutes. 

This tool allows to define:

* Cable Modem Termination System (CMTS)
* Cable Modem (CM)
* Docsis Set Top Boxes (STB)

pyDocsisMon uses SNMPv2 interface to get information about each Docsis Object. It is just needed
to add your snmp credentials (communities) at private.py file.

Some examples about how to use this tool could be found in test.py

Clasess definition should be reviewed in order to better design the object oriented implementation of the library.

# Example

Download pyDocsisMon repository and edit private.py file with your credentials. (Be sure to untrack this changes from git)

```python

from cmDevices import Cm
import time

myIP = 'Insert here the Cm IP address'
#Example:
#myIP= '192.168.0.10'

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


print ("Full Band Capture Information:\t", PartialServ )
#Gettingfull band capture information;
fbc = myCm.fbc()
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
print(myCm.getModel() +'\t\t' + str(endTime-iniTime) + '\t\t'+ result)

```
Output expected:
```
CM acceded via SNMP Interface
CM IP:   192.168.0.10
CM Model:        F@ST3286
CM Mac:  0x8c10d4fd10a2
CM Channel list:         {'3': '603000000', '48': '609000000', '49': '615000000', '50': '621000000', '51': '627000000', '52': '633000000', '53': '639000000', '54': '645000000', '4': '30200000', '80': '36600000'}
PartiServ Channel list:  {}
Full Band Capture Information:   {}
Modelo           Fullband Response               Result
F@ST3286                26.49843430519104               OK

```
