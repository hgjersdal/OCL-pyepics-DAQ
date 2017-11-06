import grabData, time, numpy, epics

#Spectra
spectrumToScreenConfig = {
    'CCS1:det1:ImageMode': 0,#Single
    'CCS1:det1:TlAcquisitionType': 1, #Processed, set to 0 for raw
    'CCS1:det1:TriggerMode': 0, #Internal
    'CCS1:trace1:EnableCallbacks': 1, #Enable
    'CCS1:trace1:ArrayCallbacks': 1, #Enable
    'CCS1:det1:TlAmplitudeDataTarget': 2, #Thorlabs
    'CCS1:det1:TlWavelengthDataTarget': 1, #Factory
}

spectrumToHDF5Config =  {
    'CCS1:HDF1:EnableCallbacks': 1, #Enable
    'CCS1:HDF1:AutoIncrement': 1, #Enable
    'CCS1:HDF1:FileWriteMode': 0, #Single
    'CCS1:HDF1:NumCapture': 1, #Capture one image
    'CCS1:HDF1:FileTemplate': '%s%s_%3.3d.h5' # path + basename + imagecounter + '.h5'
}


spectrumToHDF5Config = dict( spectrumToScreenConfig.items() + spectrumToHDF5Config.items() )

def calibrationData():
    """ Get calibration data """
    grabData.caputDict({
        'CCS1:det1:TlAmplitudeDataGet': 1,
        'CCS1:det1:TlWavelengthDataGet': 1
    })
    time.sleep(1)

def setExposure(exposure):
    """ Set integration time to 'exposure' """
    grabData.caputAndCheckDict({'CCS1:det1:AcquireTime': exposure})

def acquireSpectrum():
    """ Get a spectrum, return it together with the corresponding wavelength array"""
    return( grabData.acquireData('CCS1:det1:', 'CCS1:trace1:ArrayData'), 
            epics.caget('CCS1:det1:TlWavelengthData_RBV') )

def printSpectrumToScreen():
    """ Plot a spectrum """
    grabData.caputAndCheckDict(spectrumToScreen)
    amplitudes, waves = acquireSpectrum()
    shortLength = min( amplitudes.size, waves.size)
    import matplotlib.pyplot as plt
    plt.plot(waves[0:shortLength], amplitudes[0:shortLength])
    plt.show()

def saveSpectrumToHDF5(pathname, basename):
    grabData.caputAndCheckDict(spectrumToHDF5Config)
    grabData.caputDict({
        'CCS1:HDF1:FilePath': pathname,
        'CCS1:HDF1:FileName': basename
    })
    acquireSpectrum()
    epics.caput('CCS1:HDF1:WriteFile', 1)


calibrationData()
setExposure(0.1)
#printSpectrumToScreen()
saveSpectrumToHDF5('/tmp/', 'ccstest')
