import h5py, time, math
import numpy as np
import grabData, grabImage, grabSpectrum, grabPMVal, moveStage, grabTemperature
from misc_ess.k24xx import K24xx

# setup sourcemeter
baud = 57600
port = '/dev/ttyUSB0'
timeout = 30 # communications timeout [s]
nplc = 10 # number of power line cycles
meanValues = 15 # number of readings to internally average
k = K24xx(baud=baud, port=port, timeout=timeout)
k.currentSetup(nplc=nplc, nMean=meanValues)

with h5py.File('/var/data/ocl/2017-11-15-OCL-tempscanHV1.h5', 'w') as h5f: #set to w- to ensure no overwriting
    temperature = grabTemperature.grabTemperature()
    temperature += 2.0 #Make sure we get the first reading immediately
    sample = 'HV1'
    while (temperature > 25):
        #Move to FC, so we are ready
        while( temperature - grabTemperature.grabTemperature() < 1 ):
            pass

        temperature = grabTemperature.grabTemperature()
        print('Temperature is ' + str(temperature))
        group = grabData.makePathname(str(sample) + 'temp' + str(math.floor(temperature))) #Store in group names after sample

        #Get Current
        k.setOutput(True) # turn the sourcemeter on
        current = k.getCurrent()
        k.setOutput(False) # turn the sourcemeter off
        #print('WE HAVE NO CURRENT MEASUREMENT!')
        #current = 100
        #Add meta
        grabData.setAttributes(h5f, group,
                               { 'Sample': sample,
                                 'Position': 5000,
                                 'CameraDistance': 1170,
                                 'BeamCurrent': current})
        
        #getImages NO IMAGES DUE TO CAMERA FAILURE
        #subgroup = grabData.makePathname(group, 'images') #Store in group names after sample    
        #grabImage.imagesToHDF5(h5f, subgroup, 10)
        #getSpectra
        subgroup = grabData.makePathname(group, 'spectum')
        grabSpectrum.spectrumToHDF5(h5f, subgroup, 10)
        
