class CWEWeaknessMeaning:
    def __init__(self, id=1, scomp=[], sfunc=[], sobj=[]) -> None:
        self.id = id
        self.systemComponent = scomp
        self.systemFunction = sfunc
        self.systemObject = sobj

    def __repr__(self) -> str:
        return """
            -----------------
            CWE Weakness Meaning ID: {}
            -----------------
            SYSTEM COMPONENT: {} 
            SYSTEM FUNCTION:  {}  
            SYSTEN OBJECT:    {} 
            -----------------
        """.format(self.id, self.systemComponent, self.systemFunction, self.systemComponent)