# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 17:56:14 2018

@author: gdavila
"""

import cmDevices


myIP= '10.32.173.143'
myCm = cmDevices.Cm(myIP)


print ("CM IP:\t", myIP)
print ("CM Model:\t", myCm.getModel())
print ("CM conected LAN Devices:\t", myCm.getLANdevices())
