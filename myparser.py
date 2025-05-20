class Parser:

    def __init__(self, tokens):
        self.tokens = tokens 
        self.index = 0 
        self.token = self.tokens[self.index]
    

    def factor(self):
        if self.token.type == "int" or self.token.type == "flt":
            return self.token
        elif self.token.val == "(":
            self.move()
            expression = self.expression()
            return expression

    def term(self):
        left_node = self.factor()
        self.move()
        
        while self.token.val == "*" or self.token.val == "/":

            operation = self.token 
            self.move()
            right_node = self.factor()
            self.move()
            left_node = [left_node, operation, right_node] 

        return left_node 

    def expression(self):
        left_node = self.term()
        while self.token.val == "+" or self.token.val == "-":
            operation = self.token 
            self.move()
            right_node = self.term()
            left_node = [left_node, operation, right_node] 
        return left_node  

    def parse(self):
        return self.expression()

    def move(self):
        self.index += 1 
        if self.index < len(self.tokens):
            self.token = self.tokens[self.index]