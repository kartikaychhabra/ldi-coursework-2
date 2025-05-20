class Token:

    def __init__(self, type, val):

        self.type = type 
        self.val = val 

    def __repr__(self):
        
        return str(self.val)
 
class Integer(Token):
    
    def __init__(self, val):
        super().__init__("int", val)

class Float(Token):

    def __init__(self, val):
        super().__init__("flt", val)

class Operation(Token):

    def __init__(self, val):
        super().__init__("op", val)