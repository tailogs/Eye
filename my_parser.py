# my_parser.py

from my_lexer import KEYWORDS
from console.ConsoleColors import ConsoleColors

class MyParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self):
        return self.program()
    
    def program(self):
        statements = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] != '}':
            statements.append(self.statement())
        return statements
        
    def statement(self):
        token = self.tokens[self.pos]
        if token[1] == 'let':
            return self.let_statement()
        elif token[1] == 'fn':
            return self.fn_statement()
        elif token[1] == 'return':
            return self.return_statement()
        elif token[1] == 'print':
            return self.print_statement()
        elif token[1] == 'println':  # Обработка println
            return self.println_statement()
        elif token[1] == 'if':
            return self.if_statement()
        elif token[1] == 'ifel':
            return self.ifel_statement()
        elif token[1] == 'else':
            return self.else_statement()
        elif token[1] == 'while':
            return self.while_statement()  
        else:
            return self.expr_statement()

    def let_statement(self):
        self.expect('KEYWORD')
        ident = self.expect('IDENT')
        self.expect('OP')
        expr = self.expr()
        self.expect('SEMICOL')
        return ('let', ident, expr)
    
    def fn_statement(self):
        self.expect('KEYWORD')
        ident = self.expect('IDENT')
        self.expect('PAREN')
        params = self.params()
        self.expect('PAREN')
        self.expect('BRACE')
        body = self.program()
        self.expect('BRACE')
        return ('fn', ident, params, body)
    
    def return_statement(self):
        self.expect('KEYWORD')
        expr = self.expr()
        self.expect('SEMICOL')
        return ('return', expr)
    
    def print_statement(self):
        self.expect('KEYWORD')
        expr = self.expr()
        self.expect('SEMICOL')
        return ('print', expr)

    def println_statement(self):  # Метод для обработки println
        self.expect('KEYWORD')
        expr = self.expr()
        self.expect('SEMICOL')
        return ('println', expr)

    def if_statement(self):
        self.expect('KEYWORD')
        self.expect('PAREN')
        condition = self.expr()
        self.expect('PAREN')
        self.expect('BRACE')
        then_branch = self.program()
        self.expect('BRACE')
        else_branch = None  # Убрали ожидание `else` здесь
        if self.pos < len(self.tokens) and self.tokens[self.pos][1] == 'else':
            self.expect('KEYWORD')
            self.expect('BRACE')
            else_branch = self.program()
            self.expect('BRACE')
        return ('if', condition, then_branch, else_branch if else_branch else [])

    def ifel_statement(self):
        ifel_branches = []
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] == 'ifel':
            self.expect('KEYWORD')
            self.expect('PAREN')
            condition = self.expr()
            self.expect('PAREN')
            self.expect('BRACE')
            then_branch = self.program()
            self.expect('BRACE')
            ifel_branches.append((condition, then_branch))
        else_branch = None  # Убрали ожидание `else` здесь
        if self.pos < len(self.tokens) and self.tokens[self.pos][1] == 'else':
            self.expect('KEYWORD')
            self.expect('BRACE')
            else_branch = self.program()
            self.expect('BRACE')
        return ('ifel', ifel_branches, else_branch if else_branch else [])

    def else_statement(self):
        self.expect('KEYWORD')  
        self.expect('BRACE')  
        else_branch = self.program()
        self.expect('BRACE')  
        
        if self.pos < len(self.tokens) and self.tokens[self.pos][1] == 'else':
            raise SyntaxError(f"{ConsoleColors.Text.RED}Unexpected 'else' after 'else' at line {self.tokens[self.pos][2]}, column {self.tokens[self.pos][3]}{ConsoleColors.RESET}")
        
        return ('else', else_branch)

    def while_statement(self):
        self.expect('KEYWORD')  
        self.expect('PAREN')    
        condition = self.expr()
        self.expect('PAREN')    
        self.expect('BRACE')    
        body = self.program()
        self.expect('BRACE')    
        return ('while', condition, body)

    def array_literal(self):
        self.expect('LBRACKET')
        elements = []
        if self.tokens[self.pos][1] != ']':
            elements.append(self.expr())
            while self.tokens[self.pos][1] == ',':
                self.pos += 1
                elements.append(self.expr())
        self.expect('RBRACKET')
        return ('array', elements)

    def expr_statement(self):
        expr = self.expr()
        self.expect('SEMICOL')
        return expr
    
    def params(self):
        params = []
        if self.tokens[self.pos][0] == 'IDENT':
            params.append(self.tokens[self.pos][1])
            self.pos += 1
            while self.tokens[self.pos][0] == 'COMMA':
                self.pos += 1
                params.append(self.tokens[self.pos][1])
                self.pos += 1
        return params
    
    def expr(self):
        node = self.logic_or()
        return node
    
    def logic_or(self):
        node = self.logic_and()
        while self.pos < len(self.tokens) and (self.tokens[self.pos][1] == '||' or self.tokens[self.pos][0] == 'OR' or self.tokens[self.pos][1] == 'or'):
            op = self.tokens[self.pos][1]
            self.pos += 1
            node = ('or', node, self.logic_and())
        return node

    def logic_and(self):
        node = self.equality()
        while self.pos < len(self.tokens) and (self.tokens[self.pos][1] == '&&' or self.tokens[self.pos][0] == 'AND' or self.tokens[self.pos][1] == 'and'):
            op = self.tokens[self.pos][1]
            self.pos += 1
            node = ('and', node, self.equality())
        return node
    
    def equality(self):
        node = self.comparison()
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] in ('==', '!='):
            op = self.tokens[self.pos][1]
            self.pos += 1
            node = (op, node, self.comparison())
        return node
    
    def comparison(self):
        node = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] in ('<', '>', '<=', '>='):
            op = self.tokens[self.pos][1]
            self.pos += 1
            node = (op, node, self.term())
        return node
    
    def term(self):
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] in ('+', '-', '*', '/', '%', '//'):
            op = self.tokens[self.pos][1]
            self.pos += 1
            node = (op, node, self.factor())
        return node

    def factor(self):
        token = self.tokens[self.pos]
        if token[0] == 'NUMBER':
            self.pos += 1
            return ('num', token[1])
        elif token[0] == 'STRING':
            self.pos += 1
            return ('string', token[1][1:-1])  # Удаляем кавычки вокруг строки
        elif token[0] == 'BOOLEAN':
            self.pos += 1
            return ('bool', token[1] == 'true')
        elif token[0] == 'IDENT':
            if token[1] == 'read':
                return self.read_expr()  # Handle read() function call
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][1] == '(':
                return self.call()
            self.pos += 1
            return ('ident', token[1])
        elif token[0] == 'LBRACKET':
            return self.array_literal()
        elif token[1] == 'get_element':
            return self.get_element_expr()
        elif token[1] == 'set_element':
            return self.set_element_expr()
        elif token[1] == '(':
            self.pos += 1
            node = self.expr()
            self.expect('PAREN')
            return node
        elif token[0] == 'NOT' or token[1] == 'not':
            self.pos += 1
            return ('not', self.factor())
        elif token[0] == 'AND' or token[1] == 'and':
            self.pos += 1
            return ('and', self.logic_or(), self.factor())  # Обновление здесь
        elif token[0] == 'OR' or token[1] == 'or':
            self.pos += 1
            return ('or', self.logic_and(), self.factor())  # Обновление здесь
        else:
            raise SyntaxError(f"{ConsoleColors.Text.RED}Unexpected token {token}{ConsoleColors.RESET}")

    def read_expr(self):
        self.pos += 1  # Пропускаем 'read'
        self.expect('PAREN')
        if self.tokens[self.pos][1] == ')':
            self.expect('PAREN')
            return ('call', 'read', [])
        else:
            prompt = self.expr()
            self.expect('PAREN')
            return ('call', 'read', [prompt])
    
    def get_element_expr(self):
        self.pos += 1  # Пропускаем 'get_element'
        self.expect('PAREN')
        array = self.expr()
        self.expect('COMMA')
        index = self.expr()
        self.expect('PAREN')
        return ('get_element', array, index)
    
    def set_element_expr(self):
        self.pos += 1  # Пропускаем 'set_element'
        self.expect('PAREN')
        array = self.expr()
        self.expect('COMMA')
        index = self.expr()
        self.expect('COMMA')
        value = self.expr()
        self.expect('PAREN')
        return ('set_element', array, index, value)
    
    def index_expr(self):
        array_name = self.expect('IDENT')
        self.expect('LBRACKET')
        index = self.expr()
        self.expect('RBRACKET')
        return ('index', array_name, index)
    
    def call(self):
        ident = self.expect('IDENT')
        self.expect('PAREN')
        args = []
        if self.tokens[self.pos][1] != ')':
            args.append(self.expr())
            while self.tokens[self.pos][1] == ',':
                self.pos += 1
                args.append(self.expr())
        self.expect('PAREN')
        return ('call', ident, args)
    
    def expect(self, token_type):
        token = self.tokens[self.pos]
        if token[0] != token_type:
            raise SyntaxError(f"{ConsoleColors.Text.RED}Expected {token_type} but got {token[0]} '{token[1]}' at line {token[2] - 1}, column {token[3]}{ConsoleColors.RESET}")
        self.pos += 1
        return token[1]
