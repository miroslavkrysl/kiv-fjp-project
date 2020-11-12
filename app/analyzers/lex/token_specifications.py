import re

# ##################################################
# Reserved keyword definitions
# ########################################


reserved = {
    # keyword: TOKEN
    'if': 'IF',
    'else': 'ELSE',
 }


# ##################################################
# Simple token regex definitions
# ########################################


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
    r'[a-zA-Z]+'
    t.value = str(t.value)
    t.type = reserved.get(t.value, 'IDENTIFIER')
    return t


def t_DATA_TYPE_DEF(t):
    r'\:\s?(int16|int10|int8|int2|boolean|string)'
    t.value = re.search(r'\:\s?(.+)', t.value).group(1)
    return t


def t_INTEGER_HEX(t):
    r'0x[0-9A-Fa-f]+'
    t.value = int(t.value, 16)
    return t


def t_INTEGER_DEC(t):
    r'[0-9]+'
    t.value = int(t.value, 10)
    return t


def t_INTEGER_OCT(t):
    r'0o[0-9]+'
    t.value = int(t.value, 8)
    return t


def t_INTEGER_BIN(t):
    r'0b[0-1]+'
    t.value = int(t.value, 2)
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

