import grabData, time, numpy, epics

#Spectra
spectrumToScreenConfig = {
    'CCS1:det1:ImageMode': 0,#Single
    'CCS1:det1:TlAcquisitionType': 0, #1 is processed, set to 0 for raw
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

def spectrumToHDF5(h5f, path, nSpectra):
    import h5py
    calibrationData()
    grabData.caputAndCheckDict(spectrumToHDF5Config)
    for n in range(nSpectra):
        raw = acquireSpectrum()
        #h5f.create_dataset( path + '/spectrum' + str(n), data = raw[0])
        grabData.setDataWithTimestamp(h5f, path + '/spectrum' + str(n), raw[0])
    waves =  epics.caget('CCS1:det1:TlWavelengthData_RBV')
    grabData.setDataWithTimestamp(h5f, path + '/wavelengths', waves)
    amplitudes =  epics.caget('CCS1:det1:TlAmplitudeData_RBV')
    grabData.setDataWithTimestamp(h5f, path + '/amplitudes', amplitudes)
    grabData.setAttributes(h5f, path, 
                           {'exposure': epics.caget('CCS1:det1:AcquireTime_RBV'),
                           })

#calibrationData()
#setExposure(0.1)
#printSpectrumToScreen()
#saveSpectrumToHDF5('/tmp/', 'ccstest')
