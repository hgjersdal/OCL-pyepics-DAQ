import h5py
import sys
import numpy as np
import matplotlib.pyplot as plt

def visitFunction(name, obj, plotp, match):
    print(name)
    for key, val in obj.attrs.items():
        print( '    ' + str(key) + ': ' + str(val) )
    matching = True
    if( isinstance(match, str) and 
        name.find(match) == -1):
        matching = False
    if(type(obj) == h5py._hl.dataset.Dataset  and
       matching and 
       plotp):
        if(obj.len() > 100000):
            raw = obj[:].reshape(964, 1292)
            plt.matshow(raw)
            plt.colorbar()
            plt.show()        
        if(obj.len() < 100000 and obj.len()>3599):
            raw = obj[:]
            plt.plot(raw[0:3600])
            plt.show()        
        if(obj.len() < 3599):
            raw = obj[:]
            plt.plot(raw)
            plt.show()        

import argparse

parser = argparse.ArgumentParser(description='List contents of HDF5 file. ')
parser.add_argument('filename')
parser.add_argument('-p','--plot', action='store_true', default=False, help="Plot data")
parser.add_argument('-m','--match', default=None, help="Print things where the full pathname contains MATCH")
args = parser.parse_args()

if(args.match):
    args.plot = True

with h5py.File(args.filename,'r') as f:
    f.visititems(lambda obj, name: visitFunction(obj, name, args.plot, args.match))
