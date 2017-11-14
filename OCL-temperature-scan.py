import h5py, time
import numpy as np
import grabData, grabImage, grabSpectrum, grabPMVal, moveStage, grabTemperature
from misc_ess.k24xx import K24xx

samples={#Not set!
    'HV1': 4000,
    'FC': 6000,
}



# setup sourcemeter
# baud = 57600
# port = '/dev/ttyUSB2'
# timeout = 30 # communications timeout [s]
# nplc = 10 # number of power line cycles
# meanValues = 15 # number of readings to internally average
# k = K24xx(baud=baud, port=port, timeout=timeout)
# k.currentSetup(nplc=nplc, nMean=meanValues)

with h5py.File('/var/data/ocl/2017-11-15-OCL-tempscanHV1.h5', 'w-') as h5f: #set to w- to ensure no overwriting
    temperature = grabTemperature.grabTemperature()
    while (temperature > 25):
        #Move to FC, so we are ready
        while( temperature - grabTemperature.grabTemperature() < 1 ):
            pass
        #move to heater
        temperature = grabTemperature.grabTemperature()
        print('Temperature is ' + str(temperature))
        #Do stuff
        #getCurrent
        #Add meta
        #getImages
        #getSpectra
        time.sleep(2)

