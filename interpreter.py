from tokens import Integer, Float

class Interpreter: 

    def __init__(self, tree, base):
        self.tree = tree
        self.data = base 

    def read_int(self, val):
        return int(val)

    def read_flt(self, val):
        return float(val)
    
    def get_value(self, token):
        """Get the actual value of a token, resolving variables"""
        if token.type == "int":
            return int(token.val)
        elif token.type == "flt":
            return float(token.val)
        elif token.type.startswith("var"):
            # Resolve variable reference
            var_name = token.val
            try:
                value = self.data.read(var_name)
                # If stored as raw value, return it
                if isinstance(value, (int, float)):
                    return value
                # If stored as token, get its value
                elif hasattr(value, 'type'):
                    return self.get_value(value)
                return value
            except KeyError:
                raise Exception(f"Undefined variable: {var_name}")
        else:
            raise Exception(f"Cannot get value of token type: {token.type}")

    def compute_binary(self, left, op, right):
        if op.val == "=":
            # Evaluate right side fully
            if isinstance(right, list):
                right_val = self.interpret(right)
            else:
                right_val = right
                
            # Store the value (either token or raw value)
            if hasattr(right_val, "type"):
                if right_val.type == "int":
                    self.data.write(left.val, int(right_val.val))
                elif right_val.type == "flt":
                    self.data.write(left.val, float(right_val.val)) 
                elif right_val.type.startswith("var"):
                    # If right side is variable, store its value
                    var_value = self.get_value(right_val)
                    self.data.write(left.val, var_value)
                else:
                    self.data.write(left.val, right_val)
            else:
                # Raw value
                self.data.write(left.val, right_val)
            
            return self.data.read_all()
        
        # For arithmetic operations
        left_val = None
        right_val = None
        
        # Get the actual values of operands
        if isinstance(left, list):
            # If left is an expression, evaluate it
            left_result = self.interpret(left)
            if hasattr(left_result, "type"):
                left_val = self.get_value(left_result)
            else:
                left_val = left_result
        else:
            # Direct token
            left_val = self.get_value(left)
            
        if isinstance(right, list):
            # If right is an expression, evaluate it
            right_result = self.interpret(right)
            if hasattr(right_result, "type"):
                right_val = self.get_value(right_result)
            else:
                right_val = right_result
        else:
            # Direct token
            right_val = self.get_value(right)
            
        # Calculate result
        if op.val == "+":
            result = left_val + right_val
        elif op.val == "-":
            result = left_val - right_val
        elif op.val == "*":
            result = left_val * right_val
        elif op.val == "/":
            result = left_val / right_val
        else:
            raise Exception(f"Unknown operator: {op.val}")
            
        # Convert float results to int if they're whole numbers
        if isinstance(result, float) and result.is_integer():
            result = int(result)
            
        # Return as appropriate token
        if isinstance(result, int):
            return Integer(str(result))
        elif isinstance(result, float):
            return Float(str(result))
        else:
            raise Exception(f"Unexpected result type: {type(result)}")

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree
            
        # Handle unary minus
        if isinstance(tree, list) and len(tree) == 2 and tree[0].val == "-":
            node = tree[1]
            val = self.interpret(node) if isinstance(node, list) else node
            
            if hasattr(val, "type"):
                val_num = self.get_value(val)
            else:
                val_num = val
                
            result = -val_num
            
            # Convert float to int if it's a whole number
            if isinstance(result, float) and result.is_integer():
                result = int(result)
                
            return Integer(str(result)) if isinstance(result, int) else Float(str(result))
            
        # Handle leaf node
        if not isinstance(tree, list):
            return tree
            
        # Handle binary operations
        left = tree[0]
        op = tree[1]
        right = tree[2]
        
        return self.compute_binary(left, op, right)