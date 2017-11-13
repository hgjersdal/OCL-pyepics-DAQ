import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reads current from keithley 24xx sourcemeter.')
    parser.add_argument('-p','--pos', action='store_true', default=False, help="Print position")
    parser.add_argument('-m','--move', type=int, help="Move stage to position")
    args = parser.parse_args()

    if( args.pos ): 
        print('Position is office')
        sys.exit(0)
        
    pos = args.move
    print ('Move to ' + str(pos) )
    sys.exit(0)
