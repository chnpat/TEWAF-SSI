import json
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet


class SystemicMeaning:

    def __init__(self, id=1, sub=[], ops=[], dat=[]) -> None:
        self.id = id
        self.subject = sub
        self.operation = ops
        self.data = dat

    def __repr__(self) -> str:
        return """
            -----------------
            SSI Systemic Meaning ID: {}
            -----------------
            SUBJECT: {} 
            OPERATION: {}  
            DATA: {} 
            -----------------
        """.format(self.id, self.subject, self.operation, self.data)

    def get_eqv_set(self, notions):
        new_subject = set()
        new_data = set()
        FoundEqv = False

        # For SUBJECT noun terms
        for sb in self.subject:
            FoundEqv = False
            new_subject.add(sb)
            for notion in notions["SSI.notions"]:
                if sb in notion["term"]:
                    new_subject.update(notion["term"])
                    FoundEqv = True

            if not FoundEqv:
                more_term = input("""
                    '{}' is not found in SSO general notion, please add common terms separated by commas (leave empty if it is none): """.format(sb))
                if more_term != "":
                    more_term_list = more_term.split(',')
                    new_subject.update(more_term_list)
                    more_term_list.append(sb)
                    notions["SSI.notions"].append({"term": more_term_list})

        self.subject = list(new_subject)

        # For DATA noun terms   
        FoundEqv = False
        for dt in self.data:
            new_data.add(dt)
            for notion in notions["SSI.notions"]:
                if dt in notion["term"]:
                    new_data.update(notion["term"])
                    FoundEqv = True
            
            if not FoundEqv:
                more_term = input("""
                    '{}' is not found in the SSI general notions, please add common terms separated by commas (leave empty if it is none): """.format(dt))
                if more_term != "":
                    more_term_list = more_term.split(',')
                    new_data.update(more_term_list)
                    more_term_list.append(dt)
                    notions["SSI.notions"].append({"term": more_term_list})

        self.data = list(new_data)
        return notions, notions

    def get_synonym_set(self):
        syn = set()

        # For OPERATION verb terms
        for op in self.operation:
            for synset in wordnet.synsets(op, pos=wordnet.VERB):
                for lemma in synset.lemmas():
                    syn.add(lemma.name())   
            syn.add(op)
        
        list_syn = list(syn)
        break_list_syn = []
        for s in list_syn:
            break_list_syn.append(str(s).replace("_", " "))

        self.operation = list(break_list_syn)

