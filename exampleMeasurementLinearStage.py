import h5py
import numpy as np
import grabData, grabImage, grabSpectrum, grabPMVal, moveStage, getCurrent

samples={
    'HV1': 10000,
    'Chromox': 5000,
    'FC': 0
}

with h5py.File('/tmp/test-stage.h5', 'w-') as h5f: #set to w- to ensure no overwriting
    for sample, pos in samples.iteritems():
        group = grabData.makePathname(sample) #Store in group names after sample
        print('Sample ' + group)
        moveStage.move_to(samples['FC'])
        current = getCurrent.getNValues(10)
        dsname = grabData.makePathname(sample, None, 'currentvals')
        grabData.setDataWithTimestamp(h5f, dsname, current)

        moveStage.move_to(pos)
        attributes = { 'Sample': sample,
                       'Position': pos,
                       'BeamCurrent': current[0]}
        grabData.setAttributes(h5f, group, attributes)
        for expval in [1,0.1,0.01,0.001]:
            grabImage.setExposure(expval, 0)
            subgroup = grabData.makePathname(group, 'images_ex' + str(expval))
            grabImage.imagesToHDF5(h5f, subgroup, 5)
        subgroup = grabData.makePathname(group, 'spectra')
        grabSpectrum.spectrumToHDF5(h5f, subgroup, 5)



