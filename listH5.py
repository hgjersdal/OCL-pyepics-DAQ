import h5py
import sys
import numpy as np

def visitFunction(name, obj):
    print(name)
    for key, val in obj.attrs.iteritems():
        print( '    ' + str(key) + ': ' + str(val) )
    if(type(obj) == h5py._hl.dataset.Dataset):
        if(obj.len() > 100000):
            print('I hope this is an image!')
            raw = obj[:].reshape(964, 1292)
            import matplotlib.pyplot as plt
            plt.matshow(raw)
            plt.colorbar()
            plt.show()        
        if(obj.len() < 100000 and obj.len()>3599):
            print('I hope this is a spectrum!')
            raw = obj[:]
            import matplotlib.pyplot as plt
            plt.plot(raw[0:3600])
            plt.show()        
        if(obj.len() < 3599):
            print('Power or current scan?')
            raw = obj[:]
            import matplotlib.pyplot as plt
            plt.plot(raw)
            plt.show()        

    
#x = 1292, y = 964

if( len(sys.argv)!= 2 ):
    print("Call program with one argument, the hdf5 file")

with h5py.File(sys.argv[1],'r') as f:
    f.visititems(visitFunction)
