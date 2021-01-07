from ply.lex import TOKEN

keywords = {
    'var': 'VAR',
    'const': 'CONST',
    'fn': 'FN',
    'return': 'RETURN',

    # Conditions
    'if': 'IF',
    'else': 'ELSE',

    # Cycles
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',

    # Data types
    'Int': 'TYPE_INT',
    'Real': 'TYPE_REAL',
    'Bool': 'TYPE_BOOL',
    'Str': 'TYPE_STR'
}

t_COMMA = r'\,'
t_COLON = r':'
t_SEMICOLON = r'\;'

t_MUL = r'\*'
t_DIV = r'/'
t_PLUS = r'\+'
t_MINUS = r'-'
t_EQ = r'=='
t_NE = r'!='
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_NOT = r'!'
t_AND = r'&'
t_OR = r'\|'
t_ASSIGN = r'='

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'

SIGN = r'(\+|-)?'
DIGITS = r'[0-9]+'
EXPONENT = r'((e|E)' + SIGN + DIGITS + r')'
REAL1 = r'(' + DIGITS + r'\.' + DIGITS + EXPONENT + r'?' + r')'
REAL2 = r'(' + DIGITS + EXPONENT + r')'
REAL3 = r'(' + DIGITS + r'\.' + r')'
LITERAL_REAL = SIGN + r'(' + REAL1 + r'|' + REAL2 + r'|' + REAL3 + r')'


@TOKEN(LITERAL_REAL)
def t_LITERAL_REAL(t):
    t.value = float(t.value)
    return t


def t_LITERAL_INT(t):
    r"""
    (0x[0-9A-Fa-f]+)|([0-9]+)|(0o[0-7]+)|(0b[0-1]+)
    """
    t.value = int(t.value)
    return t


def t_LITERAL_BOOL(t):
    r"""
    true|false
    """
    t.value = bool(t.value)
    return t


def t_LITERAL_STR(t):
    r"""
    "([^\\"]|\\.)*\"
    """
    t.value = str(t.value)
    return t


def t_IDENTIFIER(t):
    r"""
    [a-zA-Z_]+[a-zA-Z0-9_]*
    """
    k = keywords.get(t.value)
    if k:
        t.type = k
    return t


# --- Comments ---

# TODO
# def t_line_comment(t):
#     r"""
#     #
#     """
#


# To track line numbers
def t_newline(t):
    r"""
    \n
    """
    t.lexer.lineno += 1


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


def find_column(inp, pos):
    line_start = inp.rfind('\n', 0, pos) + 1
    return pos - line_start


# Error handling rule
def t_error(t):
    print("lexer error: line=", t.lexer.lineno, "col=", find_column(t.lexer.lexdata, t.lexer.lexpos))
    t.lexer.skip(1)
