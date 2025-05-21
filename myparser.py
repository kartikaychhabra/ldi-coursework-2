class Parser:

    def __init__(self, tokens):
        self.tokens = tokens 
        self.index = 0 
        self.token = self.tokens[self.index] if tokens else None
    
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
            node = self.factor()  # Allow unary minus on expressions like: - (3 + 2)
            return [op, node]  # Unary minus node

        # Unary not: support both 'not' and '!' forms
        if self.token and self.token.val in ["not", "!"]:
            op = self.token
            self.move()
            node = self.factor()  # Allow expressions like: ! (5 > 3)
            return [op, node]  # Unary not node

        # Parentheses
        if self.token and self.token.val == "(":
            self.move()
            expr = self.boolean_expression()  # Parse a full expression inside parentheses
            if self.token and self.token.val == ")":
                self.move()
                return expr
            else:
                raise Exception("Expected closing parenthesis")

        # Boolean value
        if self.token and self.token.type == "bool_val":
            node = self.token
            self.move()
            return node

        # Number
        if self.token and (self.token.type == "int" or self.token.type == "flt"):
            node = self.token
            self.move()
            return node

        # Variable reference
        if self.token and self.token.type.startswith("var"):
            node = self.token
            self.move()
            return node

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

    def arithmetic_expression(self):
        left_node = self.term()
        while self.token and (self.token.val == "+" or self.token.val == "-"):
            operation = self.token
            self.move()
            right_node = self.term()
            left_node = [left_node, operation, right_node]
        return left_node

    def comparison_expression(self):
        left_node = self.arithmetic_expression()
        
        # Handle comparison operators: ==, !=, <, >, <=, >=
        while self.token and self.token.type == "op" and self.token.val in ["==", "!=", "<", ">", "<=", ">="]:
            operation = self.token
            self.move()
            right_node = self.boolean_expression() 
            left_node = [left_node, operation, right_node]
            
        return left_node

    def boolean_expression(self):
        left_node = self.comparison_expression()
        
        # Handle boolean operators: and, or
        while self.token and self.token.type == "bool_op" and self.token.val in ["and", "or"]:
            operation = self.token
            self.move()
            right_node = self.comparison_expression()
            left_node = [left_node, operation, right_node]
            
        return left_node
    
    def expression(self):
        # The highest level expression is now boolean_expression
        return self.boolean_expression()
    
    def variable(self):
        if self.token and self.token.type.startswith("var"):
            var = self.token
            self.move()
            return var
        raise Exception(f"Expected variable, got {self.token}")

    def statement(self):
        if not self.token:
            raise Exception("No tokens to parse")
            
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
             
        # All other expressions (arithmetic, boolean, etc.)
        else:
            return self.expression()

    def parse(self):
        result = self.statement()
        # Check if there are any tokens left that weren't processed
        if self.token is not None:
            raise Exception(f"Unexpected token at end: {self.token}")
        return result