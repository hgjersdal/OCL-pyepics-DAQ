import grabData, time, numpy, epics

def grabTemperature():
    epics.caput('LT59:Retrieve', 1)
    time.sleep(0.1)
    return(epics.caget('LT59:Temp1_RBV'))


if __name__ == '__main__':
    while(True):
        print(grabTemperature())
