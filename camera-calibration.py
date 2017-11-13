import h5py
import numpy as np
import grabData, grabImage, grabSpectrum, grabPMVal, getCurrent

with h5py.File('/home/dev/data/lab/2017-11-13-camera-calib.h5', 'w') as h5f: #set to w- to ensure no overwriting
    group = grabData.makePathname('meas1')
    attributes = { 'Sample': 'M660L4',
                   'CurrLim': 0.2,
                   'pow': 'l0'
               }
    grabImage.setExposure(0.00001,0)
    grabData.setAttributes(h5f, group, attributes)
    grabImage.imagesToHDF5(h5f, '/meas1/images', 10)
    #grabPMVal.pmValsToHDF5(h5f, '/meas1/PMVals', 100, 0.1)
