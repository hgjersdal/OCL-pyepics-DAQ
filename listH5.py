import h5py
import numpy as np

def visitFunction(name, obj):
    print(name + ' of type ' + str(type(obj)) )
    for key, val in obj.attrs.iteritems():
        print( name + ' has attribute ' + str(key) + ': ' + str(val) )

with h5py.File('/tmp/test-file.h5','r') as f:
    f.visititems(visitFunction)

