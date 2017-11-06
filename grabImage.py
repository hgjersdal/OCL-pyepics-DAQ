import grabData, time, numpy, epics

imageOnScreenConfig = {
    'CAM1:image1:EnableCallbacks': 1,#Enable
    'CAM1:image1:ArrayCallbacks': 1, #Enable
    'CAM1:det1:ImageMode': 0, #Get a single image
    'CAM1:det1:DataType': 1,  #UInt16, 12-bit
    'CAM1:det1:LEFTSHIFT': 0 #Disable
}

imageToHDF5Config = {
    'CAM1:image1:EnableCallbacks': 1,#Enable
    'CAM1:image1:ArrayCallbacks': 1, #Enable
    'CAM1:det1:ImageMode': 0, #Get a single image
    'CAM1:det1:DataType': 1,  #UInt16, 12-bit
    'CAM1:det1:LEFTSHIFT': 0, #Disable
    'CAM1:HDF1:EnableCallbacks': 1, #Enable
    'CAM1:HDF1:AutoIncrement': 1, #Enable
    'CAM1:HDF1:NumDataBits': 16, #16 bit pixels
    'CAM1:HDF1:FileWriteMode': 0, #Single
    'CAM1:HDF1:NumCapture': 1, #Capture one image
    'CAM1:HDF1:FileTemplate': '%s%s_%3.3d.h5' # path + basename + imagecounter + '.h5'
}

def getCalibration():
    

def setExposure(exposure, gain):
    grabData.caputAndCheckDict({'CAM1:det1:AcquireTime': exposure, 'CAM1:det1:Gain': gain})

def acquireImage():
    return( grabData.acquireData('CAM1:det1:', 'CAM1:image1:ArrayData') )

def printImageToScreen():
    grabData.caputAndCheckDict(imageOnScreenConfig)
    raw = acquireImage()
    image = raw.reshape(epics.caget('CAM1:det1:SizeY_RBV'), epics.caget('CAM1:det1:SizeX_RBV'))
    import matplotlib.pyplot as plt
    plt.matshow(image)
    plt.colorbar()
    plt.show()

def saveImageToHDF5(pathname, basename):
    grabData.caputAndCheckDict(imageToHDF5Config)
    grabData.caputDict({
        'CAM1:HDF1:FilePath': pathname,
        'CAM1:HDF1:FileName': basename
    })
    acquireImage()
    epics.caput('CAM1:HDF1:WriteFile', 1)
    
setExposure(0.01, 0)
printImageToScreen()
#saveImageToHDF5('/tmp/', 'pytest')
