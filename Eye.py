# Eye.py

import my_lexer
from my_parser import MyParser
from my_interpreter import MyInterpreter

code = '''
let x = 5;
while (x > 0) {
    println("Привет, мир!");
    let x = x - 1;
}
'''

try:
    tokens = my_lexer.my_lex(code)
    parser = MyParser(tokens)
    ast = parser.parse()

    interpreter = MyInterpreter(ast)
    interpreter.my_interpret()

except SyntaxError as e:
    print(f"SyntaxError: {e}")
