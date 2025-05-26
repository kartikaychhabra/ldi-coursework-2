from tokens import Integer, Float, BooleanValue, String

class Interpreter:

    def __init__(self, tree, base):
        self.tree = tree
        self.data = base  # Data store with read(var) and write(var, val) methods

    def get_value(self, token):
        """Convert token to native Python value"""
        # If token is already a native Python value, return it directly
        if isinstance(token, (int, float, bool, str, list, dict)):
            return token

        # If token has .type and .val attributes (expected token format)
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
                    
            elif typ == "str":
                return str(val)

            elif typ.startswith("var"):
                # Variable lookup from data store
                var_name = val
                try:
                    value = self.data.read(var_name)
                    # Recursively get value if it's also a token
                    return self.get_value(value)
                except (KeyError, AttributeError):
                    raise Exception(f"Undefined variable: {var_name}")

            else:
                raise Exception(f"Unsupported token type in get_value: {typ}")

        # If token is a list (subtree), recursively evaluate
        if isinstance(token, list):
            return self.get_value(self.evaluate(token))

        raise Exception(f"Cannot get value from token: {token}")

    def convert_to_token(self, value):
        """Convert native Python values back to tokens"""
        if isinstance(value, bool):
            return BooleanValue("true" if value else "false")
        elif isinstance(value, int):
            return Integer(str(value))
        elif isinstance(value, float):
            return Float(str(value))
        elif isinstance(value, str):
            return String(value)
        elif isinstance(value, list):
            # For lists, we can return the native list since get_value handles it
            return value
        elif isinstance(value, dict):
            # For dicts, we can return the native dict since get_value handles it
            return value
        elif value is None:
            return None
        else:
            raise Exception(f"Cannot convert result of type {type(value)} to token")

    def compute_binary(self, left_token, op_token, right_val):
        """Handle binary operations"""
        op = op_token.val.lower() if hasattr(op_token, 'val') else str(op_token).lower()

        # Assignment: left_token must be variable token or index access
        if op == "=":
            # Handle variable assignment
            if hasattr(left_token, "type") and left_token.type.startswith("var"):
                var_name = left_token.val
                self.data.write(var_name, right_val)
                return right_val
            
            # Handle index assignment: ['index_access', container_expr, key_expr]
            elif isinstance(left_token, list) and len(left_token) == 3 and left_token[0] == "index_access":
                container_token = left_token[1]
                key_token = left_token[2]

                # Get the container object and key
                container_obj = self.get_value(self.evaluate(container_token))
                key = self.get_value(self.evaluate(key_token))

                if isinstance(container_obj, dict):
                    if not isinstance(key, (str, int, float, bool)):
                        raise Exception(f"Invalid dictionary key type: {type(key).__name__}")
                    container_obj[key] = right_val
                elif isinstance(container_obj, list):
                    if not isinstance(key, int):
                        raise Exception(f"List index must be integer, got {type(key).__name__}")
                    try:
                        container_obj[key] = right_val
                    except IndexError:
                        raise Exception(f"List index {key} out of bounds")
                else:
                    raise Exception(f"Cannot assign to index of type {type(container_obj).__name__}")

                return right_val

            else:
                raise Exception("Left operand of '=' must be a variable or indexable expression")

        # Get left value for other operations
        left_val = self.get_value(left_token)

        # Arithmetic and comparison operations
        if op == "+":
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                result = left_val + right_val
            elif isinstance(left_val, str) and isinstance(right_val, str):
                result = left_val + right_val
            elif isinstance(left_val, list) and isinstance(right_val, list):
                result = left_val + right_val
            else:
                raise Exception(f"Type error: Cannot add {type(left_val).__name__} and {type(right_val).__name__}")

        elif op == "-":
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                result = left_val - right_val
            else:
                raise Exception(f"Type error: Cannot subtract {type(right_val).__name__} from {type(left_val).__name__}")

        elif op == "*":
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                result = left_val * right_val
            else:
                raise Exception(f"Type error: Cannot multiply {type(left_val).__name__} with {type(right_val).__name__}")

        elif op == "/":
            if isinstance(left_val, (int, float)) and isinstance(right_val, (int, float)):
                if right_val == 0:
                    raise Exception("Division by zero")
                result = left_val / right_val
            else:
                raise Exception(f"Type error: Cannot divide {type(left_val).__name__} by {type(right_val).__name__}")

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

        return result

    def compute_unary(self, op_token, val):
        """Handle unary operations"""
        op = op_token.val.lower() if hasattr(op_token, 'val') else str(op_token).lower()

        if op == "-":
            if isinstance(val, (int, float)):
                res = -val
                if isinstance(res, float) and res.is_integer():
                    res = int(res)
                return res
            else:
                raise Exception(f"Cannot negate {type(val).__name__}")

        elif op == "not" or op == "!":
            return not val

        else:
            raise Exception(f"Unknown unary operator: {op}")

    def evaluate(self, expr):
        """Main evaluation method"""
        
        # Handle None
        if expr is None:
            return None

        # Handle sequences of statements
        if isinstance(expr, list) and all(isinstance(e, list) for e in expr):
            result = None
            for stmt in expr:
                result = self.evaluate(stmt)
            return result

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
            
            while True:
                cond_val = self.get_value(self.evaluate(condition))
                if not cond_val:
                    break
                for stmt in body:
                    self.evaluate(stmt)
            return None

        # Handle list literals: ['list_literal', [elements]]
        if isinstance(expr, list) and len(expr) == 2 and expr[0] == "list_literal":
            elements = expr[1]
            evaluated_elements = []
            for el in elements:
                evaluated_elements.append(self.get_value(self.evaluate(el)))
            return evaluated_elements

        # Handle dictionary literals: ['dict_literal', [[key1, val1], [key2, val2], ...]]
        if isinstance(expr, list) and len(expr) == 2 and expr[0] == "dict_literal":
            pairs = expr[1]
            evaluated_dict = {}

            for pair in pairs:
                if len(pair) != 2:
                    raise Exception("Dictionary pair must have exactly 2 elements")
                    
                key_expr, val_expr = pair
                key = self.get_value(self.evaluate(key_expr))
                val = self.get_value(self.evaluate(val_expr))

                if not isinstance(key, (str, int, float, bool)):
                    raise Exception(f"Invalid dictionary key type: {type(key).__name__}")

                evaluated_dict[key] = val

            return evaluated_dict

        # Handle index access: ['index_access', container_expr, key_expr]
        if isinstance(expr, list) and len(expr) == 3 and expr[0] == "index_access":
            container_val = self.get_value(self.evaluate(expr[1]))
            index_val = self.get_value(self.evaluate(expr[2]))

            if isinstance(container_val, list):
                if not isinstance(index_val, int):
                    raise Exception(f"List index must be integer, got {type(index_val).__name__}")
                try:
                    return container_val[index_val]
                except IndexError:
                    raise Exception(f"List index {index_val} out of bounds")

            elif isinstance(container_val, dict):
                if not isinstance(index_val, (str, int, float, bool)):
                    raise Exception(f"Invalid dictionary key type: {type(index_val).__name__}")

                if index_val not in container_val:
                    raise Exception(f"Key {index_val} not found in dictionary")

                return container_val[index_val]

            else:
                raise Exception(f"Type error: cannot index {type(container_val).__name__}")

        # Handle delete statements: ['delete', target_expr]
        if isinstance(expr, list) and len(expr) == 2 and expr[0] == "delete":
            target = expr[1]

            # Handle deleting dictionary keys or list elements: ['index_access', container_expr, key_expr]
            if isinstance(target, list) and len(target) == 3 and target[0] == "index_access":
                container_token = target[1]
                key_token = target[2]

                container_obj = self.get_value(self.evaluate(container_token))
                key = self.get_value(self.evaluate(key_token))

                if isinstance(container_obj, dict):
                    if key in container_obj:
                        del container_obj[key]
                        return None
                    else:
                        raise Exception(f"Key {key} not found in dictionary")
                elif isinstance(container_obj, list):
                    if not isinstance(key, int):
                        raise Exception(f"List index must be integer, got {type(key).__name__}")
                    try:
                        del container_obj[key]
                        return None
                    except IndexError:
                        raise Exception(f"List index {key} out of bounds")
                else:
                    raise Exception(f"Cannot delete from {type(container_obj).__name__}")

            else:
                raise Exception("Delete target must be an indexable expression")

        # Handle method calls: ['method_call', object_expr, method_name_token, args_list]
        if isinstance(expr, list) and len(expr) == 4 and expr[0] == "method_call":
            obj_val = self.get_value(self.evaluate(expr[1]))
            method_name_token = expr[2]
            args_exprs = expr[3]

            method_name = method_name_token.val if hasattr(method_name_token, 'val') else str(method_name_token)
            args = [self.get_value(self.evaluate(arg)) for arg in args_exprs]

            if isinstance(obj_val, list):
                if method_name == "push":
                    for arg in args:
                        obj_val.append(arg)
                    return obj_val

                elif method_name == "pop":
                    try:
                        if len(args) == 0:
                            return obj_val.pop()
                        elif len(args) == 1:
                            idx = args[0]
                            if not isinstance(idx, int):
                                raise Exception(f"pop index must be integer, got {type(idx).__name__}")
                            return obj_val.pop(idx)
                        else:
                            raise Exception("pop() takes at most one argument")
                    except IndexError:
                        raise Exception("pop from empty list")

                else:
                    raise Exception(f"Unknown method '{method_name}' for list")

            else:
                raise Exception(f"Cannot call method on {type(obj_val).__name__}")

        # Handle non-list expressions (tokens or native values)
        if not isinstance(expr, list):
            # If it's already a token, return it
            if hasattr(expr, "type") and hasattr(expr, "val"):
                return expr
            # If it's a native value, return it
            return expr

        # Handle token constructors like ['int', '123'], ['str', 'value'], etc.
        if isinstance(expr, list) and len(expr) == 2 and isinstance(expr[0], str):
            type_str = expr[0].lower()
            val = expr[1]

            if type_str == "int":
                return Integer(str(val))
            elif type_str == "flt":
                return Float(str(val))
            elif type_str == "bool_val":
                return BooleanValue(str(val).lower())
            elif type_str == "str":
                return String(val)

        # Handle unary operations: [op, operand]
        if isinstance(expr, list) and len(expr) == 2:
            op_token = expr[0]
            operand_expr = expr[1]

            # Skip if this looks like a constructor or other special form
            if isinstance(op_token, str) and op_token in ["int", "flt", "bool_val", "str", "list_literal", "dict_literal"]:
                pass  # Let it fall through to other handlers
            else:
                operand_token = self.evaluate(operand_expr)
                operand_val = self.get_value(operand_token)
                return self.compute_unary(op_token, operand_val)

        # Handle binary operations: [left, op, right]
        if isinstance(expr, list) and len(expr) == 3:
            left_expr, op_token, right_expr = expr

            left_token = self.evaluate(left_expr)
            right_token = self.evaluate(right_expr)
            right_val = self.get_value(right_token)

            return self.compute_binary(left_token, op_token, right_val)

        # Handle single element expressions (parentheses)
        if isinstance(expr, list) and len(expr) == 1:
            return self.evaluate(expr[0])

        raise Exception(f"Invalid expression format: {expr}")

    def interpret(self, tree=None):
        """Main interpretation entry point"""
        if tree is None:
            tree = self.tree
        return self.evaluate(tree)