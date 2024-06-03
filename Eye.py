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
~ Определяем функцию factorial для вычисления факториала числа n
fn factorial(n) {
    if (n == 0) {
        return 1; ~ Если n равно 0, возвращаем 1 (базовый случай рекурсии)
    } else {
        return n * factorial(n - 1); ~ Иначе возвращаем произведение n на факториал (n - 1) (рекурсивный случай)
    }
}

let num = 5; ~ Определяем переменную num и присваиваем ей значение 5

let result = factorial(num); ~ Вызываем функцию factorial с аргументом num и сохраняем результат в переменную result

println("Факториал числа " + num + " равен: " + result); ~ Выводим на экран сообщение о значении факториала числа num
'''

array = '''
let array = [1, 2, 3, 4, 5];
println(array);
'''

try:
    tokens = my_lexer.my_lex(array)
    parser = MyParser(tokens)
    ast = parser.parse()

    interpreter = MyInterpreter(ast)
    interpreter.my_interpret()

except SyntaxError as e:
    print(f"SyntaxError: {e}")
