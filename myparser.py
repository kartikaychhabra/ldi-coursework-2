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
        
        # Variable reference
        elif self.token and self.token.type.startswith("var"):
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
        raise Exception(f"Unexpected token in factor: {self.token}")

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
    
    def variable(self):
        if self.token.type.startswith("var"):
            var = self.token
            self.move()
            return var
        raise Exception(f"Expected variable, got {self.token}")

    def statement(self):
        if self.token.type == "decl":
             # Variable Assignment
             self.move()
             left_node = self.variable()
             if self.token and self.token.val == "=":
                operation = self.token 
                self.move()
                right_node = self.expression()
                return [left_node, operation, right_node]
             else:
                raise Exception("Expected '=' after variable in declaration")
             
        elif self.token.type == "int" or self.token.type == "flt" or self.token.type.startswith("var") or self.token.val == "(" or self.token.val == "-":
            # Arithmetic Expression
            return self.expression()
        else:
            raise Exception(f"Unexpected token at start of statement: {self.token}")

    def parse(self):
        return self.statement()