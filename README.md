# pyDocsisMon

Python Docsis Monitorinh

# Summary

PyDocsisMon is a very draft library/tool to work in estraightfoward maner with Docsis atribbutes. 

This tool allows to define:

* Cable Modem Termination System (CMTS)
* Cable Modem (CM)
* Docsis Set Top Boxes (STB)

pyDocsisMon uses a SNMPv2 interfaces to get information about each Docsis Object. It is just needed
to add your snmp credentials (communities) at private.py file.

Some examples about how to use this tool could be found in test.py

A lot of features need to be added and  clasess definition should be reviewed in order to clean the object oriented implementation of the library.