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
println(y);
println(s);
println(b);

if (x > 0) {
    println("x больше 0");
} 


if (x < 20) {
    println("x меньше 20");
} else {
    println("x не меньше 20");
}

if (x > 5) {
    println("x больше 5");
} ifel (x > 15) {
    println("x больше 15");
} else {
    println("x равен 5 или меньше");
}

let x = 10;
while (x > 0) {
    println(x);
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
println("Факториал числа " + num + " равен: " + result); 
'''

try:
    tokens = my_lexer.my_lex(code)
    parser = MyParser(tokens)
    ast = parser.parse()

    interpreter = MyInterpreter(ast)
    interpreter.my_interpret()

except SyntaxError as e:
    print(f"SyntaxError: {e}")
