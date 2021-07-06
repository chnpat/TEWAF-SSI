import json
from models.SystemicMeaning import SystemicMeaning


class SSIDesignAnalyzer:
    def __init__(self, infile, intfile) -> None:
        self.infile = infile
        self.intfile = intfile

    def read_notion(self):
        filename = "./intermediate files/"+self.intfile
        with open(filename) as file:
            notions = json.load(file)
            file.close()

        print("Read an SSI general notions' file successfully: {} entries found\n".format(len(
            notions["SSI.notions"])))

        return notions

    def read_input(self):
        infilename = self.infile
        with open("./inputs/"+infilename) as infile:
            design = json.load(infile)
            infile.close()
        return design

    def analyze_meaning(self):
        notions = self.read_notion()
        design = self.read_input()
        updatedSM = []
        for data in design["SSI Systemic Meaning"]:
            meaning = SystemicMeaning(
                data["id"], data["subject"], data["operation"], data["data"])
            print("> Processing SSI Systemic Meaning ID: {}".format(meaning.id))
            notions = meaning.get_eqv_set(notions)
            meaning.get_synonym_set()
            updatedSM.append(meaning)
        return updatedSM
