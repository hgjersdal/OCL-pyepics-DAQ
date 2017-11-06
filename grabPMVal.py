import grabData, time, epics

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


printPMVals(100, 0.1)
