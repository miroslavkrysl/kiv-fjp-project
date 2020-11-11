# ##################################################
# Simple token regex definitions
# ########################################


t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'


# ##################################################
# Advanced token regex definitions
# ########################################


# A regular expression rule with some action code
def t_NUMBER(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


# ##################################################
# Basic structure token rule definitions
# ########################################


# Define a rule so we can track line numbers
def t_newline(t):
    r"""\n+"""
    t.lexer.lineno += len(t.value)


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

