import h5py
import numpy as np
import grabData, grabImage, grabSpectrum, grabPMVal, getCurrent

with h5py.File('/tmp/test-file.h5', 'w') as h5f: #set to w- to ensure no overwriting
    group = grabData.makePathname('meas1')
    current = getCurrent.getNValues(10)
    attributes = { 'BeamCurrent': current[0], #nA
                   'Temperature': 150, #degrees C
                   'Sample': 'HV1'
               }
    grabData.setDataWithTimestamp(h5f, '/meas1/currentVals', current)
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
