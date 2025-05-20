from lexer import Lexer
from myparser import Parser

while True:
    text = input("KayLang: ")

    tokenizer = Lexer(text)
    tokens = tokenizer.tokenize()

    parser = Parser(tokens)
    tree = parser.parse()

    print(tree)