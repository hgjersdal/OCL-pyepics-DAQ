import h5py
import numpy as np
import grabData, grabImage, grabSpectrum, grabPMVal
from misc_ess.k24xx import K24xx

# setup sourcemeter
baud = 9600
port = '/dev/ttyUSB1'
timeout = 30 # communications timeout [s]
nplc = 10 # number of power line cycles
meanValues = 5 # number of readings to internally average
k = K24xx(baud=baud, port=port, timeout=timeout)
k.currentSetup(nplc=nplc, nMean=meanValues)

with h5py.File('/tmp/test-file.h5', 'w') as h5f: #set to w- to ensure no overwriting
    group = grabData.makePathname('meas1')
    k.setOutput(True)
    current = k.getCurrent()
    k.setOutput(False)
    attributes = { 'BeamCurrent': current, #in amps
                   'Temperature': 150, #degrees C
                   'Sample': 'HV1'
               }
    grabData.setAttributes(h5f, group, attributes)
    grabImage.imagesToHDF5(h5f, '/meas1/images', 5)
    grabSpectrum.spectrumToHDF5(h5f, '/meas1/spectra', 5)
    #grabPMVal.pmValsToHDF5(h5f, '/meas1/PMVals', 100, 0.1)

# #What a heat scan might look like
# with h5py.File('/tmp/test-file.h5', 'w-') as h5f: #set to w- to ensure no overwriting
#     temp = getTemp()
#     while(temp > 25):
#         moveStage(samples['FC'])
#         current = getCurrent()
#         moveStage(samplesp['HV1'])
#         temp = getTemp()
#         path = '/temp' + math.floor(temp) 
#         attributes = { 'Sample': key,
#                        'BeamCurrent': current,
#                        'temp': temp
#                    }
#         grabData.setAttributes(attributes)
#         grabImage.imagesToHDF5(h5f, path + '/images', 5)
#         grabSpectrum.spectrumToHDF5(h5f, path + '/spectra', 5)
#         while( temp > getTemp() + 2.0):
#             sleep(0.5)
