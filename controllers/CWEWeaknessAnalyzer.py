import json
from models.CWEWeaknessMeaning import CWEWeaknessMeaning

class CWEWeaknessAnalyzer:
    def __init__(self, cwmfile) -> None:
        self.cwmfile = cwmfile

    def read_file(self):
        print("----------------------------------------------------------------------")
        print(" PREPARING CWE WEAKNESS MEANING")
        print("----------------------------------------------------------------------")
        CWM_list = []
        with open("./intermediate files/" + self.cwmfile) as cwmfile:
            cwm = json.load(cwmfile)
            cwmfile.close()
        
        ibm = [211, 317, 406, 476, 576, 669, 688, 779, 833, 1124] 
        sovrin = [32, 106, 211, 317, 327, 453, 704, 710, 1234, 1239] 
        uport = [9, 168, 211, 284, 317, 406, 447, 669, 779, 829] 

        for data in cwm["CWE.Entries"]:
            if data["id"] in uport:
                meaning = CWEWeaknessMeaning(data["id"], data["SystemComponent"], data["SystemFunction"], data["SystemObject"])
                CWM_list.append(meaning)

        print("Read a CWE weakness meaning's file successfully: {} entries found.\n".format(len(CWM_list)))
        print("...CWE weakness meanings are prepared successfully.\n")
        return CWM_list