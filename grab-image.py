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

imageOnScreenConfig = {
    'CAM1:image1:EnableCallbacks': 1,#Enable
    'CAM1:image1:ArrayCallbacks': 1, #Enable
    'CAM1:det1:ImageMode': 0, #Get a single image
    'CAM1:det1:DataType': 1  #UInt16, 12-bit
}

imageToHDF5Config = {
    'CAM1:image1:EnableCallbacks': 1,#Enable
    'CAM1:image1:ArrayCallbacks': 1, #Enable
    'CAM1:det1:ImageMode': 0, #Get a single image
    'CAM1:det1:DataType': 1,  #UInt16, 12-bit
    'CAM1:HDF1:EnableCallbacks': 1, #Enable
    'CAM1:HDF1:AutoIncrement': 1, #Enable
    'CAM1:HDF1:NumDataBits': 16, #16 bit pixels
    'CAM1:HDF1:FileWriteMode': 0, #Single
    'CAM1:HDF1:NumCapture': 1, #Capture one image
}



def caputDict(dict):
    for key, value in dict.iteritems():
        epics.caput(key, value)
        
def caputAndCheckDict(dict):
    caputDict(dict)
    time.sleep(1)
    for key, value in dict.iteritems():
        rbv = epics.caget(key + '_RBV')
        if( rbv != value):
            warnings.warn( key + " is set to " + str(value) + ", but RBV is " + str(rbv))

def setExposure(exposure, gain):
    caputAndCheckDict({'CAM1:det1:AcquireTime': exposure, 'CAM1:det1:Gain': gain})

def acquireImage():
    caputDict({'CAM1:det1:Acquire': 1})
    time.sleep(0.1)
    while (epics.caget('CAM1:det1:DetectorState_RBV') != 0):
        time.sleep(0.1)
    return( epics.caget('CAM1:image1:ArrayData').astype(numpy.uint16))

def printImageToScreen():
    caputAndCheckDict(imageOnScreenConfig)
    setExposure(0.03, 0)
    raw = acquireImage()
    print(str(min(raw)) + ", " + str(max(raw)))
    image = raw.reshape(epics.caget('CAM1:det1:SizeY_RBV'), epics.caget('CAM1:det1:SizeX_RBV'))
    import matplotlib.pyplot as plt
    plt.matshow(image)
    plt.colorbar()
    plt.show()

def saveImageToHDF5(pathname, basename):
    caputAndCheckDict(imageToHDF5Config)
    epics.caput('CAM1:HDF1:FilePath', pathname)
    epics.caput('CAM1:HDF1:FileName', basename)
    epics.caput('CAM1:HDF1:FileTemplate', '%s%s_%3.3d.h5')
    acquireImage()
    epics.caput('CAM1:HDF1:WriteFile', 1)
    

#printImageToScreen()
saveImageToHDF5('/tmp/', 'pytest')
