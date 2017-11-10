from ctypes import *
import argparse
import time
import os
import sys
import tempfile
import re
if sys.version_info >= (3,0):
    import urllib.parse
try:
    from pyximc import *
except ImportError as err:    
    print ("Can't import pyximc module. The most probable reason is that you haven't copied pyximc.py to the working directory. See developers' documentation for details.")
    exit()
except OSError as err:
    print ("Can't load libximc library. Please add all shared libraries to the appropriate places (next to pyximc.py on Windows). It is decribed in detail in developers' documentation. On Linux make sure you installed libximc-dev package.")
    exit()

open_name = 'xi-com:///dev/ximc/00001A4C'
open_name = open_name.encode()

def home():
    device_id = lib.open_device(open_name)
    result = lib.command_left(device_id)
    result = lib.command_wait_for_stop(device_id, 10)
    glob_position = 0
    
def get_position():
    device_id = lib.open_device(open_name)
    x_pos = get_position_t()
    result = lib.get_position(device_id, byref(x_pos))
    if result != Result.Ok:
        print("Result: " + repr(result))
    lib.close_device(byref(cast(device_id, POINTER(c_int))))
    return(x_pos.Position)

def move_to (position):
    current_pos = get_position()
    time.sleep(1)
    device_id = lib.open_device(open_name)
    distance = position - current_pos
    print("Moving from " + str(current_pos) + ' to ' + str(position))
    result = lib.command_movr(device_id, distance, 0)
    result = lib.command_wait_for_stop(device_id, 10)
    lib.close_device(byref(cast(device_id, POINTER(c_int))))
    print('Now at ' + str(get_position()) )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check or set position of Standa stage')
    parser.add_argument('-p','--pos', action='store_true', default=False, help="Print position")
    parser.add_argument('-m','--move', type=int, help="Move stage to position")
    args = parser.parse_args()

    if( args.pos ): 
        print('Position is office')
        sys.exit(0)
        
    pos = args.move
    move_to(pos)
    sys.exit(0)
