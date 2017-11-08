import h5py
import numpy as np
import grabData, grabImage, grabSpectrum, grabPMVal

with h5py.File('/tmp/test-file.h5', 'w') as h5f: #set to w- to ensure no overwriting
    path = '/meas1'
    attributes = { 'BeamCurrent': 100, #nA
                   'Temperature': 150, #degrees C
                   'Sample': 'HV1'
               }
    grabData.setAttributes(h5f, path, attributes)
    grabImage.imagesToHDF5(h5f, path + '/images', 5)
    grabSpectrum.spectrumToHDF5(h5f, path + '/spectra', 5)
    grabPMVal.pmValsToHDF5(h5f, path + '/PMVals', 100, 0.1)

#samples={
#     'HV1': 1001,
#     'Chromox': 1234,
#     'FC': 2345
# }
# # What a sample scan might look like
# with h5py.File('/tmp/test-file.h5', 'w-') as h5f: #set to w- to ensure no overwriting
#     for key, value in samples:
#         path = '/' + key
#         moveStage(samples['FC'])
#         attributes = { 'Sample': key,
#                        'BeamCurrent': getCurrent(),
#                    }
#         moveStage(value)
#         grabData.setAttributes(attributes)
#         grabImage.imagesToHDF5(h5f, path + '/images', 5)
#         grabSpectrum.spectrumToHDF5(h5f, path + '/spectra', 5)


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
