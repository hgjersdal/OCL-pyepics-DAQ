import grabData, time, epics

def setWavelength(wavelengthInNm):
    epics.caput('PM100:SENS:CORR:WAV', wavelengthInNm)
    time.sleep(0.1)
    epics.caput('PM100:SENS:CORR:WAV_RBV.PROC', 1)
    time.sleep(0.1)
    if(wavelengthInNm != epics.caget('PM100:SENS:CORR:WAV_RBV') ):
        warnings.warn('PM is set to ' + str(wavelengthInNm) + ', but read back as ' + str(epics.caget('PM100:SENS:CORR:WAV_RBV')))

def getPMVals(nValues, sleepTime):
    print('This will take >' + str(nValues * sleepTime) + ' seconds' )
    PMVals = []
    for t in range(nValues):
    	epics.caput('PM100:MEAS:POW.PROC', 1)
	time.sleep(sleepTime)
    	PMVals.append( epics.caget('PM100:MEAS:POW'))
    return(PMVals)

def printPMVals(nValues, sleepTime):
    PMVals = getPMVals(nValues, sleepTime)
    import matplotlib.pyplot as plt
    plt.plot(PMVals)
    plt.show()

setWavelength(500)
printPMVals(100, 0.1)
