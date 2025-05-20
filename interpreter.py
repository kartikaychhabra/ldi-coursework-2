from tokens import Float, Integer

class Interpreter: 

    def __init__(self, tree):
        self.tree = tree

    def read_int(self, val):
        return int(val)

    def read_flt(self, val):
        return float(val)
    
    def compute_binary(self, left, op, right):
        left_type = left.type 
        right_type = right.type

        left = getattr(self, f"read_{left_type}")(left.val)
        right = getattr(self, f"read_{right_type}")(right.val)

        if op.val == "+":
            output =  left + right
        elif op.val == "-":
            output = left - right 
        elif op.val == "*":
            output = left * right 
        elif op.val == "/":
            output = left / right 
        
        return Integer(output) if (left_type == "int" and right_type == "int") else Float(output)

    def interpret(self, tree=None):

        if tree is None:
            tree = self.tree
        # Post Order Traversal 

        #Left Subtree Evaluation    
        left_node = tree[0] 
        
        if isinstance(left_node, list):
            # using recursion 
            left_node = self.interpret(left_node)

        # Right Subtree Evaluation
        right_node = tree[2] 

        if isinstance(right_node, list): 
            right_node = self.interpret(right_node)

        operator = tree[1] # Root Node 

        return self.compute_binary(left_node, operator, right_node)