# Eye.py

import my_lexer
from my_parser import MyParser
from my_interpreter import MyInterpreter

code = '''
let x = 10;
fn add(a, b) {
    return a + b;
}
fn sub(a, b) {
    return a - b;
}
let y = add(x, 20) - sub(100, 50);
print(y);
'''

tokens = my_lexer.my_lex(code)
parser = MyParser(tokens)
ast = parser.parse()

interpreter = MyInterpreter(ast)
interpreter.my_interpret()
