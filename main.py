import sys, getopt
import json
import time
from controllers.SSIDesignAnalyzer import SSIDesignAnalyzer
from controllers.CWEWeaknessAnalyzer import CWEWeaknessAnalyzer
from controllers.PotentialWeaknessAnalyzer import PotentialWeaknessAnalyzer
from datetime import datetime


def main(argv):
    # Command line argument read
    input, interm, cwm, tnw, noedge = input_args(argv)
    
    # Controller initiations
    sda = SSIDesignAnalyzer(input, interm)
    cwa = CWEWeaknessAnalyzer(cwm)
    pwa = PotentialWeaknessAnalyzer(noedge)


    # Process the TEWAF-SSI procedure
    updatedSM, interm = sda.analyze_meaning()
    cwe_list = cwa.read_file()
    potentialWN = pwa.analyze_la(updatedSM, cwe_list, tnw)
    print("\n...{} potential weaknesses are found.\n".format(len(potentialWN)))
    prepare_result(potentialWN, input)
    
    # dump evolutionary knowledge
    print("Prepare to save an SSI text network's file successfully: {} nodes and {} edges are prepared.\n".format(len(pwa.tnw["SSI.TextNetwork"]["node"]),len(pwa.tnw["SSI.TextNetwork"]["edge"])))
    dump_json_to_file(pwa.tnw, "./intermediate files/int-network-updated.json")
    print("Prepare to save an SSI general notion's file successfully: {} notions are prepared.\n".format(len(interm["SSI.notions"])))
    dump_json_to_file(interm, "./intermediate files/int-notions-updated.json")
    dump_json_to_file(pwa.no_edge, "./intermediate files/int-noedge.json")

def input_args(argv):
    inputfile = ''
    intermediatefile = ''
    cwmfile = ''
    tnwfile = ''
    noedgefile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:n:c:t:e:",["ifile=","intfile=","cwmfile=","tnwfile="])
    except getopt.GetoptError:
        print('python main.py -i <inputfile> -n <intermediatefile> -c <cwmfile> -t <tnwfile> -e <noedgefile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -n <intermediatefile> -c <cwmfile> -t <tnwfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-n", "--intfile"):
            intermediatefile = arg
        elif opt in ("-c", "--cwmfile"):
            cwmfile = arg
        elif opt in ("-t", "--tnwfile"):
            tnwfile = arg
        elif opt in ("-e", "--noedgefile"):
            noedgefile = arg
        print(opt, arg)

    return inputfile, intermediatefile, cwmfile, tnwfile, noedgefile

def prepare_result(potentialWN, infile):
    la_count_list = []
    output = {}
    output["potential weakness"] = list()
    for pw in potentialWN:
        out = {}
        out["SSI systemic meaning"] = {}
        out["SSI systemic meaning"]["id"] = pw.CorrespondingSSM.id
        out["SSI systemic meaning"]["subject"] = pw.CorrespondingSSM.subject
        out["SSI systemic meaning"]["operation"] = pw.CorrespondingSSM.operation
        out["SSI systemic meaning"]["data"] = pw.CorrespondingSSM.data
        out["CWE weakness meaning"] = {}
        out["CWE weakness meaning"]["id"] = pw.CorrespondingCWM.id
        out["CWE weakness meaning"]["system component"] = pw.CorrespondingCWM.systemComponent
        out["CWE weakness meaning"]["system function"] = pw.CorrespondingCWM.systemFunction
        out["CWE weakness meaning"]["system object"] = pw.CorrespondingCWM.systemObject
        out["linguistic association"] = []
        countLA = 0
        for la in pw.CorrespondingLA:
            countLA += 1
            out_la = {}
            out_la["first"] = la.termA
            out_la["firstType"] = la.termAType
            out_la["second"] = la.termB
            out_la["secondType"] = la.termBType
            out_la["justification"] = la.justification
            out["linguistic association"].append(out_la)
        output["potential weakness"].append(out)
        la_count_list.append(countLA)


    print("...Linguistic Assocation per Weakness: {}".format(str(la_count_list)))
    target = infile[3:-5]
    now = datetime.now() 
    filename = "./outputs/out-" + target + "-" + now.strftime("%d%m%Y%H%M") + ".json"
    dump_json_to_file(output, filename)

def dump_json_to_file(json_object, filepath):
    jsonString = json.dumps(json_object)
    with open(filepath, 'w') as outfile:
        outfile.write(jsonString)
        outfile.close()

if __name__ == '__main__':
    start_time = time.time()
    main(sys.argv[1:])
    print("=========== {} seconds ===========".format((time.time() - start_time)))