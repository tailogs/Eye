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

if (x > 11) {
    print("x больше 0");
} else {}


if (x < 20) {
    print("x меньше 20");
} else {
    print("x не меньше 20");
}

if (x > 5) {
    print("x больше 5");
} ifel (x > 15) {
    print("x больше 15");
} else {
    print("x равен 5 или меньше");
}

let x = 10;
while (x > 0) {
    print(x);
    let x = x - 1;
}
'''

factorial = '''
fn factorial(n) {
    if (n == 0) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

let num = 5;
let result = factorial(num);
print("Факториал числа " + num + " равен: " + result); 
'''

try:
    tokens = my_lexer.my_lex(code)
    parser = MyParser(tokens)
    ast = parser.parse()

    interpreter = MyInterpreter(ast)
    interpreter.my_interpret()

except SyntaxError as e:
    print(f"SyntaxError: {e}")
