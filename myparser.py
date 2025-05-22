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

        # String literal
        if self.token and self.token.type == "str":
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
    
    def print_statement(self):
        
        self.move()  # consume 'print'
        expr = self.expression()
        return ["print", expr]


    def statement(self):

        # Handle while loop
        if self.token.type == "kw" and self.token.val == "while":
            return self.parse_while_statement()

        # Handle if-else statement
        if self.token.type == "kw" and self.token.val == "if":
            return self.parse_if_statement()

        if not self.token:
            raise Exception("No tokens to parse")

        # Handle 'let' declaration
        if self.token.type == "decl" and self.token.val == "let":
            self.move()
            left_node = self.variable()

            if self.token and self.token.val == "=":
                operation = self.token
                self.move()

                if self.token and self.token.val == "=":
                    raise Exception("Chained assignments like 'a = b = 5' are not supported.")

                right_node = self.expression()
                return [left_node, operation, right_node]
            else:
                raise Exception("Expected '=' after variable in declaration")

        # Handle print statement
        if self.token.val == "print":
            return self.print_statement()

        if self.token.type == "decl" and self.token.val == "print":
            self.move()
            expr = self.expression()
            return ["print", expr]

        # Handle assignment or fallback to expression
        if self.token.type.startswith("var"):
            start_index = self.index
            left_node = self.token
            self.move()

            if self.token and self.token.val == "=":
                operation = self.token
                self.move()

                if self.token and self.token.val == "=":
                    raise Exception("Chained assignments like 'a = b = 5' are not supported.")

                right_node = self.expression()
                return [left_node, operation, right_node]
            else:
                # Not an assignment; backtrack and parse as expression
                self.index = start_index
                self.token = self.tokens[self.index]
                return self.expression()

        # Default: just an expression
        return self.expression()


            
    def parse_statements(self):
        statements = []
        while self.token is not None:
            stmt = self.statement()
            statements.append(stmt)
            if self.token and self.token.val == ";":
                self.move()  # consume semicolon
            else:
                break
        return statements

    def parse(self):
        result = self.parse_statements()
        # Check if there are any tokens left that weren't processed
        if self.token is not None:
            raise Exception(f"Unexpected token at end: {self.token}")
        return result
    
    def parse_block(self):
        if self.token and self.token.val == "{":
            self.move()
            statements = []
            while self.token and self.token.val != "}":
                stmt = self.statement()
                statements.append(stmt)
                if self.token and self.token.val == ";":
                    self.move()
            if self.token and self.token.val == "}":
                self.move()
                return statements
            else:
                raise Exception("Expected '}' at end of block")
        else:
            raise Exception("Expected '{' to start block")

    def parse_if_statement(self):
        self.move()  # consume 'if'

        if self.token.val != "(":
            raise Exception("Expected '(' after 'if'")
        self.move()

        condition = self.expression()

        if self.token.val != ")":
            raise Exception("Expected ')' after if condition")
        self.move()

        then_block = self.parse_block()

        else_block = []
        if self.token and self.token.val == "else":
            self.move()
            else_block = self.parse_block()

        return ["if", condition, then_block, else_block]
    
    def parse_while_statement(self):
        self.move()  # consume 'while'

        if self.token.val != "(":
            raise Exception("Expected '(' after 'while'")
        self.move()

        condition = self.expression()

        if self.token.val != ")":
            raise Exception("Expected ')' after while condition")
        self.move()

        body = self.parse_block()
        return ["while", condition, body]
    


