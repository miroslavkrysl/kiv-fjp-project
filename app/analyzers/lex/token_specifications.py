import re

# ##################################################
# Reserved keyword definitions
# ########################################


reserved = {
    # keyword: TOKEN
    'if': 'IF',
    'else': 'ELSE',

    'while': 'WHILE',
    'continue': 'CONTINUE',
    'break': 'BREAK',

    'function': 'FUNCTION',
    'return': 'RETURN',
 }


# ##################################################
# Simple token regex definitions
# ########################################


t_SEMICOLON = r'\;'
t_COMMA = r'\,'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_EQUAL = r'=='
t_NOT_EQUAL = r'!='
t_LESS = r'<'
t_GREATER = r'>'
t_LESS_OR_EQUAL = r'<='
t_GREATER_OR_EQUAL = r'>='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'


# ##################################################
# Advanced token regex definitions
# ########################################


def t_IDENTIFIER(t):
    r'[a-zA-Z]+[a-zA-Z0-9]*'
    t.value = str(t.value)
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


def t_DATA_TYPE_DEF(t):
    r'\:\s?(int16|int10|int8|int2|boolean|string)'
    t.value = re.search(r'\:\s?(.+)', t.value).group(1)
    return t


def t_INTEGER(t):
    r'(0x[0-9A-Fa-f]+)|([0-9]+)|(0o[0-9]+)|(0b[0-1]+)'
    t.value = int(t.value)
    return t


def t_FLOAT(t):
    r'\d+(\.\d+){0,1}f'
    t.value = float(t.value)
    return t


def t_BOOLEAN(t):
    r'true|false'
    t.value = bool(t.value)
    return t


def t_STRING(t):
    r'\".*\"'
    t.value = str(t.value)
    return t


# ##################################################
# Token precedence
# ########################################


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


# ##################################################
# Basic structure token rule definitions
# ########################################


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

