import sys
import getopt
import datetime


def main(argv):
    t4312Encoding = {
        "000": 600,
        "001": 3600,
        "010": 36000,
        "011": 2,
        "100": 30,
        "101": 60,
        "110": 1152000,
        "111": 0
    }

    t3324Encoding = {
        "000": 2,
        "001": 60,
        "010": 3600,
        "111": 0
    }

    try:
        opts, args = getopt.getopt(argv,'ta:p:')
    except getopt.GetoptError:
      print('--- wrong input - exiting ---')
      sys.exit(2)
    
    for opt, arg in opts: 
        if opt == '-a':
            multiple = t3324Encoding.get(arg[0:3],-1)
            if(multiple == -1):
                print('--- Invalid t3324 value ---')
                print(arg[0:3])
                sys.exit(2)

            time = multiple*int(arg[3:8],2)
            print("--- Active time ---")
            print(datetime.timedelta(seconds=time))
        elif opt == '-p':
            multiple = t4312Encoding.get(arg[0:3],-1)
            if(multiple == -1):
                print('--- Invalid t4312 value ---')
                print(arg[0:3])
                sys.exit(2)

            time = multiple*int(arg[3:8],2)

            print("--- Periodic TAU ---")
            print(datetime.timedelta(seconds=time))
        else:
            print("Invalid argument")

if __name__ == "__main__":
   main(sys.argv[1:])