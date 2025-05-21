from lexer import Lexer
from myparser import Parser
from interpreter import Interpreter
from data import Data 

base = Data()  # Persistent global variable storage

interpreter = Interpreter(None, base)  # Create interpreter once and reuse it

while True:
    text = input("KayLang: ")

    tokenizer = Lexer(text)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    statements = parser.parse()  # parse_statements returns list of statements

    interpreter = Interpreter(None, base)

    for stmt in statements:
        interpreter.tree = stmt
        result = interpreter.interpret()

        # Skip printing for assignments (e.g. [var, '=', expr])
        if isinstance(stmt, list) and len(stmt) == 3 and hasattr(stmt[1], "val") and stmt[1].val == "=":
            continue

        # Skip printing if result is None (e.g. print statements)
        if result is None:
            continue

        if hasattr(result, "val"):
            print(result.val)
        else:
            print(result)
