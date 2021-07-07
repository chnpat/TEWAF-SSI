from models.LinguisticAssociation import LinguisticAssociation
from models.CWEWeaknessMeaning import CWEWeaknessMeaning
from models.SystemicMeaning import SystemicMeaning


class PotentialWeakness:
    def __init__(self, sm=SystemicMeaning(), cwm=CWEWeaknessMeaning) -> None:
        self.CorrespondingSSM = sm
        self.CorrespondingCWM = cwm
        self.CorrespondingLA = list()


    def get_SSM(self):
        return self.CorrespondingSSM

    def get_CWM(self):
        return self.CorrespondingCWM

    def get_LA(self):
        if len(self.CorrespondingLA) > 0:
            return self.CorrespondingLA
        else:
            return None
    
    def set_SSM(self, sm):
        self.CorrespondingSSM = sm

    def set_CWM(self, cwm):
        self.CorrespondingCWM = cwm

    def add_la_by_terms(self, a, b):
        la = LinguisticAssociation(a, b)
        self.CorrespondingLA.append(la)

    def add_la_by_terms_justify(self, a, b, justify):
        la = LinguisticAssociation(a, b)
        la.set_justification(justify)
        self.CorrespondingLA.append(la)

    def add_one_la(self, la):
        self.CorrespondingLA.append(la)

    def add_list_la(self, la):
        self.CorrespondingLA.extend(la)

    def set_new_la(self, la):
        self.CorrespondingLA = la