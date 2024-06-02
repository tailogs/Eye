# my_parser.py

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
        node = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] in ('+', '-'):
            op = self.tokens[self.pos][1]
            self.pos += 1
            node = (op, node, self.term())
        return node
    
    def term(self):
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][1] in ('*', '/'):
            op = self.tokens[self.pos][1]
            self.pos += 1
            node = (op, node, self.factor())
        return node
    
    def factor(self):
        token = self.tokens[self.pos]
        if token[0] == 'NUMBER':
            self.pos += 1
            return ('num', token[1])
        elif token[0] == 'IDENT':
            if self.pos + 1 < len(self.tokens) and self.tokens[self.pos + 1][1] == '(':
                return self.call()
            self.pos += 1
            return ('ident', token[1])
        elif token[1] == '(':
            self.pos += 1
            node = self.expr()
            self.expect('PAREN')
            return node
        else:
            raise SyntaxError(f"Unexpected token {token}")
    
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
            raise SyntaxError(f"Expected {token_type} but got {token}")
        self.pos += 1
        return token[1]
