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

def acquireData(baseString, dataString):
    caputDict({ baseString + 'Acquire': 1})
    time.sleep(0.1)
    while (epics.caget( baseString + 'DetectorState_RBV' ) != 0):
        time.sleep(0.1)
    return(epics.caget( dataString ))

def setAttributes(h5f, pathname, attributes):
    import h5py
    group = h5f.require_group(pathname)
    for key,value in attributes.iteritems():
        group.attrs[key] = value
    
def setDataWithTimestamp(h5f, pathname, data):
    ds = h5f.create_dataset( pathname, data = data)
    ds.attrs['timestamp'] = time.time()

def makePathname(group, subgroup=None, dataset=None):
    pn = group
    if(not pn.startswith('/')):
         pn = '/' + pn
    if(subgroup):
       pn = pn + '/' + subgroup
    if(dataset):
        pn = pn + '/' + dataset
    return(pn)
