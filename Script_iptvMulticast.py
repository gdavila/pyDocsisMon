# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 16:30:59 2018

@author: gdavila

This is a very basic example that allows to monitor the Docsis Health of a CM
within a time window. The script request some information to the CM periodically.  
"""
import docsisMon.cmDevices as cmDevices
import time
from docsisMon.snmp import SnmpError



# 1 Setup 
myIP= '10.254.1.46' # CM IP address you want to monitor
fileName = "multicast.log" # Filename to save your results
interval = 10 # monitoring interval (seconds) to do SNMP request to the CM
duration = 10*60*60 # Total last of the monitoring


# 2 create the  CM device
myCm = cmDevices.Cm(myIP)


# 3 Getting some  Basic Values to monitor
CmModel = myCm.getModel() # Model
CmFw = myCm.getSw_rev() # Software version
CmDocIf = myCm.DocsIf() # Docsis Iface Object
ChId = CmDocIf.getChId() # ids of the Docsis channels
Freq = CmDocIf.getChFreq() # Frecuencies of the Docsis channels
CmMac = CmDocIf.getMac() # Mac Address of the Docsis Iface
Snr = CmDocIf.getDownSnr() # SNR of the Downstream channles
#Corrected Codewords, Uncorrected Codewords, Unerrored Codewords
CorrC_i, UncorrC_i, UnerrC_i  = CmDocIf.updateCorrCodewords(), CmDocIf.updateUncorrCodewords(), CmDocIf.updateUnerrCodewords()
#Amount of octects received by the CM 
OctetsIn_i= myCm.getInOctets()
timeStamp_i = time.time()
start = time.time()

Ccer = {}
Cer = {}
print("timeStamp,", "MAC,", "FREQ [MHz], ", "SNR [dB], ", "CCER [%], ", "CER [%], ", "Bandwidth [Mbps]")
with open(fileName, 'w') as file:
    file.write("timeStamp, MAC, FREQ [MHz], SNR [dB], CCER , CER, Bandwidth [Mbps]")
    
while (time.time()-start < duration):
    time.sleep(interval)
    timeStamp = time.time() -start
    try:
        CorrC_f, UncorrC_f, UnerrC_f = CmDocIf.updateCorrCodewords(), CmDocIf.updateUncorrCodewords(), CmDocIf.updateUnerrCodewords()
        OctetsIn_f= myCm.getInOctets()
        timeStamp_f = time.time()
        Snr = CmDocIf.updateDownSnr()
    except SnmpError:
        continue
    bandwidth_Mbps = round(((int(OctetsIn_f) - int(OctetsIn_i)) /(timeStamp_f-timeStamp_i))*8/1E6,2)
    for ch in Snr.keys():
        try:
            Ccer[ch] = round(100*(int(CorrC_f[ch])-int(CorrC_i[ch])) / (int(CorrC_f[ch])-int(CorrC_i[ch]) +int(UncorrC_f[ch])-int(UncorrC_i[ch]) + int(UnerrC_f[ch])- int(UnerrC_i[ch])), 2)
            Cer[ch] =  round(100*(int(UncorrC_f[ch]) -int(UncorrC_i[ch])) / (int(CorrC_f[ch])-int(CorrC_i[ch]) +int(UncorrC_f[ch])-int(UncorrC_i[ch]) + int(UnerrC_f[ch])-int(UnerrC_i[ch])), 4)
        except ZeroDivisionError :
            Ccer[ch] = "PS"
            Cer[ch] = "PS"
        print(timeStamp, ",", CmMac[2:], ",",round(int(Freq[ch])/1E6,2), ",", round(int(Snr[ch])/10,2), ",", Ccer[ch], ",",Cer[ch],"," ,bandwidth_Mbps)
        with open(fileName, 'a') as file:
            file.write("\n"+str(timeStamp)+ ","+ str(CmMac[2:]) + ","+ str(round(int(Freq[ch])/1E6,2)) + "," +str( round(int(Snr[ch])/10,2)) + "," + str( Ccer[ch])+ ","+str(Cer[ch]) +"," +str(bandwidth_Mbps))
    CorrC_i, UncorrC_i, UnerrC_i  = CorrC_f, UncorrC_f, UnerrC_f
    OctetsIn_i=OctetsIn_f
    timeStamp_i=timeStamp_f

