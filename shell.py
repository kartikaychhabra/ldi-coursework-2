from lexer import Lexer
from myparser import Parser
from interpreter import Interpreter

from data import Data 

base = Data()

while True:
    text = input("KayLang: ")

    tokenizer = Lexer(text)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    tree = parser.parse()   


    interpreter = Interpreter(tree, base)
    result = interpreter.interpret()

    if hasattr(result, "val"):
        print(result.val)
    else:
        print(result)
