# Fix "cannot find Epics CA DLL"
import os
os.environ["PYEPICS_LIBCA"] = "/home/dev/git/ng3e/root/R3.15.4/base/lib/linux-x86_64/libca.so"

import epics, time, numpy, warnings, sys

# Supress CA warnings. Currently it is spamming due to "Identical process variable names on multiple servers"
supressEpicsWarings = True
if(supressEpicsWarings):
    def handleMessages(text):
        None
    epics.ca.replace_printf_handler(handleMessages)

def caputDict(dict):
    for key, value in dict.iteritems():
        epics.caput(key, value)
        
def caputAndCheckDict(dict):
    caputDict(dict)
    time.sleep(1)
    for key, value in dict.iteritems():
        rbv = epics.caget(key + '_RBV')
        if( (type(rbv) != numpy.ndarray ) and (rbv != value) ):
            warnings.warn( key + " is set to " + str(value) + ", but RBV is " + str(rbv))

