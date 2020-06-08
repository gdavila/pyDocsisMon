# -*- coding: utf-8 -*-
"""
Created on Mon Jan 15 12:16:14 2018

@author: gdavila

This is a example to get Full Band Channel information
On Docsis 3.0 Full Band Channels is a feature that allows to get detailed info
about the power distribution of the espectrum
"""


import docsisMon.cmDevices as cmDevices
from docsisMon.snmp import SnmpError
import time
import ggplot
import sys

def asint(s):
    try: return int(s), ''
    except ValueError: return sys.maxsize, s
    
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
    

   
def main():
    try:
        myIP = '10.218.49.38'
        myCm = cmDevices.Cm(myIP)
        myCmModel = myCm.getModel()


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
        print("Modelo \t\tTiempo Espera SET/GET(s) \tTiempo de Descarga FB data(s)\t Result\t\t Nro Muestras")

        for i in range(1,2):
            data = {}
            fbc = myCm.fbc()
            fbc.turnOff()
            time.sleep(2)
            fbc.inactivityTimeout = 300
            fbc.firstFrequency = 50000000
            fbc.lastFrequency =  1000000000
            fbc.span =   10000000
            fbc.binsPerSegment = 250
            fbc.noisebandwidth = 150
            fbc.numberOfAverages = 1
            fbc.config()
            timeConfig = time.time()
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
                
            print(str(i)+" "+myCm.getModel() +'\t\t\t' + str(round(timeGet-timeConfig)) + \
                  '\t\t\t'+ str(round(timeResponse - timeGet)) + '\t\t\t'+  str(result)+'\t\t'+ str(len(format_fb_data(data)[0])))
            
        return(format_fb_data(data))  
    except SnmpError as e:
        print(e)
        result = e
 
    freq, pot= main()
    ggplot.qplot(freq[0:], pot[0:], geom="line")

