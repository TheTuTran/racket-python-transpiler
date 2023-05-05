from lark import Lark, Tree
import os

racket_grammar = """
    start: expr

    ?expr: atom
         | "(" operation ")"
         | quoted_expr

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
             | racket_list
             | car
             | cdr
             | cons

    operator: MATH_OPERATOR
            | CONDITIONAL_OPERATOR

    define: "define" SYMBOL expr
    define_function: "define" "(" SYMBOL params? ")" expr
    lambda: "lambda" "(" params? ")" expr
    racket_if: "if" expr expr expr?
    racket_and: "and" expr+
    racket_or: "or" expr+
    racket_not: "not" expr
    racket_list: "list" expr*
    car: "car" expr
    cdr: "cdr" expr
    cons: "cons" expr expr
    quoted_expr: "'" list

    list: "(" expr* ")"
    params: SYMBOL*

    SYMBOL: /[a-zA-Z][_a-zA-Z0-9-]*/
    MATH_OPERATOR: "+" | "-" | "*" | "/"
    CONDITIONAL_OPERATOR: ">" | "<" | ">=" | "<=" | "=" | "!="
    NUMBER: /\-?\d+(\.\d+)?/
    STRING: /"[^"]*"/

    %import common.WS
    %ignore WS
"""

racket_parser = Lark(racket_grammar)

def translate_expr(x):
    return x[0]

def translate_atom(x):
    return x[0]

def translate_operation(x):
    operator = translate_to_python(x[0])
    args = [translate_to_python(arg) for arg in x[1:]]
    if len(args) == 2:
        return f"({args[0]} {operator} {args[1]})"
    else:
        return f"{operator}({', '.join(args)})"
    
def translate_define(x):
    return f"{x[0]} = {x[1]}"

def translate_define_function(x):
    func_name, params, body = x
    body_code = translate_to_python(body)
    return f"def {func_name}({', '.join(params)}):\n    return {body_code}"

def translate_lambda(x):
    return f"lambda {', '.join(x[0])}: {x[1]}"

def translate_racket_if(x):
    if len(x) == 3:
        return f"if {translate_to_python(x[0])}:\n    {translate_to_python(x[1])}\nelse:\n    {translate_to_python(x[2])}"
    else:
        return f"if {translate_to_python(x[0])}:\n    {translate_to_python(x[1])}"

def translate_STRING(x):
    return f'print({x[0]})'
    
def translate_racket_and(x):
    return f"({') and ('.join([translate_to_python(e) for e in x])})"

def translate_racket_or(x):
    return f"({') or ('.join([translate_to_python(e) for e in x])})"

def translate_racket_not(x):
    return f"not {translate_to_python(x[0])}"

def translate_racket_list(x):
    return f"[{', '.join([translate_to_python(e) for e in x])}]"

def translate_car(x):
    return f"({translate_to_python(x[0])})[0]"

def translate_cdr(x):
    return f"{translate_to_python(x[0])}[1:]"

def translate_cons(x):
    return f"[{translate_to_python(x[0])}] + {translate_to_python(x[1])}"

def translate_operator(x):
    return x[0]

def translate_MATH_OPERATOR(x):
    return x[0]

def translate_CONDITIONAL_OPERATOR(x):
    return x[0]

def translate_SYMBOL(x):
    return x[0]

def translate_NUMBER(x):
    return x[0]

def translate_params(x):
    return x

def translate_quoted_expr(x):
    return f"{translate_to_python(x[0])}"

def translate_list(x):
    return f"[{', '.join([translate_to_python(e) for e in x])}]"

translation_map = {
    "expr": translate_expr,
    "atom": translate_atom,
    "operation": translate_operation,
    "define": translate_define,
    "define_function": translate_define_function,
    "lambda": translate_lambda,
    "racket_if": translate_racket_if,
    "racket_and": translate_racket_and,
    "racket_or": translate_racket_or,
    "racket_not": translate_racket_not,
    "racket_list": translate_racket_list,
    "car": translate_car,
    "cdr": translate_cdr,
    "cons": translate_cons,
    "SYMBOL": translate_SYMBOL,
    "NUMBER": translate_NUMBER,
    "STRING": translate_STRING,
    "operator": translate_operator,
    "MATH_OPERATOR": translate_MATH_OPERATOR,
    "CONDITIONAL_OPERATOR": translate_CONDITIONAL_OPERATOR,
    "params": translate_params,
    "quoted_expr": translate_quoted_expr,
    "list": translate_list,
}

def translate_to_python(parsed_racket):
    if isinstance(parsed_racket, Tree):
        rule = parsed_racket.data
        if rule == 'start':
            return translate_to_python(parsed_racket.children[0])
        children = [translate_to_python(c) for c in parsed_racket.children]
        if rule in translation_map:
            return translation_map[rule](children)
        else:
            return f"Unknown rule: {rule}"
    else:  # Leaf or a Python list
        if hasattr(parsed_racket, 'type'):
            rule = parsed_racket.type
            value = parsed_racket.value
            if rule in translation_map:
                return translation_map[rule]([value])
            else:
                return f"Unknown rule: {rule}"
        elif isinstance(parsed_racket, list):
            if len(parsed_racket) == 1:
                return parsed_racket[0]  # Return the first element if there's only one
            else:
                return parsed_racket  # Otherwise, return the whole list
        elif isinstance(parsed_racket, str):
            return parsed_racket
        else:
            raise ValueError(f"Unsupported input type: {type(parsed_racket)}")

# Define a function to execute Racket code
def execute_racket(racket_code):
    parsed_racket = racket_parser.parse(racket_code)
    if parsed_racket:
        print("Parsed Racket code:")
        print(parsed_racket.pretty())
        python_code = translate_to_python(parsed_racket)
        if not python_code:
            print("Error: cannot execute this Racket code")
        else:
            python_code = python_code.replace("()", "")
            print("\nTranslated Python code:")
            print(python_code)

# Define a function to read and execute a Racket file
def execute_racket_file(filename):
    print(f"Executing {filename}...")
    with open(filename, "r") as f:
        contents = f.read()
        execute_racket(contents)

# Define a function to display a list of available tezt files with racket commands
def display_files():
    print("Available Files to Test:")
    for filename in os.listdir("."):
        if filename.endswith(".rkt"):
            print(filename)

def run_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                print(f"\nRunning line: {line.strip()}")
                try:
                    execute_racket(line.strip())
                except Exception as e:
                    print(f"Error running line: {e}")

if __name__ == '__main__':
    while True:
        try:
            command = input("Enter Racket code, type 'FILES' to see all sample files to test parser, or type 'STOP' to exit: ")
            if command.upper() == "STOP":
                break
            elif command.upper() == "FILES":
                display_files()
            elif command.upper().endswith(".RKT"):
                filename = command.strip()
                if os.path.isfile(filename):
                    run_file(filename)
                else:
                    print("File not found.")
            else:
                execute_racket(command)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print("An error occurred:", str(e))
