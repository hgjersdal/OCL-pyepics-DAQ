import h5py
import numpy as np
import grabData, grabImage, grabSpectrum, grabPMVal, moveStage
from misc-epics.k24xx import K24xx

samples={
    'HV1': 10000,
    'Chromox': 5000,
    'FC': 0
}

# setup sourcemeter
baud = 9600
port = '/dev/ttyUSB0'
timeout = 30 # communications timeout [s]
nplc = 10 # number of power line cycles
meanValues = 5 # number of readings to internally average
k = K24xx(baud=baud, port=port, timeout=timeout)
k.currentSetup(nplc=nplc, nMean=meanValues)

with h5py.File('/tmp/test-stage.h5', 'w-') as h5f: #set to w- to ensure no overwriting
    for sample, pos in samples.iteritems():
        group = grabData.makePathname(sample) #Store in group names after sample
        print('Sample ' + group)
        moveStage.move_to(samples['FC'])
        k.setOutout(True) # turn the sourcemeter on
        current = k.getCurrent()
        k.setOutout(False) # turn the sourcemeter off
        dsname = grabData.makePathname(sample, None, 'currentvals')

        moveStage.move_to(pos)
        attributes = { 'Sample': sample,
                       'Position': pos,
                       'BeamCurrent': current}
        grabData.setAttributes(h5f, group, attributes)
        for expval in [1,0.1,0.01,0.001]:
            grabImage.setExposure(expval, 0)
            subgroup = grabData.makePathname(group, 'images_ex' + str(expval))
            grabImage.imagesToHDF5(h5f, subgroup, 5)
        subgroup = grabData.makePathname(group, 'spectra')
        grabSpectrum.spectrumToHDF5(h5f, subgroup, 5)

