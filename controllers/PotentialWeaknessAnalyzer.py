import json
from models.PotentialWeakness import PotentialWeakness
from models.LinguisticAssociation import LinguisticAssociation
from models.CWEWeaknessMeaning import CWEWeaknessMeaning
from models.SystemicMeaning import SystemicMeaning
import spacy

nlp = spacy.load('en_core_web_md')


class PotentialWeaknessAnalyzer:
    def __init__(self, no_edge=[]) -> None:
        self.tnw = []
        self.iteration = 1
        self.last_node_id = 1
        self.last_edge_id = 1
        self.result = []

        with open("./intermediate files/"+no_edge, 'r') as file:
            data = json.load(file)
            file.close()

        print("Read an SSI intitial no edge pairs successfully: {} pairs found.\n".format(len(data)))
        self.no_edge = data

    def read_tnw(self, file):
        with open("./intermediate files/" + file) as tnwfile:
            self.tnw = json.load(tnwfile)
            tnwfile.close()

        print("Read an SSI text network's file successfully: {} nodes and {} edges are found.\n".format(len(self.tnw["SSI.TextNetwork"]["node"]),len(self.tnw["SSI.TextNetwork"]["edge"])))

        self.last_node_id = self.tnw["SSI.TextNetwork"]["node"][-1]["Id"]
        self.last_edge_id = self.tnw["SSI.TextNetwork"]["edge"][-1]["Id"]

        if len(file.split("_")) > 1:
            self.iteration = int(file.split("_")[1])

    def analyze_la(self, usm, cwm, file):

        print("----------------------------------------------------------------------")
        print(" ANALYZING LINGUISTIC ASSOCIATIONS AND POTENTIAL WEAKNESS")
        print("----------------------------------------------------------------------")
        self.read_tnw(file)

        count = 0

        for s in usm:

            for c in cwm:

                pw = PotentialWeakness(s, c)

                # SUB ~ SComp
                for sb in s.subject:
                    for sc in c.systemComponent:
                        pw = self.check_la(
                            sb, sc, "subject", "systemComponent", pw)
                        count += 1
                # DAT ~ SObj
                for dt in s.data:
                    for so in c.systemObject:
                        pw = self.check_la(dt, so, "data", "systemObject", pw)
                        count += 1
                # OPS ~ SFunc
                for op in s.operation:
                    for sf in c.systemFunction:
                        pw = self.check_la(op, sf, "operation",
                                           "systemFunction", pw)
                        count += 1

                if self.check_pw(pw):
                    self.result.append(pw)

        print("\n...Potential weaknesses and linguistic associations are analyzed successfully from {} pairs.\n".format(count))
        return self.result

    def check_in_tnw(self, txt):

        result = list(
            filter(lambda d: d["Label"] == txt, self.tnw["SSI.TextNetwork"]["node"]))

        if len(result) > 0:
            return result[0]["Id"]

        return -1

    def check_la_in_tnw(self, id_a, id_b):

        if id_a == id_b:
            return True

        result = list(filter(lambda d: (d["Source"] == id_a and d["Target"] == id_b) or (
            d["Source"] == id_b and d["Target"] == id_a),  self.tnw["SSI.TextNetwork"]["edge"]))

        if len(result) > 0:
            return True

        return False

    def check_la(self, a, b, atype, btype, pw):

        a_id = self.check_in_tnw(a)
        b_id = self.check_in_tnw(b)
        if a_id != -1 and b_id != -1:
            if self.check_la_in_tnw(a_id, b_id):

                # print("( {}:{} , {}:{} )".format(a, atype, b, btype))
                la = LinguisticAssociation(a, b, atype, btype)
                pw.add_one_la(la)
        #     else:
        #         if self.update_la(a, b, a_id, b_id):
        #             la = LinguisticAssociation(a, b, atype, btype)
        #             pw.add_one_la(la)
        # else:
        #     if self.update_la(a, b, a_id, b_id):
        #         la = LinguisticAssociation(a, b, atype, btype)
        #         pw.add_one_la(la)

        return pw

    def update_la(self, a, b, a_id, b_id):

        tokens = nlp(a + " " + b)
        token1, token2 = tokens[0], tokens[1]
        sim_score = token1.similarity(token2)
        # print("Similarity ({} , {}): {}".format(token1, token2, sim_score))

        if [a,b] in self.no_edge["SSI.No_Edge"] or [b, a] in self.no_edge["SSI.No_Edge"]:
            return False

        if sim_score > 0.7:
            manual_la = input(
                "----> Is this ('{}', '{}') pair linguistically associated ? (y/n): ".format(a, b))
            if(manual_la == 'y'):
                a_update_id = self.update_node(a, a_id)
                b_update_id = self.update_node(b, b_id)
                self.update_edge(a_update_id, b_update_id)
                return True
            else:
                self.no_edge["SSI.No_Edge"].append([a,b])
        return False

    def update_node(self, lbl, id):
        if id == -1:
            new_node_ent = {}
            new_node_ent["Id"] = self.last_node_id + 1
            new_node_ent["Label"] = lbl
            new_node_ent["Timeset"] = ""
            new_node_ent["Degree"] = 1
            self.tnw["SSI.TextNetwork"]["node"].append(new_node_ent)
            self.last_node_id += 1
            return new_node_ent["Id"]
        else:
            for i, node in enumerate(self.tnw["SSI.TextNetwork"]["node"]):
                if node["Id"] == id:
                    new_deg = node["Degree"] + 1
                    self.tnw["SSI.TextNetwork"]["node"][i].update(
                        {"Degree": new_deg})
                    return id
        return -1

    def update_edge(self, a_id, b_id):
        for edge in self.tnw["SSI.TextNetwork"]["edge"]:
            if (edge["Source"] == a_id and edge["Target"] == b_id) or (edge["Source"] == b_id and edge["Target"] == a_id):
                return False

        new_edge_ent = {}
        new_edge_ent["Id"] = self.last_edge_id + 1
        new_edge_ent["Source"] = a_id
        new_edge_ent["Target"] = b_id
        new_edge_ent["Type"] = "Undirected"
        new_edge_ent["Weight"] = 1
        new_edge_ent["Label"] = ""
        new_edge_ent["Timeset"] = ""
        self.tnw["SSI.TextNetwork"]["edge"].append(new_edge_ent)
        self.last_edge_id += 1

    def check_pw(self, pw):
        if len(pw.CorrespondingLA) > 0:
            count_s = 0
            count_o = 0
            count_d = 0
            for la in pw.CorrespondingLA:
                if la.termAType == "subject" and la.termBType == "systemComponent":
                    count_s += 1
                elif la.termAType == "operation" and la.termBType == "systemFunction":
                    count_o += 1
                elif la.termAType == "data" and la.termBType == "systemObject":
                    count_d += 1
            a = count_s > 0
            b = count_o > 0
            c = count_d > 0

            return a and (b or c) or (b and c)
