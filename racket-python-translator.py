import sys
from lark import Lark, UnexpectedInput, Transformer, v_args

racket_grammar = """
    start: expr

    ?expr: atom
         | "(" operation ")"

    atom: SYMBOL
        | NUMBER
        | STRING

    operation: operator expr+
             | define
             | define_function
             | lambda
             | racket_if
             | racket_and
             | racket_or
             | racket_not
             | racket_let
             | racket_list
             | car
             | cdr
             | cons

    operator: OPERATOR
            | CONDITIONAL_OPERATOR

    define: "define" SYMBOL expr
    define_function: "define" "(" SYMBOL params? ")" expr
    lambda: "lambda" "(" params? ")" expr
    racket_if: "if" expr expr expr?
    racket_and: "and" expr+
    racket_or: "or" expr+
    racket_not: "not" expr
    racket_let: "let" "(" (SYMBOL expr)+ ")" expr
    racket_list: "list" expr*
    car: "car" expr
    cdr: "cdr" expr
    cons: "cons" expr expr

    params: SYMBOL*

    SYMBOL: /[a-zA-Z][_a-zA-Z0-9-]*/
    OPERATOR: "+" | "-" | "*" | "/"
    CONDITIONAL_OPERATOR: ">" | "<" | ">=" | "<=" | "=" | "!="
    NUMBER: /\-?\d+(\.\d+)?/
    STRING: /"[^"]*"/

    %import common.WS
    %ignore WS
"""

racket_parser = Lark(racket_grammar)

class RacketToPythonTransformer(Transformer):
    def expr(self, x):
        return x[0]

    def atom(self, x):
        return x[0]

    def operation(self, x):
        return x

    def SYMBOL(self, x):
        return x[0]

    def NUMBER(self, x):
        return x[0]

    def STRING(self, x):
        return x[0]

    def operator(self, x):
        return x[0]

    def define(self, x):
        return f"{x[0]} = {x[1]}"

    def define_function(self, x):
        return f"def {x[0]}({', '.join(x[1])}):\n    return {x[2]}"

    def lambda_(self, x):
        return f"lambda {', '.join(x[0])}: {x[1]}"

    def racket_if(self, x):
        if len(x) == 3:
            return f"{x[1]} if {x[0]} else {x[2]}"
        else:
            return f"{x[1]} if {x[0]} else None"

    def racket_and(self, x):
        return f"({') and ('.join(x)})"

    def racket_or(self, x):
        return f"({') or ('.join(x)})"

    def racket_not(self, x):
        return f"not {x[0]}"

    def racket_let(self, x):
        assignments = "\n".join([f"{var} = {val}" for var, val in x[0]])
        return f"{assignments}\n{x[1]}"

    def racket_list(self, x):
        return f"[{', '.join(x)}]"

    def car(self, x):
        return f"{x[0]}[0]"

    def cdr(self, x):
        return f"{x[0]}[1:]"

    def cons(self, x):
        return f"[{x[0]}] + {x[1]}"

transformer = RacketToPythonTransformer()

def translate_to_python(parsed_racket):
    python_ast = transformer.transform(parsed_racket)
    return python_ast

if __name__ == '__main__':
    while True:
        try:
            racket_code = input("Enter Racket code or type 'STOP' to exit: ")
            if racket_code.upper() == "STOP":
                break
            parsed_racket = racket_parser.parse(racket_code)
            if parsed_racket:
                print("Parsed Racket code:")
                print(parsed_racket.pretty())
                python_code = translate_to_python(parsed_racket)
                print("\nTranslated Python code:")
                print(python_code)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print("An error occurred:", str(e))