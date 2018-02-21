# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:30:59 2018

@author: gdavila
"""
import cmDevices
import time
from snmp import SnmpError


def updateChValues(CmDocIf):
    CmDocIf.updateDownSnr()
    CmDocIf.updateCorrCodewords()
    CmDocIf.updateUncorrCodewords()


# definitions 
myIP= '10.254.1.46'
interval = 10 #seconds
duration = 120 #seconds


# create CM
myCm = cmDevices.Cm(myIP)


# Getting Basic Values
CmModel = myCm.getModel()
CmFw = myCm.getSw_rev()
CmDocIf = myCm.DocsIf()
ChId = CmDocIf.getChId()
ChFreq = CmDocIf.getChFreq()
CmMac = CmDocIf.getMac()
ChSnr = CmDocIf.getDownSnr()


ChCorrC_i, CorrC_timeStamp_i = CmDocIf.updateCorrCodewords(), time.time()
ChUncorrC_i, UncorrC_timeStamp_i = CmDocIf.updateUncorrCodewords(), time.time()
ChUnerrC_i, UnerrC_timeStamp_i = CmDocIf.updateUnerrCodewords(), time.time()

start = time.time()

ChCcer = {}
ChCer = {}

while (time.time()-start < duration):
    time.sleep(interval)
    timeStamp = time.time()
    ChCorrC_f, ChUncorrC_f, ChUnerrC_f = CmDocIf.updateCorrCodewords(), CmDocIf.updateUncorrCodewords(), CmDocIf.updateUnerrCodewords()
    ChSnr = CmDocIf.updateDownSnr()
    for ch in ChSnr.keys():
        ChCcer[ch] = round((int(ChCorrC_f[ch])-int(ChCorrC_i[ch])) / (int(ChCorrC_f[ch])-int(ChCorrC_i[ch]) +int(ChUncorrC_f[ch])-int(ChUncorrC_i[ch]) + int(ChUnerrC_f[ch])- int(ChUnerrC_i[ch])), 2)
        ChCer[ch] =  round((int(ChUncorrC_f[ch]) -int(ChUncorrC_i[ch])) / (int(ChCorrC_f[ch])-int(ChCorrC_i[ch]) +int(ChUncorrC_f[ch])-int(ChUncorrC_i[ch]) + int(ChUnerrC_f[ch])-int(ChUnerrC_i[ch])), 2)
        print(timeStamp, ",", CmMac[2:], ",",ChFreq[ch], ",", ChSnr[ch], ",", ChCcer[ch], ",",ChCer[ch])
    ChCorrC_i, ChUncorrC_i, ChUnerrC_i  = ChCorrC_f, ChUncorrC_f, ChUnerrC_f

