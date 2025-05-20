class Parser:

    def __init__(self, tokens):
        self.tokens = tokens 
        self.index = 0 
        self.token = self.tokens[self.index]
    
    def move(self):
        self.index += 1 
        if self.index < len(self.tokens):
            self.token = self.tokens[self.index]
        else:
            self.token = None  # No more tokens

    def factor(self):
        # Unary minus
        if self.token and self.token.val == "-":
            op = self.token
            self.move()
            node = self.factor()
            return [op, node]  # Unary minus node

        # Number
        if self.token and (self.token.type == "int" or self.token.type == "flt"):
            node = self.token
            self.move()
            return node

        # Parentheses
        elif self.token and self.token.val == "(":
            self.move()
            expr = self.expression()
            if self.token and self.token.val == ")":
                self.move()
            return expr

        # Unexpected token
        raise Exception("Unexpected token in factor")

    def term(self):
        left_node = self.factor()
        
        while self.token and (self.token.val == "*" or self.token.val == "/"):
            operation = self.token
            self.move()
            right_node = self.factor()
            left_node = [left_node, operation, right_node]

        return left_node

    def expression(self):
        left_node = self.term()
        while self.token and (self.token.val == "+" or self.token.val == "-"):
            operation = self.token
            self.move()
            right_node = self.term()
            left_node = [left_node, operation, right_node]
        return left_node  

    def parse(self):
        return self.expression()
