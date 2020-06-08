# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 17:56:14 2018

@author: gdavila

This example uses a propietary MIB only available on Sagecom devices
to get information about the devices connected to the LAN interface of the CM
"""

import docsisMon.cmDevices as cmDevices


myIP= '10.32.173.143'
myCm = cmDevices.Cm(myIP)


print ("CM IP:\t", myIP)
print ("CM Model:\t", myCm.getModel())
print ("CM conected LAN Devices:\t", myCm.getLANdevices())
