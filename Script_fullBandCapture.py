# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 12:16:14 2018

@author: gdavila
"""

import cm31Devices
import time
from snmp import SnmpError
import sys
import ggplot

def asint(s):
    try: return int(s), ''
    except ValueError: return sys.maxint, s
    
def format_fb_data(data):
    spectrum_freq = []
    spectrum_pot = []
    if data is not None:
        for key in sorted(data, key=asint):
            center_frec = int('0x'+data[key][2:10], 16)
            span = int('0x'+data[key][10:18], 16)
            samples = int('0x'+data[key][18:26], 16)
            resolution_bw = int('0x'+data[key][26:34], 16)
            offset = 42
            for i in range(0, samples):
                frec = (center_frec-span/2)+i*resolution_bw
                dec_value = int('0x'+data[key][offset+i*4:offset+i*4+4], 16)
                if dec_value > 32767:
                    value = (dec_value-65535)/100
                else:
                    value = dec_value/100
                item = [frec, round(value, 2)]
                spectrum_freq.append(item[0])
                spectrum_pot.append(item[1])
        return spectrum_freq, spectrum_pot
    else:
        return None
    

   
#'10.32.173.143', 14987d33880f, DPC3848VE' 
#'10.32.156.240', d404cdd9ff79, DCX4220
# 10.32.141.48, f46befd91120, F@ST3686 10.254.1.29 lab
#10.32.173.127, CC65.AD32.D3D7, SVG6582
#10.254.1.29 D3.1
def main():
    try:
        myIP= '10.218.49.38'
        myCm = cm31Devices.Cm31(myIP)
    
       # getting the CM Model
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
        
        
        #Gettingfull band capture information;
        print ("Full Band Capture Information:")
        for i in range(0,2):
            data = {}
            fbc = myCm.fbc()
            fbc.turnOff()
            time.sleep(2)
            fbc.inactivityTimeout = 300
            fbc.firstFrequency = 500000000
            fbc.lastFrequency =  1000000000
            fbc.span =  10000000
            fbc.binsPerSegment = 10
            fbc.noisebandwidth = 150
            fbc.numberOfAverages = 1
            fbc.config()
            timeConfig = time.time()
            #time.sleep(20)
            result = 'data OK'
            timeGet = time.time()
            data = fbc.get()
            timeResponse = time.time()

            while(data == {}):
                time.sleep(1)
                if (time.time() - timeConfig > 600): break
                timeGet = time.time()
                data = fbc.get()
                timeResponse = time.time()
                #print (timeGet, len(format_fb_data(data)))
                
            print("Model  \t\t Data ready time\tData recieved time\t Result")
            print(str(i)+" "+myCm.getModel() +'\t\t' + str(round(timeGet-timeConfig)) + '\t\t'+ str(round(timeResponse - timeGet)) + '\t\t'+  str(result))
            #print ("\nData [frequency(Hz), Power (dBmV)]: \n")
            print(len(format_fb_data(data)[0]))
        return(format_fb_data(data))  
    except SnmpError as e:
        print(e)
        result = e
 
main()
#freq, pot= main()
#ggplot.qplot(freq[18000:], pot[18000:], geom="line")
