# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 12:16:14 2018

@author: gdavila
"""

import cmDevices
import time
from snmp import SnmpError
import sys


def asint(s):
    try: return int(s), ''
    except ValueError: return sys.maxint, s
    
def format_fb_data(data):
    spectrum = []
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
                spectrum.append(item)
        return spectrum
    else:
        return None
    
    
#'10.32.173.143', 14987d33880f, DPC3848VE' 
#'10.32.156.240', d404cdd9ff79, DCX4220
# 10.32.141.48, f46befd91120, F@ST3686
#10.32.173.127, CC65.AD32.D3D7, SVG6582

def main():
    try:
        myIP= '10.27.26.242'
        myCm = cmDevices.Cm(myIP)
    
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
        for i in range(1,10):
            data = {}
            fbc = myCm.fbc()
            fbc.turnOff()
            time.sleep(2)
            fbc.inactivityTimeout = 300
            fbc.firstFrequency = 50000000
            fbc.lastFrequency =  1000000000
            fbc.span =  10000000
            fbc.binsPerSegment = 250
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
            print (len(format_fb_data(data)))
    
    except SnmpError as e:
        result = e
    

    
main()
