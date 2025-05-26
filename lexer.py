from tokens import Token, Integer, Operation, Float, Declaration, Variable, Boolean, BooleanValue, String, Keyword
import string

class Lexer:

    digits = "0123456789"
    operations = "+-*/()=<>!;{}[],.:"
    stopwords = [" ", "\n", "\t", "\r"]

    letters =  string.ascii_letters + "_"
    declarations = ["let", "print"]
    boolean_ops = ["and", "or", "not"]
    boolean_vals = ["true", "false"]
    keywords = ["if", "else", "while", "input", "delete"]  # Added "delete" here


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
                # Handle multi-character operators
                if self.char == "=" and self.peek() == "=":
                    self.token = Operation("==")
                    self.move()
                    self.move()
                elif self.char == "!" and self.peek() == "=":
                    self.token = Operation("!=")
                    self.move()
                    self.move()
                elif self.char == "<" and self.peek() == "=":
                    self.token = Operation("<=")
                    self.move()
                    self.move()
                elif self.char == ">" and self.peek() == "=":
                    self.token = Operation(">=")
                    self.move()
                    self.move()
                elif self.char in "{}":
                    self.token = Token("brace", self.char)
                    self.move()
                elif self.char == "[":
                    self.token = Token("lbracket", self.char)
                    self.move()
                elif self.char == "]":
                    self.token = Token("rbracket", self.char)
                    self.move()
                elif self.char == ",":
                    self.token = Token("comma", self.char)
                    self.move()
                elif self.char == ":":
                    self.token = Token("colon", self.char)
                    self.move()
                else:
                    self.token = Operation(self.char)
                    self.move()

            elif self.char in Lexer.stopwords:
                self.move()
                continue

            elif self.char == '#':
                # ✅ Skip comments
                while self.char != '\n' and self.index < len(self.text):
                    self.move()
                self.move()  # also skip the newline
                continue

            elif self.char == '"':
                self.token = self.extract_string()

            elif self.char in Lexer.letters:
                word = self.extract_word()

                if word in Lexer.declarations:
                    self.token = Declaration(word)
                elif word in Lexer.boolean_ops:
                    self.token = Boolean(word)
                elif word in Lexer.boolean_vals:
                    self.token = BooleanValue(word)
                elif word in Lexer.keywords:
                    self.token = Keyword(word)
                else:
                    self.token = Variable(word)

            else:
                raise Exception(f"Unknown character: {self.char}")

            self.tokens.append(self.token)

        return self.tokens

    def extract_string(self):
        string_val = ""
        self.move()  # skip opening quote

        while self.char != '"' and self.index < len(self.text):
            if self.char == '\\':  # escape sequence start
                self.move()
                if self.char == 'n':
                    string_val += '\n'
                elif self.char == 't':
                    string_val += '\t'
                elif self.char == '"':
                    string_val += '"'
                else:
                    raise Exception(f"Unknown escape sequence \\{self.char}")
                self.move()
            else:
                string_val += self.char
                self.move()

        if self.char != '"':
            raise Exception("Unterminated string literal")

        self.move()  # skip closing quote

        return String(string_val)

    
    def peek(self):
        # Look at the next character without moving
        peek_index = self.index + 1
        if peek_index < len(self.text):
            return self.text[peek_index]
        return None

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