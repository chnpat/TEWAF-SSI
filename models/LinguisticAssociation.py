class LinguisticAssociation:

    def __init__(self, a, b, atype, btype) -> None:
        self.termA = a
        self.termB = b
        self.termAType = atype
        self.termBType = btype
        self.justification = ''

    def set_justification(self, justify):
        self.justification = justify

    def __str__(self) -> str:
        if self.justification != '':
            return "({}:{} , {}:{}) -> {}".format(self.termA, self.termAType, self.termB, self.termBType, self.justification)
        return "({}:{} , {}:{})".format(self.termA, self.termAType, self.termB, self.termBType)
