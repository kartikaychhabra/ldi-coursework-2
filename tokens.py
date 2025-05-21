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

class Declaration(Token):
    def __init__(self, val):
        super().__init__("decl", val)

class Variable(Token):
    def __init__(self, val):
        super().__init__("var(?)", val)

class Boolean(Token):
    def __init__(self, val):
        super().__init__("bool_op", val)  # Changed to bool_op to distinguish from bool values

class BooleanValue(Token):
    def __init__(self, val):
        super().__init__("bool_val", val)
