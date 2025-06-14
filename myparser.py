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
        
        # List literal
        if self.token and self.token.type == "lbracket":
             return self.parse_list_literal()
        
        # Dictionary literal
        if self.token and self.token.type == "brace" and self.token.val == "{":
            return self.parse_dict_literal()

        # Unexpected token
        raise Exception(f"Unexpected token in factor: {self.token}")


    def term(self):

        left_node = self.postfix_expression()
        while self.token and (self.token.val == "*" or self.token.val == "/"):
            operation = self.token
            self.move()
            right_node = self.postfix_expression()
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


    def is_valid_assignment_target(self, node):
        # Valid targets: simple variable or index access
        if isinstance(node, list) and len(node) == 3 and node[0] == "index_access":
            return True
        if hasattr(node, "type") and node.type.startswith("var"):
            return True
        return False


    def statement(self):
        # Delete statement
        if self.token and self.token.type == "kw" and self.token.val == "delete":
            self.move()  # consume 'delete'
            target = self.postfix_expression()
            if not self.is_valid_assignment_target(target):
                raise Exception("Can only delete a variable or dictionary/list index")
            return ["delete", target]

        # If statement
        if self.token and self.token.type == "kw" and self.token.val == "if":
            return self.parse_if_statement()

        # While statement
        if self.token and self.token.type == "kw" and self.token.val == "while":
            return self.parse_while_statement()

        # Let declaration
        if self.token and self.token.type == "decl" and self.token.val == "let":
            self.move()
            left_node = self.expression()  # Changed from postfix_expression to expression

            if not self.is_valid_assignment_target(left_node):
                raise Exception("Left operand of '=' must be a variable or dictionary index")

            if self.token and self.token.val == "=":
                operation = self.token
                self.move()

                if self.token and self.token.val == "=":
                    raise Exception("Chained assignments like 'a = b = 5' are not supported.")

                right_node = self.expression()
                return [left_node, operation, right_node]
            else:
                raise Exception("Expected '=' after variable in declaration")

        # Print statement
        if self.token and self.token.val == "print":
            return self.print_statement()

        # Try to parse as assignment or expression
        left_node = self.expression()  # Changed from postfix_expression to expression
        
        # Check if this is an assignment
        if self.token and self.token.val == "=":
            if not self.is_valid_assignment_target(left_node):
                raise Exception("Left operand of '=' must be a variable or indexable expression")
                
            operation = self.token
            self.move()

            if self.token and self.token.val == "=":
                raise Exception("Chained assignments like 'a = b = 5' are not supported.")

            right_node = self.expression()
            return [left_node, operation, right_node]
        else:
            # It's just an expression
            return left_node

            
    def parse_statements(self):
        statements = []
        while self.token is not None:
            stmt = self.statement()
            statements.append(stmt)
            
            # Handle optional semicolon
            if self.token and self.token.val == ";":
                self.move()  # consume semicolon
                
            # Check if we're at the end or need to continue
            if self.token is None:
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
    
    def parse_list_literal(self):
        # Current token is '['
        if self.token.type != "lbracket":
            raise Exception("Expected '[' to start list literal")
        self.move()  # consume '['

        elements = []
        while self.token and self.token.type != "rbracket":
            element = self.expression()
            elements.append(element)

            if self.token and self.token.type == "comma":
                self.move()  # consume comma and continue parsing elements
            elif self.token and self.token.type == "rbracket":
                break
            else:
                raise Exception("Expected ',' or ']' in list literal")

        if self.token and self.token.type == "rbracket":
            self.move()  # consume ']'
            return ["list_literal", elements]
        else:
            raise Exception("Expected ']' at end of list literal")

    
    def postfix_expression(self):
        # Start by parsing a factor (number, var, list literal, etc)
        node = self.factor()

        while True:
            # Check for list indexing: [ expr ]
            if self.token and self.token.type == "lbracket":
                self.move()  # consume '['
                index_expr = self.expression()
                if not (self.token and self.token.type == "rbracket"):
                    raise Exception("Expected ']' after index expression")
                self.move()  # consume ']'
                # Wrap node as index access
                node = ["index_access", node, index_expr]

            # Check for method call: .methodName(args)
            elif self.token and self.token.val == ".":
                self.move()  # consume '.'
                if not (self.token and self.token.type.startswith("var")):
                    raise Exception("Expected method name after '.'")
                method_name = self.token
                self.move()

                if not (self.token and self.token.val == "("):
                    raise Exception("Expected '(' after method name")
                self.move()  # consume '('

                args = []
                if self.token and self.token.val != ")":
                    while True:
                        arg = self.expression()
                        args.append(arg)
                        if self.token and self.token.val == ",":
                            self.move()  # consume ','
                            continue
                        else:
                            break

                if not (self.token and self.token.val == ")"):
                    raise Exception("Expected ')' after method call arguments")
                self.move()  # consume ')'

                # Wrap node as method call
                node = ["method_call", node, method_name, args]

            else:
                # No more postfix operators
                break

        return node
    
    def parse_dict_literal(self):
        if self.token.type != "brace" or self.token.val != "{":
            raise Exception("Expected '{' to start dictionary literal")
        
        self.move()  # consume '{'
        pairs = []

        while self.token and not (self.token.type == "brace" and self.token.val == "}"):
            # Treat unquoted variable keys as string literals
            if self.token.type.startswith("var"):
                key_token = self.token
                key = ["str", key_token.val]  # Convert to string literal
                self.move()
            else:
                key = self.expression()  # Fallback to full expression

            if not (self.token and self.token.type == "colon"):
                raise Exception("Expected ':' between key and value in dict")
            self.move()  # consume ':'

            value = self.expression()
            pairs.append([key, value])

            if self.token and self.token.type == "comma":
                self.move()  # consume ',' and continue
            elif self.token and self.token.type == "brace" and self.token.val == "}":
                break
            else:
                raise Exception("Expected ',' or '}' in dict literal")

        if self.token and self.token.type == "brace" and self.token.val == "}":
            self.move()  # consume '}'
            return ["dict_literal", pairs]
        else:
            raise Exception("Expected '}' at end of dictionary literal")