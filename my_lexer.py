# my_lexer.py

import re

# Определение типов токенов
TOKEN_SPECIFICATION = [
    ('NUMBER',   r'\d+(\.\d*)?'),  # Числа
    ('IDENT',    r'[A-Za-z_]\w*'), # Идентификаторы
    ('OP',       r'[+\-*/=]'),     # Операторы
    ('PAREN',    r'[()]'),         # Скобки
    ('BRACE',    r'[{}]'),         # Фигурные скобки
    ('COMMA',    r','),            # Запятая
    ('SEMICOL',  r';'),            # Точка с запятой
    ('SKIP',     r'[ \t]+'),       # Пропуск пробелов и табуляций
    ('NEWLINE',  r'\n'),           # Новая строка
    ('MISMATCH', r'.'),            # Остальные символы
]

# Ключевые слова
KEYWORDS = {'fn', 'let', 'if', 'else', 'while', 'for', 'return', 'int', 'float', 'bool', 'string', 'print'}

# Регулярное выражение для разбора токенов
token_re = re.compile('|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION))

# Лексический анализатор
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
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        tokens.append((kind, value, line_num, column))
    return tokens
