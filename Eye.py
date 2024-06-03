# Eye.py

import my_lexer
from my_parser import MyParser
from my_interpreter import MyInterpreter

code = '''
let x = 10;
let s = "Hello, world!";
let b = true;
fn add(a, b) {
    return a + b;
}
let y = add(x, 20);
print(y);
print(s);
print(b);

if (x < 20) {
    print("x is less than 20");
} else {
    print("x is not less than 20");
}

if (x > 5) {
    print("x is greater than 5");
} ifel (x > 15) {
    print("x is greater than 15");
} else {
    print("x is 5 or less");
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
