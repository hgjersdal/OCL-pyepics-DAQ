import h5py
import numpy as np
import grabData, grabImage, grabSpectrum, grabPMVal, moveStage
from misc_ess.k24xx import K24xx

# samples={
#     'Chromox': 100,
#     'HV1': 6000,
#     'FC': 6000,
#     'Yttria': 12000,
#     'HV5': 15000
# }

samples={
    'HV10': 100,
    'HV1': 6000,
    'FC': 6000,
    'HVC1.2': 12000,
    'HVC4': 15000
}


# setup sourcemeter
baud = 57600
port = '/dev/ttyUSB2'
timeout = 30 # communications timeout [s]
nplc = 10 # number of power line cycles
meanValues = 15 # number of readings to internally average
k = K24xx(baud=baud, port=port, timeout=timeout)
k.currentSetup(nplc=nplc, nMean=meanValues)

with h5py.File('/var/data/ocl/2017-11-14-OCL-currentscan2-100nA.h5', 'w') as h5f: #set to w- to ensure no overwriting
    for sample, pos in samples.iteritems():
        group = grabData.makePathname(sample) #Store in group names after sample
        print('Sample ' + group)
        moveStage.move_to(samples['FC'])
        k.setOutput(True) # turn the sourcemeter on
        current = k.getCurrent()
        k.setOutput(False) # turn the sourcemeter off
        dsname = grabData.makePathname(sample, None, 'currentvals')

        moveStage.move_to(pos)
        attributes = { 'Sample': sample,
                       'Position': pos,
                       'BeamCurrent': current}
        grabData.setAttributes(h5f, group, attributes)
        for expval in [0.0002, 0.0005, 0.001, 0.01,.1]:
            grabImage.setExposure(expval, 0)
            subgroup = grabData.makePathname(group, 'images_ex' + str(expval))
            grabImage.imagesToHDF5(h5f, subgroup, 10)
        for expval in [0.005, 0.01,0.1, 1]:
            grabSpectrum.setExposure(expval)
            subgroup = grabData.makePathname(group, 'spectrum_ex' + str(expval))
            grabSpectrum.spectrumToHDF5(h5f, subgroup, 10)
        if( sample == 'Yttria'):
            grabSpectrum.setExposure(10)
            subgroup = grabData.makePathname(group, 'spectrum_ex10')
            grabSpectrum.spectrumToHDF5(h5f, subgroup, 5)

# with h5py.File('/var/data/ocl/2017-11-14-OCL-currentscan2-300nA.h5', 'w-') as h5f: #set to w- to ensure no overwriting
#     for sample, pos in samples.iteritems():
#         group = grabData.makePathname(sample) #Store in group names after sample
#         print('Sample ' + group)
#         moveStage.move_to(samples['FC'])
#         k.setOutput(True) # turn the sourcemeter on
#         current = k.getCurrent()
#         k.setOutput(False) # turn the sourcemeter off
#         dsname = grabData.makePathname(sample, None, 'currentvals')

#         moveStage.move_to(pos)
#         attributes = { 'Sample': sample,
#                        'Position': pos,
#                        'BeamCurrent': current}
#         grabData.setAttributes(h5f, group, attributes)
#         for expval in [0.0002, 0.0005, 0.001, 0.01,.1,1.0]:
#             grabImage.setExposure(expval, 0)
#             subgroup = grabData.makePathname(group, 'images_ex' + str(expval))
#             grabImage.imagesToHDF5(h5f, subgroup, 10)
#         for expval in [0.005, 0.01,0.1, 1]:
#             grabSpectrum.setExposure(expval)
#             subgroup = grabData.makePathname(group, 'spectrum_ex' + str(expval))
#             grabSpectrum.spectrumToHDF5(h5f, subgroup, 10)
#         if( sample == 'Yttria'):
#             grabSpectrum.setExposure(10)
#             subgroup = grabData.makePathname(group, 'spectrum_ex10')
#             grabSpectrum.spectrumToHDF5(h5f, subgroup, 5)

# with h5py.File('/var/data/ocl/2017-11-14-OCL-currentscan2-600nA.h5', 'w-') as h5f: #set to w- to ensure no overwriting
#     for sample, pos in samples.iteritems():
#         group = grabData.makePathname(sample) #Store in group names after sample
#         print('Sample ' + group)
#         moveStage.move_to(samples['FC'])
#         k.setOutput(True) # turn the sourcemeter on
#         current = k.getCurrent()
#         k.setOutput(False) # turn the sourcemeter off
#         dsname = grabData.makePathname(sample, None, 'currentvals')

#         moveStage.move_to(pos)
#         attributes = { 'Sample': sample,
#                        'Position': pos,
#                        'BeamCurrent': current}
#         grabData.setAttributes(h5f, group, attributes)
#         for expval in [0.0002, 0.0005, 0.001, 0.01,.1,1.0]:
#             grabImage.setExposure(expval, 0)
#             subgroup = grabData.makePathname(group, 'images_ex' + str(expval))
#             grabImage.imagesToHDF5(h5f, subgroup, 10)
#         for expval in [0.001, 0.005, 0.01,0.1, 1]:
#             grabSpectrum.setExposure(expval)
#             subgroup = grabData.makePathname(group, 'spectrum_ex' + str(expval))
#             grabSpectrum.spectrumToHDF5(h5f, subgroup, 10)
#         if( sample == 'Yttria'):
#             grabSpectrum.setExposure(10)
#             subgroup = grabData.makePathname(group, 'spectrum_ex10')
#             grabSpectrum.spectrumToHDF5(h5f, subgroup, 5)
