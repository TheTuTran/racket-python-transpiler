import sys
from lark import Lark, UnexpectedInput, Transformer, v_args

racket_grammar = """
    start: expr

    ?expr: atom
         | list

    atom: SYMBOL
        | NUMBER
        | OPERATOR
        | STRING

    list: "(" _expr_inner+ ")"

    _expr_inner: expr
               | define
               | lambda
               | cond
               | racket_displayln
               | racket_list
               | racket_if
               | racket_null
               | racket_let

    define: "define" "(" SYMBOL expr+ ")"
    lambda: "lambda" "(" SYMBOL* ")" expr
    cond: "cond" "(" _cond_inner+ ")"

    _cond_inner: "(" expr ":" expr ")"

    car: "car" expr
    cdr: "cdr" expr
    cons: "cons" expr expr

    racket_displayln: "displayln" expr
    racket_list: "list" expr*
    racket_if: "if" expr expr expr?

    racket_null: "null?" expr
    racket_let: "let" "(" (SYMBOL expr)+ ")" expr

    SYMBOL: /[a-zA-Z][_a-zA-Z0-9-]*/
    NUMBER: /\-?\d+(\.\d+)?/
    OPERATOR: "+" | "-" | "*" | "/"
    STRING: /"[^"]*"/

    %import common.WS
    %ignore WS
"""


lark_parser = Lark(racket_grammar, start='start')

class RacketToPythonTransformer(Transformer):
    @v_args(inline=True)
    def expr(self, x):
        return x

    def atom(self, x):
        return x[0]

    def list(self, x):
        return x

    def SYMBOL(self, x):
        return x[0]

    def NUMBER(self, x):
        return x[0]

def parse_racket(racket_code):
    try:
        parsed_racket = lark_parser.parse(racket_code)
    except UnexpectedInput as e:
        print("An exception occurred: Unrecognized terminal")
        print("Context:", e.get_context(racket_code))
    except Exception as e:
        print("An exception occurred:", str(e))
    else:
        return parsed_racket

def translate_to_python(parsed_racket):
    tree = lark_parser.parse(parsed_racket)
    transformer = RacketToPythonTransformer()
    python_ast = transformer.transform(tree)
    return python_ast

if __name__ == '__main__':
    while True:
        try:
            racket_code = input("Enter Racket code or type 'STOP' to exit: ")
            if racket_code.upper() == "STOP":
                break
            parsed_racket = parse_racket(racket_code)
            if parsed_racket:
                print(parsed_racket.pretty())
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print("An error occurred:", str(e))