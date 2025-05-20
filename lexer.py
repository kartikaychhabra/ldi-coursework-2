class Lexer:

    digits = "0123456789"
    operations = "+-*/"
    stopwords = [" "]

    def __init__(self, text):
        self.text = text 
        self.index = 0 
        self.tokens = []
        self.char = self.text[self.index]
        self.token = None 
        
    
    def tokenize(self):
        while self.index < len(self.text):
            if self.char in Lexer.digits:
                self.token = self.extract_number()

            elif self.char in Lexer.operations:

                self.token = Operation(self.char)
                self.move()
            
            elif self.char in Lexer.stopwords:
                self.move()
                continue

            self.tokens.append(self.token)

        return self.tokens

    
    def extract_number(self):

        isFloat = False
        number = ""
        while (self.char in Lexer.digits or self.char == ".") and (self.index < len(self.text)):
            if  self.char == ".":
                isFloat = True 
            number += self.char 
            self.move()
        
        return Integer(number) if not isFloat else Float(number)

    def move(self):

        self.index += 1 
        if self.index < len(self.text):
            self.char = self.text[self.index]

    
class Token:

    def __init__(self, type, val):

        self.type = type 
        self.val = val 

    def __repr__(self):
        
        return self.val 
    
class Integer(Token):
    
    def __init__(self, val):
        super().__init__("int", val)

class Float(Token):

    def __init__(self, val):
        super().__init__("flt", val)

class Operation(Token):

    def __init__(self, val):
        super().__init__("op", val)


        