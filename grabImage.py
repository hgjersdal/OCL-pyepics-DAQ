import grabData, time, numpy, epics


grabImageConfig = {
    'CAM1:image1:EnableCallbacks': 1,#Enable
    'CAM1:image1:ArrayCallbacks': 1, #Enable
    'CAM1:det1:ImageMode': 0, #Get a single image
    'CAM1:det1:DataType': 1,  #UInt16, 12-bit
    'CAM1:det1:LEFTSHIFT': 0 #Disable
}

def setExposure(exposure, gain):
    grabData.caputAndCheckDict({'CAM1:det1:AcquireTime': exposure, 'CAM1:det1:Gain': gain})

def acquireImage():
    return( grabData.acquireData('CAM1:det1:', 'CAM1:image1:ArrayData') )

def printImageToScreen():
    grabData.caputAndCheckDict(grabImageConfig)
    raw = acquireImage()
    image = raw.reshape(epics.caget('CAM1:det1:SizeY_RBV'), epics.caget('CAM1:det1:SizeX_RBV'))
    import matplotlib.pyplot as plt
    plt.matshow(image)
    plt.colorbar()
    plt.show()

def imagesToHDF5(h5f, pathname, nImages):
    import h5py
    grabData.caputAndCheckDict(grabImageConfigConfig)
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

def getSmoothMax():
    #from scipy import misc
    import scipy.ndimage
    raw = acquireImage()
    image = raw.reshape(epics.caget('CAM1:det1:SizeY_RBV'), epics.caget('CAM1:det1:SizeX_RBV'))
    smoothed = scipy.ndimage.filters.median_filter(image, 9)
    import matplotlib.pyplot as plt
    plt.matshow(smoothed)
    plt.colorbar()
    plt.show()
    
    return(smoothed.max())

def autoExposure():
    grabData.caputAndCheckDict(imageToHDF5Config)

    gain = epics.caget('CAM1:det1:Gain_RBV')
    datatype = 12
    max_image = 2**datatype
    while(True):
        sm = getSmoothMax()
        exp = epics.caget('CAM1:det1:AcquireTime_RBV')
        print('Smoothed max is: ' + str(sm) + ' out of ' + str(max_image))
        autoset = exp * (max_image *  0.5)/sm
        if(autoset > 1.0):
            setExposure(1.0, gain)
            return(1.0)
        if(autoset < 0.0001):
            setExposure(0.001, gain)
            return(0.0001)
        if( (sm < max_image * 0.4) or ( sm > max_image * 0.6)):
            epics.caput('CAM1:det1:AcquireTime', autoset)
        else:
            epics.caput('CAM1:det1:AcquireTime', autoset)
            break

if __name__ == '__main__':
    setExposure(0.05,0)
    printImageToScreen()
    
#setExposure(0.01, 0)
#printImageToScreen()
#saveImageToHDF5('/tmp/', 'pytest')
