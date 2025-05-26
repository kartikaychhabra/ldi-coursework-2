KayLang Usage Guide

KayLang is a dynamically typed, interpreted programming language built for the 6CC509 coursework. It supports arithmetic operations, boolean logic, strings, global variables, control flow (if/else, while loops), lists, and dictionaries. This guide will explain how to use the KayLang interpreter.

How to Use:

Ensure the project is set up as described in BUILD.txt (clone from GitHub, ensure Python 3.8+ is installed).

Start the interactive REPL by running: python3 shell.py

In the shell, type KayLang commands and press Enter. Examples:

Arithmetic: 2 + 3 * 4 (outputs 14)

Boolean: true and (5 < 10) (outputs true)

Strings: "hello" + " world" (outputs hello world)

Variables: x = 5; x = x + 1; print x (outputs 6)

Control Flow: if (x > 3) { print "large"; } (outputs large)

Lists: lst = [1, 2]; lst.push(3); print lst[0] (outputs 1)

Dictionaries: dict = {a: 1}; dict[b] = 2; print dict (outputs {'a': 1, 'b': 2})


To run a complete program, use the provided example files in the folder "Examples":

To run a script, run this command in the terminal after running python shell.py, run this command to run the example: run "E:\LDI A2\Examples\stage6.txt" , change the file name as required from stage1 to stage6. 

Supported Features

1. Arithmetic: Addition (+), subtraction (-), multiplication (*), division (/), parentheses, unary negation (-).

2. Boolean Logic: Comparisons (==, !=, <, >, <=, >=), logical operators (and, or, not, !).

3. Strings: Concatenation (+), equality (==, !=), escape sequences (\n, \t, ").

4. Global Variables: Create, read, update, and print variables (e.g., x = 5; print x).

5. Control Flow: If/else statements, while loops (e.g., while (x < 5) { x = x + 1; }).

6. Lists: Create ([1, 2]), index access (lst[0]), push (lstWAR lst.push(3)), pop (lst.pop()), delete (delete lst[0]).

7. Dictionaries: Create ({a: 1}), query (dict[a]), delete (delete dict[a]).


Example File 

The kaylang_example.kay file includes a complete program showcasing all features:

1. Arithmetic operations (e.g., 1 - 2, (10 * 2) / 6).

2. Boolean expressions (e.g., true != false, (0 < 1) or false).

3. String operations (e.g., "hello" + " world").

4. Variable assignments (e.g., quickMaths = 10; quickMaths = quickMaths + 2).

5. Control flow (if and while loops).

6. List and dictionary operations (e.g., lst.push(4), dict[c] = 3). Run it with: python3 shell.py kaylang_example.kay

Limitations 

1. No support for user-defined functions or local variables
2. No input reading function 

NOTE 

1. Ensure all source files (data.py, interpreter.py, lexer.py, myparser.py, shell.py, tokens.py) are in the same directory.
2. Refer to BUILD.txt for setup.