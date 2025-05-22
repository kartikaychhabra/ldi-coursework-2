from tokens import Integer, Float, BooleanValue, String

class Interpreter:

    def __init__(self, tree, base):
        self.tree = tree
        self.data = base  # Data store with read(var) and write(var, val) methods

    def get_value(self, token):
        # If token is already a native Python value, return it directly
        if isinstance(token, (int, float, bool)):
            return token

        # If token has .type and .val attributes (expected)
        if hasattr(token, "type") and hasattr(token, "val"):

            val = token.val
            typ = token.type.lower()

            if typ == "int":
                try:
                    return int(val)
                except ValueError:
                    raise Exception(f"Invalid integer literal: {val}")

            elif typ == "flt":
                try:
                    return float(val)
                except ValueError:
                    raise Exception(f"Invalid float literal: {val}")

            elif typ == "bool_val":
                val_lower = str(val).lower()
                if val_lower == "true":
                    return True
                elif val_lower == "false":
                    return False
                else:
                    raise Exception(f"Invalid boolean literal: {val}")
            if typ == "str":
                return str(val)

            elif typ.startswith("var"):
                # Variable lookup from data store
                var_name = val
                try:
                    value = self.data.read(var_name)
                    # value can be token or native value
                    if hasattr(value, "type") and hasattr(value, "val"):
                        return self.get_value(value)
                    else:
                        return value
                except KeyError:
                    raise Exception(f"Undefined variable: {var_name}")

            else:
                raise Exception(f"Unsupported token type in get_value: {typ}")

        # If token is a list (subtree), recursively evaluate
        if isinstance(token, list):
            return self.evaluate(token)

        raise Exception(f"Cannot get value from token: {token}")

    def convert_to_token(self, value):
        # Convert native python values back into tokens for consistency
        if isinstance(value, bool):
            return BooleanValue("true" if value else "false")
        elif isinstance(value, int):
            return Integer(str(value))
        elif isinstance(value, float):
            return Float(str(value))
        elif isinstance(value, str):
            return String(value)
        else:
            raise Exception(f"Cannot convert result of type {type(value)} to token")

    def compute_binary(self, left_token, op_token, right_val):
        # left_token is usually a token (for assignment), right_val is native python value
        op = op_token.val.lower()

        # Assignment: left_token must be variable token
        if op == "=":
            if not (hasattr(left_token, "type") and left_token.type.startswith("var")):
                raise Exception("Left operand of '=' must be a variable")
            var_name = left_token.val
            self.data.write(var_name, right_val)
            # For assignment, you can return the assigned value wrapped as token
            return self.convert_to_token(right_val)

        # For other operations, get native python value for left operand
        left_val = self.get_value(left_token)

        result = None
        if op == "+":
            # Prevent mixing strings with numbers
            if isinstance(left_val, str) and isinstance(right_val, str):
                result = left_val + right_val
            elif isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                result = left_val + right_val
            else:
                raise Exception(f"Type error: Cannot add {type(left_val).__name__} and {type(right_val).__name__}")

        elif op == "-":
            result = left_val - right_val
        elif op == "*":
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                result = left_val * right_val
            else:
                raise Exception(f"Type error: Cannot multiply {type(left_val).__name__} with {type(right_val).__name__}")

        elif op == "/":
            result = left_val / right_val
        elif op == "==":
            result = left_val == right_val
        elif op == "!=":
            result = left_val != right_val
        elif op == "<":
            result = left_val < right_val
        elif op == ">":
            result = left_val > right_val
        elif op == "<=":
            result = left_val <= right_val
        elif op == ">=":
            result = left_val >= right_val
        elif op == "and":
            result = left_val and right_val
        elif op == "or":
            result = left_val or right_val
        else:
            raise Exception(f"Unknown binary operator: {op}")

        # Convert float results that are whole numbers to int
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        return self.convert_to_token(result)

    def compute_unary(self, op_token, val):
        op = op_token.val.lower()

        if op == "-":
            res = -val
            if isinstance(res, float) and res.is_integer():
                res = int(res)
            return self.convert_to_token(res)

        elif op == "not"  or op == "!":
            res = not val
            return self.convert_to_token(res)

        else:
            raise Exception(f"Unknown unary operator: {op}")

    def evaluate(self, expr):

         # Handle print statements: ["print", expr]
        if isinstance(expr, list) and len(expr) == 2 and expr[0] == "print":
            to_print = self.evaluate(expr[1])
            val = self.get_value(to_print)
            print(val)
            return None

        # Handle if statements: ['if', condition_expr, then_body_list, else_body_list?]
        if isinstance(expr, list) and len(expr) >= 3 and expr[0] == 'if':
            condition = expr[1]
            then_branch = expr[2]
            else_branch = expr[3] if len(expr) > 3 else None

            cond_val = self.get_value(self.evaluate(condition))
            if cond_val:
                result = None
                for stmt in then_branch:
                    result = self.evaluate(stmt)
                return result
            elif else_branch is not None:
                result = None
                for stmt in else_branch:
                    result = self.evaluate(stmt)
                return result
            return None

        # Handle while statements: ['while', condition_expr, body_list]
        if isinstance(expr, list) and len(expr) == 3 and expr[0] == 'while':
            condition = expr[1]
            body = expr[2]
            result = None
            while True:
                cond_val = self.get_value(self.evaluate(condition))
                if not cond_val:
                    break
                for stmt in body:
                    result = self.evaluate(stmt)
            return None  # while loops usually do not return a value

        # expr can be token, native value, or list (subtree)

        # If expr is not a list, just return as token or convert native python to token
        if not isinstance(expr, list):
            # Already token?
            if hasattr(expr, "type") and hasattr(expr, "val"):
                return expr
            # Native python bool/int/float
            if isinstance(expr, bool):
                return BooleanValue("true" if expr else "false")
            elif isinstance(expr, int):
                return Integer(str(expr))
            elif isinstance(expr, float):
                return Float(str(expr))
            else:
                # Could be a variable token or other token, just return as is
                return expr

        # Handle unary operations: [op, operand]
        if len(expr) == 2:
            op_token = expr[0]
            operand_expr = expr[1]

            operand_token = self.evaluate(operand_expr)
            operand_val = self.get_value(operand_token)
            return self.compute_unary(op_token, operand_val)

        # Handle binary operations: [left, op, right]
        if len(expr) == 3:
            left_expr, op_token, right_expr = expr

            left_token = self.evaluate(left_expr)
            right_token = self.evaluate(right_expr)

            right_val = self.get_value(right_token)

            return self.compute_binary(left_token, op_token, right_val)

        # Single element expressions (e.g. parentheses) just evaluate inside
        if len(expr) == 1:
            return self.evaluate(expr[0])

        raise Exception(f"Invalid expression format: {expr}")

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree
        return self.evaluate(tree)
