from tokens import Integer, Float

class Interpreter: 

    def __init__(self, tree):
        self.tree = tree

    def read_int(self, val):
        return int(val)

    def read_flt(self, val):
        return float(val)
    
    def compute_binary(self, left, op, right):
        # Wrap if needed
        left = self.wrap_token(left)
        right = self.wrap_token(right)

        left_val = getattr(self, f"read_{left.type}")(left.val)
        right_val = getattr(self, f"read_{right.type}")(right.val)

        if op.val == "+":
            output = left_val + right_val
        elif op.val == "-":
            output = left_val - right_val
        elif op.val == "*":
            output = left_val * right_val
        elif op.val == "/":
            output = left_val / right_val
        else:
            raise Exception(f"Unknown operator {op.val}")

        if isinstance(output, float) and output.is_integer():
            output = int(output)

        return Integer(str(output)) if isinstance(output, int) else Float(str(output))

    def wrap_token(self, val):
        if hasattr(val, "type") and hasattr(val, "val"):
            return val
        # Wrap raw int or float in Token
        if isinstance(val, int):
            return Integer(str(val))
        elif isinstance(val, float):
            return Float(str(val))
        else:
            raise Exception(f"Cannot wrap value {val}")

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree

        # Unary minus case: [op, node]
        if isinstance(tree, list) and len(tree) == 2 and tree[0].val == "-":
            node = tree[1]
            val = self.interpret(node) if isinstance(node, list) else node
            val = self.wrap_token(val)
            val_num = getattr(self, f"read_{val.type}")(val.val)
            result = -val_num
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            return Integer(str(result)) if isinstance(result, int) else Float(str(result))

        # Leaf node token
        if not isinstance(tree, list):
            return tree

        # Binary operation: [left, op, right]
        left = self.interpret(tree[0]) if isinstance(tree[0], list) else tree[0]
        right = self.interpret(tree[2]) if isinstance(tree[2], list) else tree[2]
        op = tree[1]

        return self.compute_binary(left, op, right)
