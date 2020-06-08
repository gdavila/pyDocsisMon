# pyDocsisMon

Python Docsis Monitoring (`PyDocsisMon`)

## Summary

`PyDocsisMon` is a set of basic functions and definitions to work in estraightfoward maner with Docsis atribbutes through SNMP.

This library allows  to define:

* Cable Modem Termination System (CMTS)
* Cable Modem (CM)

`pyDocsisMon` uses SNMPv2 interface to get information about Docsis Atributes.

The main goal is to make an abstraction of the SNMP complexity to focus only on Docsis atributes.
Some examples about how to use this tool could be found in `Script_[files].py`. The examples scrips allows:

* Easily get information about a CM such as: Hardware version, Software Version, Docsis Interfaces Informacion, Docsis Channels Information, etc.
* Easily set features such as Full Band Channel .

More features could be added in a estraightfoward way by just adding new functions to each object. New MIBS could also be added.

## Example

```python

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
```

Output expected:

```json
CM acceded via SNMP Interface
CM IP:   192.168.0.10
CM Model:        F@ST3286
CM Mac:  0x80d04a097cec
CM Channel list:         {'3': '603000000', '48': '609000000', '49': '615000000', '50': '621000000', '51': '627000000', '52': '633000000', '53': '639000000', '54': '645000000', '4': '30200000', '80': '36600000'}
PartiServ Channel list:  {}
```
