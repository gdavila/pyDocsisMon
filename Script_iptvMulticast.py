# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:30:59 2018

@author: gdavila
"""
import cmDevices
import time
from snmp import SnmpError




# definitions 
myIP= '10.254.1.33'
interval = 10 #seconds
duration = 1200 #seconds


# create CM
myCm = cmDevices.Cm(myIP)


# Getting Basic Values
CmModel = myCm.getModel()
CmFw = myCm.getSw_rev()
CmDocIf = myCm.DocsIf()
ChId = CmDocIf.getChId()
Freq = CmDocIf.getChFreq()
CmMac = CmDocIf.getMac()
Snr = CmDocIf.getDownSnr()



CorrC_i, UncorrC_i, UnerrC_i  = CmDocIf.updateCorrCodewords(), CmDocIf.updateUncorrCodewords(), CmDocIf.updateUnerrCodewords()

OctetsIn_i= myCm.getInOctets()
timeStamp_i = time.time()
start = time.time()

Ccer = {}
Cer = {}
print("timeStamp,", "MAC,", "FREQ [MHz], ", "SNR [dB], ", "CCER [%], ", "CER [%], ", "Bandwidth [Mbps]")
while (time.time()-start < duration):
    time.sleep(interval)
    timeStamp = time.time() -start
    CorrC_f, UncorrC_f, UnerrC_f = CmDocIf.updateCorrCodewords(), CmDocIf.updateUncorrCodewords(), CmDocIf.updateUnerrCodewords()
    OctetsIn_f= myCm.getInOctets()
    timeStamp_f = time.time()
    ChSnr = CmDocIf.updateDownSnr()
    bandwidth_Mbps = round(((int(OctetsIn_f) - int(OctetsIn_i)) /(timeStamp_f-timeStamp_i))*8/1E6,2)
    for ch in Snr.keys():
        try:
            Ccer[ch] = round((int(CorrC_f[ch])-int(CorrC_i[ch])) / (int(CorrC_f[ch])-int(CorrC_i[ch]) +int(UncorrC_f[ch])-int(UncorrC_i[ch]) + int(UnerrC_f[ch])- int(UnerrC_i[ch])), 2)
            Cer[ch] =  round((int(UncorrC_f[ch]) -int(UncorrC_i[ch])) / (int(CorrC_f[ch])-int(CorrC_i[ch]) +int(UncorrC_f[ch])-int(UncorrC_i[ch]) + int(UnerrC_f[ch])-int(UnerrC_i[ch])), 2)
        except ZeroDivisionError :
            Ccer[ch] = "PS"
            Cer[ch] = "PS"
        print(timeStamp, ",", CmMac[2:], ",",round(int(Freq[ch])/1E6,2), ",", round(int(Snr[ch])/10,2), ",", Ccer[ch], ",",Cer[ch],"," ,bandwidth_Mbps)
    CorrC_i, UncorrC_i, UnerrC_i  = CorrC_f, UncorrC_f, UnerrC_f
    OctetsIn_i=OctetsIn_f
    timeStamp_i=timeStamp_f

