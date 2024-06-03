# my_interpreter.py

import sys

class MyInterpreter:
    def __init__(self, ast):
        self.ast = ast
        self.global_env = {
            'get_element': ('builtin', self.get_element),
            'set_element': ('builtin', self.set_element),
            'remove_element': ('builtin', self.remove_element),
            'append_element': ('builtin', self.append_element),
            'get_range': ('builtin', self.get_range),
            'length': ('builtin', self.length),
            'to_string': ('builtin', self.to_string),
            'to_integer': ('builtin', self.to_integer),
            'to_float': ('builtin', self.to_float),
            'to_boolean': ('builtin', self.to_boolean),
            'substring': ('builtin', self.substring),
            'string_length': ('builtin', self.string_length),
            'compare_strings': ('builtin', self.compare_strings),
            'find_substring': ('builtin', self.find_substring),
            'get_char_at': ('builtin', self.get_char_at),
            'to_uppercase': ('builtin', self.to_uppercase),
            'to_lowercase': ('builtin', self.to_lowercase),
            'replace_substring': ('builtin', self.replace_substring),
            'split_string': ('builtin', self.split_string),
            'delete': ('builtin', self.delete)
        }

    def my_interpret(self):
        return self.evaluate(self.ast, self.global_env)

    def evaluate(self, node, env):
        if isinstance(node, list):
            result = None
            for stmt in node:
                result = self.evaluate(stmt, env)
            return result
        elif isinstance(node, tuple):
            if node[0] == 'let':
                _, name, expr = node
                env[name] = self.evaluate(expr, env)
            elif node[0] == 'array':
                return [self.evaluate(elem, env) for elem in node[1]]
            elif node[0] == 'index':
                array_name, index_expr = node[1], node[2]
                array = env[array_name]
                index = self.evaluate(index_expr, env)
                return array[index]
            elif node[0] == 'assign_index':
                array_name, index_expr, value_expr = node[1], node[2], node[3]
                array = env[array_name]
                index = self.evaluate(index_expr, env)
                value = self.evaluate(value_expr, env)
                array[index] = value
                return None
            elif node[0] == 'fn':
                _, name, params, body = node
                env[name] = ('fn', params, body, env)
            elif node[0] == 'return':
                _, expr = node
                return self.evaluate(expr, env)
            elif node[0] in {'+', '-', '*', '/', '%', '//'}:
                op, left, right = node
                left_val = self.evaluate(left, env)
                right_val = self.evaluate(right, env)
                if op == '+':
                    if isinstance(left_val, str) or isinstance(right_val, str):
                        return str(left_val) + str(right_val)
                    else:
                        return left_val + right_val
                elif op == '-':
                    return left_val - right_val
                elif op == '*':
                    return left_val * right_val
                elif op == '/':
                    return left_val / right_val
                elif op == '%':
                    return left_val % right_val
                elif op == '//':
                    return left_val // right_val
            elif node[0] in {'<', '>', '<=', '>=', '==', '!='}:
                op, left, right = node
                left_val = self.evaluate(left, env)
                right_val = self.evaluate(right, env)
                if op == '<':
                    return left_val < right_val
                elif op == '>':
                    return left_val > right_val
                elif op == '<=':
                    return left_val <= right_val
                elif op == '>=':
                    return left_val >= right_val
                elif op == '==':
                    return left_val == right_val
                elif op == '!=':
                    return left_val != right_val
            elif node[0] in {'and', 'or'}:
                op, left, right = node
                left_val = self.evaluate(left, env)
                right_val = self.evaluate(right, env)
                if op == 'and':
                    return left_val and right_val
                elif op == 'or':
                    return left_val or right_val
            elif node[0] == 'not':
                _, expr = node
                return not self.evaluate(expr, env)
            elif node[0] == 'if':
                _, condition, then_branch, else_branch = node
                if self.evaluate(condition, env):
                    return self.evaluate(then_branch, env)
                elif else_branch:
                    return self.evaluate(else_branch, env)
            elif node[0] == 'ifel':
                _, ifel_branches, else_branch = node
                for condition, branch in ifel_branches:
                    if self.evaluate(condition, env):
                        return self.evaluate(branch, env)
                if else_branch:
                    return self.evaluate(else_branch, env)
            elif node[0] == 'while':
                _, condition, body = node
                while self.evaluate(condition, env):
                    self.evaluate(body, env)
            elif node[0] == 'num':
                return node[1]
            elif node[0] == 'string':
                return node[1]
            elif node[0] == 'bool':
                return node[1]
            elif node[0] == 'ident':
                return env[node[1]]
            elif node[0] == 'call':
                fn_name, args = node[1], node[2]
                fn = env[fn_name]
                arg_vals = [self.evaluate(arg, env) for arg in args]
                return self.call_function(fn, arg_vals, env)
            elif node[0] == 'print':
                _, expr = node
                self.print(self.evaluate(expr, env))
            elif node[0] == 'println':
                _, expr = node
                self.println(self.evaluate(expr, env))
            else:
                raise ValueError(f"Unknown node type: {node}")
        elif isinstance(node, str):
            return env[node]
        else:
            raise ValueError(f"Unknown node type: {node}")

    def call_function(self, fn, args, env):
        if fn[0] == 'builtin':
            return fn[1](*args)
        _, params, body, fn_env = fn
        local_env = fn_env.copy()
        local_env.update(zip(params, args))
        return self.evaluate(body, local_env)

    def println(self, *args):
        output = " ".join(str(arg) for arg in args)
        print(output)

    def print(self, *args):
        output = "".join(str(arg) for arg in args)
        print(output, end="")

    def get_element(self, array, index):
        return array[index]

    def set_element(self, array, index, value):
        array[index] = value
        return None

    def remove_element(self, array, index):
        return array.pop(index)

    def append_element(self, array, value):
        array.append(value)
        return None

    def get_range(self, array, start, end):
        return array[start:end]

    def length(self, obj):
        if isinstance(obj, str):
            return len(obj)
        elif isinstance(obj, list):
            return len(obj)
        elif isinstance(obj, (int, float, bool)):
            return sys.getsizeof(obj)  # Возвращаем размер в байтах
        else:
            raise ValueError(f"Length not supported for type: {type(obj)}")

    def to_string(self, value):
        return str(value)

    def to_integer(self, value):
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"Cannot convert {value} to integer")

    def to_float(self, value):
        try:
            return float(value)
        except ValueError:
            raise ValueError(f"Cannot convert {value} to float")

    def to_boolean(self, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in {'true', '1', 'yes'}
        if isinstance(value, (int, float)):
            return value != 0
        return bool(value)

    def substring(self, string, start, end=None):
        if end is None:
            return string[start:]
        else:
            return string[start:end]

    def string_length(self, string):
        return len(string)

    def compare_strings(self, str1, str2):
        if str1 == str2:
            return 0
        elif str1 < str2:
            return -1
        else:
            return 1

    def find_substring(self, string, substring):
        return string.find(substring)

    def get_char_at(self, string, index):
        return string[index]

    def to_uppercase(self, string):
        return string.upper()

    def to_lowercase(self, string):
        return string.lower()

    def replace_substring(self, string, old_substring, new_substring):
        return string.replace(old_substring, new_substring)

    def split_string(self, string, delimiter=None):
        if delimiter is None:
            return string.split()
        else:
            return string.split(delimiter)

    def delete(self, var_name):
        if var_name in self.global_env:
            del self.global_env[var_name]
        else:
            raise NameError(f"Variable '{var_name}' not found")