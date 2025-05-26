from lexer import Lexer
from myparser import Parser
from interpreter import Interpreter
from data import Data

import os

def execute_code(code, interpreter):
    tokenizer = Lexer(code)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    statements = parser.parse()  # parse_statements returns list of statements

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

# Global variable storage and interpreter setup
base = Data()
interpreter = Interpreter(None, base)

while True:
    try:
        text = input("KayLang: ").strip()

        # Run a file: e.g., run examples.kay
        if text.startswith("run "):
            filename = text[4:].strip().strip('"').strip("'")
            if not os.path.isfile(filename):
                print(f"File '{filename}' not found.")
                continue
            with open(filename, "r") as f:
                code = f.read()
                execute_code(code, interpreter)
            continue


        # Interactive mode
        execute_code(text, interpreter)

    except Exception as e:
        print(f"Error: {e}")
