from tokens import Token, Integer, Operation, Float, Declaration, Variable 

class Lexer:

    digits = "0123456789"
    operations = "+-*/()="
    stopwords = [" "]
    letters = "abcdefghijklmnopqrstuvwxyz"
    declarations = ["let"]

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

            elif self.char in Lexer.letters:
                word = self.extract_word()
                
                if word in Lexer.declarations:
                    self.token = Declaration(word)
                else:
                    self.token = Variable(word)

            self.tokens.append(self.token)


        return self.tokens

    
    def extract_number(self):
        isFloat = False
        number = ""

        while self.index < len(self.text) and (self.char in Lexer.digits or self.char == "."):
            if self.char == ".":
                isFloat = True
            number += self.char
            self.move()

        return Integer(number) if not isFloat else Float(number)
    
    def extract_word(self):
        word = ""
        while self.char in Lexer.letters and self.index < len(self.text):
            word += self.char 
            self.move()

        return word 

    def move(self):

        self.index += 1 
        if self.index < len(self.text):
            self.char = self.text[self.index]



        