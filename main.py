import sys, getopt
from controllers.SSIDesignAnalyzer import SSIDesignAnalyzer
from controllers.CWEWeaknessAnalyzer import CWEWeaknessAnalyzer

def main(argv):
    # Command line argument read
    input, interm, cwm = input_args(argv)
    
    # Controller initiations
    sda = SSIDesignAnalyzer(input, interm)
    cwa = CWEWeaknessAnalyzer(cwm)


    # Process the TEWAF-SSI procedure
    updatedSM = sda.analyze_meaning()
    cwe_list = cwa.read_file()


def input_args(argv):
    inputfile = ''
    intermediatefile = ''
    cwmfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:n:c:",["ifile=","intfile=","cwmfile="])
    except getopt.GetoptError:
        print('python main.py -i <inputfile> -n <intermediatefile> -c <cwmfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -n <intermediatefile> -c <cwmfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-n", "--intfile"):
            intermediatefile = arg
        elif opt in ("-c", "--cwmfile"):
            cwmfile = arg
        print(opt, arg)

    return inputfile, intermediatefile, cwmfile


if __name__ == '__main__':
    main(sys.argv[1:])