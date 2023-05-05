# Racket to Python Transpiler

This is a program that can translate Racket code into Python code. It includes a parser that can convert Racket syntax into an abstract syntax tree (AST), and a set of translation rules that can convert the AST into equivalent Python code.

## Usage

You have to have python and Lark installed onto your computer. To use the program, simply run the `racket-python-transpiler.py` script and enter Racket code at the prompt. The program will then display the parsed Racket code and the equivalent Python code.

There are also sample racket files with some basic racket commands that can be ranned after running the python script. Simply type FILES, and a list of sample racket files will be printed. Type the name of one of the files including .rkt, and the script will attempt to run each line on the sample program.

## Racket Syntax

The Racket syntax supported by the parser includes:

- List constructor (List)
- List manipulation (cons, car, cdr)
- Basic arithmetic operations (+, -, *, /)
- Comparison operators (> , <, >=, <=, =, !=)
- Boolean operators (and, or, not)
- Conditional statements (if)
- Function definitions (define and lambda)

## Translation Rules

The translation rules convert the Racket syntax into equivalent Python syntax. Some of the translation rules are:

- Arithmetic operations are translated to equivalent Python operators (+, -, *, /)
- Comparison operators are translated to equivalent Python operators (> , <, >=, <=, ==, !=)
- Boolean operators are translated to equivalent Python operators (and, or, not)
- Conditional statements are translated to equivalent Python if/else statements
- Function definitions are translated to equivalent Python function definitions

## Contributing

Contributions are welcome! Feel free to submit bug reports, feature requests, or pull requests on GitHub.

## Known Bugs

There may be some syntax errors like simply typing in random characters into the search bar will still give you a tree and translated python code, even though it isn't racket code. The program is limited to Racket Syntax listed above. 
