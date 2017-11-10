import grabData, time, numpy, epics

imageOnScreenConfig = {
    'CAM1:image1:EnableCallbacks': 1,#Enable
    'CAM1:image1:ArrayCallbacks': 1, #Enable
    'CAM1:det1:ImageMode': 0, #Get a single image
    'CAM1:det1:DataType': 1,  #UInt16, 12-bit
    'CAM1:det1:LEFTSHIFT': 0 #Disable
}

imageToHDF5Config = {
    'CAM1:HDF1:EnableCallbacks': 1, #Enable
    'CAM1:HDF1:AutoIncrement': 1, #Enable
    'CAM1:HDF1:NumDataBits': 16, #16 bit pixels
    'CAM1:HDF1:FileWriteMode': 0, #Single
    'CAM1:HDF1:NumCapture': 1, #Capture one image
    'CAM1:HDF1:FileTemplate': '%s%s_%3.3d.h5' # path + basename + imagecounter + '.h5'
}

imageToHDF5Config = dict( imageOnScreenConfig.items() + imageToHDF5Config.items() )

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

def imagesToHDF5(h5f, pathname, nImages):
    import h5py
    grabData.caputAndCheckDict(imageToHDF5Config)
    for n in range(nImages):
        raw = acquireImage()
        pname = grabData.makePathname(pathname, None, 'image' + str(n))
        grabData.setDataWithTimestamp(h5f, pname, raw)
    #Write exposure settings to subgroup
    grabData.setAttributes(h5f,
                           pathname,
                           {'exposure': epics.caget('CAM1:det1:AcquireTime_RBV'),
                            'gain': epics.caget('CAM1:det1:Gain_RBV'),
                            'sizeX': epics.caget('CAM1:det1:SizeX_RBV'),
                            'sizeY': epics.caget('CAM1:det1:SizeY_RBV')})
    

#setExposure(0.01, 0)
#printImageToScreen()
#saveImageToHDF5('/tmp/', 'pytest')
