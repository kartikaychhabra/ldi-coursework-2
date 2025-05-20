class Parser:

    def __init__(self, tokens):
        self.tokens = tokens 
        self.index = 0 
        self.token = self.tokens[self.index]

    def factor(self):
        if self.token.type == "int" or self.token.type == "flt":
            return self.token
    
    def term(self):
        left_node = self.factor()
        self.move()
        output = left_node 
        
        if self.token.val == "*" or self.token.val == "/":

            operation = self.token 
            self.move()
            right_node = self.factor()
            self.move()
            output = [left_node, operation, right_node] 

        return output 

    def expression(self):
        left_node = self.term()
        output = left_node 
        if self.token.val == "+" or self.token.val == "-":
            operation = self.token 
            self.move()
            right_node = self.term()
            output = [left_node, operation, right_node] 
        return output 

    def parse(self):
        return self.expression()

    def move(self):
        self.index += 1 
        if self.index < len(self.tokens):
            self.token = self.tokens[self.index]