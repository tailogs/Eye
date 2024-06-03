import re

# Token specifications
TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+(\.\d*)?'),     # Numbers
    ('STRING',   r'\"([^\\\n]|(\\.))*?\"'),  # Strings in double quotes
    ('BOOLEAN',  r'true|false'),      # Boolean values
    ('IDENT',    r'[A-Za-z_]\w*'),    # Identifiers
    ('OP',       r'==|!=|<=|>=|<|>|//|\|\||&&|[+\-*/%=]'),  # Operators
    ('PAREN',    r'[()]'),            # Parentheses
    ('BRACE',    r'[{}]'),            # Braces
    ('COMMA',    r','),               # Comma
    ('SEMICOL',  r';'),               # Semicolon
    ('SKIP',     r'[ \t]+'),          # Skip spaces and tabs
    ('NEWLINE',  r'\n'),              # Newline
    ('MISMATCH', r'.'),               # Any other character
]

# Keywords
KEYWORDS = {'fn', 'let', 'if', 'else', 'while', 'for', 'return', 'int', 'float', 'bool', 'string', 'print', 'println', 'and', 'or', 'not', 'ifel'}

# Regular expression for tokenizing
token_re = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION))

# Lexical analyzer
def my_lex(code):
    line_num = 1
    line_start = 0
    tokens = []
    for mo in token_re.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'IDENT' and value in KEYWORDS:
            kind = 'KEYWORD'
        elif kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected token: {value} at line {line_num}')
        tokens.append((kind, value, line_num, column))
    return tokens
