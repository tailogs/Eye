# my_interpreter.py

class MyInterpreter:
    def __init__(self, ast):
        self.ast = ast
        self.global_env = {}

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
            elif node[0] == 'fn':
                _, name, params, body = node
                env[name] = ('fn', params, body, env)
            elif node[0] == 'return':
                _, expr = node
                return self.evaluate(expr, env)
            elif node[0] in {'+', '-', '*', '/'}:
                op, left, right = node
                left_val = self.evaluate(left, env)
                right_val = self.evaluate(right, env)
                if op == '+':
                    return left_val + right_val
                elif op == '-':
                    return left_val - right_val
                elif op == '*':
                    return left_val * right_val
                elif op == '/':
                    return left_val / right_val
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
                print(self.evaluate(expr, env))
        elif isinstance(node, str):
            return env[node]
        else:
            raise ValueError(f"Unknown node type: {node}")

    def call_function(self, fn, args, env):
        _, params, body, fn_env = fn
        local_env = fn_env.copy()
        local_env.update(zip(params, args))
        return self.evaluate(body, local_env)