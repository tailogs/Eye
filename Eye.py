import argparse
import os
import my_lexer
from my_parser import MyParser
from my_interpreter import MyInterpreter
from console.ConsoleColors import ConsoleColors

class EyeInterpreterError(Exception):
    pass

def main():
    try:
        ConsoleColors.console_colors_init()
        parser = argparse.ArgumentParser(description="Eye Interpreter")
        parser.add_argument("filename", nargs="?", help="The Eye source file to interpret")
        args = parser.parse_args()

        if not args.filename:
            raise EyeInterpreterError(f"{ConsoleColors.Text.RED}No input file provided. Usage: python Eye.py <filename.eye>{ConsoleColors.RESET}")

        if not args.filename.endswith('.eye'):
            raise EyeInterpreterError(f"{ConsoleColors.Text.RED}The input file must have a .eye extension.{ConsoleColors.RESET}")

        if not os.path.isfile(args.filename):
            raise EyeInterpreterError(f"{ConsoleColors.Text.RED}The file '{args.filename}' does not exist.{ConsoleColors.RESET}")

        with open("standard_library.eye", 'r', encoding='utf-8') as file:
            standard_library = file.read()

        with open(args.filename, 'r', encoding='utf-8') as file:
            code = file.read()

        tokens = my_lexer.my_lex(standard_library + code)
        parser = MyParser(tokens)
        ast = parser.parse()

        interpreter = MyInterpreter(ast)
        interpreter.my_interpret()

    except EyeInterpreterError as e:
        print(f"Error: {ConsoleColors.Text.RED}{e}{ConsoleColors.RESET}")
    except SyntaxError as e:
        print(f"SyntaxError: {ConsoleColors.Text.RED}{e}{ConsoleColors.RESET}")
    except Exception as e:
        print(f"Error: {ConsoleColors.Text.RED}{e}{ConsoleColors.RESET}")


if __name__ == "__main__":
    main()
