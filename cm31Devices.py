# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:09:02 2018

@author: gdavila
"""

from docsisDevice import DocsisDevice
from cmDevices import *

class Cm31(Cm):
    
    def __init__(self,ip):
        Cm.__init__(self, ip)
        self.__deviceType=DocsisDevice.cm31()
        self.__pnm = pnm(self.snmpIf)
        

class pnm():
    def __init__(self,snmpIf):
        self.__snmpIf=snmpIf