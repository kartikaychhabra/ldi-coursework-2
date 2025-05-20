from tokens import Token, Integer, Operation, Float

class Lexer:

    digits = "0123456789"
    operations = "+-*/()"
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



        