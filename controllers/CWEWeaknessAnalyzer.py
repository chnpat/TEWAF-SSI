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
        
        for data in cwm["CWE.Entries"]:
            meaning = CWEWeaknessMeaning(data["id"], data["SystemComponent"], data["SystemFunction"], data["SystemObject"])
            CWM_list.append(meaning)

        print("Read a CWE weakness meaning's file successfully: {} entries found.\n".format(len(CWM_list)))
        print("...CWE weakness meanings are prepared successfully.\n")
        return CWM_list