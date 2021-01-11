from app.syntax.ast import Node

from app.lex import tokens
from app.types import TypeInt, TypeReal, TypeBool, TypeStr, TypeArray

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('right', 'UMINUS', 'UPLUS')
)


def p_definition(p):
    """
    definitions :
                | definitions constant_definition SEMICOLON
                | definitions function_definition
    """
    if len(p) <= 1:
        p[0] = ()
    else:
        p[0] = p[1] + (p[2])


def p_statements(p):
    """
    statements  :
                | statements variable_declaration SEMICOLON
                | statements variable_definition SEMICOLON
                | statements constant_definition SEMICOLON
                | statements store SEMICOLON
                | statements function_call SEMICOLON
                | statements return SEMICOLON
                | statements if
                | statements if_else
                | statements while
                | statements break SEMICOLON
                | statements continue SEMICOLON
    """
    if len(p) <= 1:
        p[0] = ()
    else:
        p[0] = p[1] + (p[2])


# --- Functions ---

def p_function_definition(p):
    """
    function_definition : FN IDENTIFIER LPAREN parameters RPAREN LBRACE statements RBRACE
                        | FN IDENTIFIER LPAREN parameters RPAREN COLON type LBRACE statements RBRACE
    """
    ret = None if len(p) == 9 else p[7]
    statements = p[7] if len(p) == 9 else p[9]
    p[0] = (Node.FUNCTION_DEFINITION, p[2], p[4], ret[1], statements)


def p_parameters(p):
    """
    parameters  :
                | parameters_list
    """
    if len(p) <= 1:
        p[0] = []
    else:
        p[0] = p[1]


def p_parameters_list(p):
    """
    parameters_list : parameter
                    | parameters_list COMMA parameter
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_parameter(p):
    """
    parameter   : IDENTIFIER COLON type
    """
    p[0] = (p[1], p[3][1])


def p_function_call(p):
    """
    function_call   : IDENTIFIER LPAREN arguments RPAREN
    """
    p[0] = (Node.FUNCTION_CALL, p[1], p[3])


def p_function_call_value(p):
    """
    function_call_value : function_call
    """
    p[0] = (Node.FUNCTION_CALL_VALUE, p[1][1], p[1][3])


def p_arguments(p):
    """
    arguments   :
                | arguments_list
    """
    if len(p) <= 1:
        p[0] = []
    else:
        p[0] = p[1]


def p_arguments_list(p):
    """
    arguments_list  : expression
                    | arguments_list COMMA expression
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_return(p):
    """
    return  : RETURN expression
    """
    p[0] = (Node.RETURN, p[2])


# --- Types ---

def p_type(p):
    """
    type    : type_int
            | type_real
            | type_bool
            | type_str
            | type_array
    """
    p[0] = p[1]


def p_type_int(p):
    """
    type_int : TYPE_INT
    """
    p[0] = (Node.TYPE_INT, TypeInt())


def p_type_real(p):
    """
    type_real    : TYPE_REAL
    """
    p[0] = (Node.TYPE_REAL, TypeReal())


def p_type_bool(p):
    """
    type_bool    : TYPE_BOOL
    """
    p[0] = (Node.TYPE_BOOL, TypeBool())


def p_type_str(p):
    """
    type_str : TYPE_STR
    """
    p[0] = (Node.TYPE_STR, TypeStr())


def p_type_array(p):
    """
    type_array   : LBRACKET type RBRACKET
    """
    if p[2][0] == Node.TYPE_ARRAY:
        p[0] = (Node.TYPE_ARRAY, TypeArray(p[2][1].dim + 1, p[2][1].inner))
    else:
        p[0] = (Node.TYPE_ARRAY, TypeArray(1, p[2][1]))


# --- Conditions ---

def p_if(p):
    """
    if  : IF expression LBRACE statements RBRACE
    """
    p[0] = (Node.IF, p[2], p[4])


def p_if_else(p):
    """
    if_else : IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE
    """
    p[0] = (Node.IF_ELSE, p[2], p[4], p[8])


# --- Cycles ---

def p_while(p):
    """
    while   : WHILE expression LBRACE statements RBRACE
    """
    p[0] = (Node.WHILE, p[2], p[4])


def p_break(p):
    """
    break   : BREAK
    """
    p[0] = (Node.BREAK,)


def p_continue(p):
    """
    continue    : CONTINUE
    """
    p[0] = (Node.CONTINUE,)


# --- Expressions ---

def p_expression(p):
    """
    expression  : value
                | load
                | assignment
                | operator
                | parens
                | function_call_value
    """
    p[0] = p[1]


def p_parens(p):
    """
    parens  : LPAREN expression RPAREN
    """
    p[0] = p[2]


# --- Operators ---

def p_operator(p):
    """
    operator    : uplus
                | uminus
                | mul
                | div
                | plus
                | minus
                | eq
                | ne
                | lt
                | gt
                | le
                | ge
                | not
                | and
                | or
    """
    p[0] = p[1]


def p_assignment(p):
    """
    assignment : store
    """
    if p[1][0] == Node.VARIABLE_STORE:
        p[0] = (Node.VARIABLE_ASSIGNMENT, p[1][1], p[1][2])
    else:
        p[0] = (Node.ARRAY_ASSIGNMENT, p[1][1], p[1][2], p[1][3])


def p_uplus(p):
    """
    uplus   : PLUS expression %prec UPLUS
    """
    p[0] = (Node.UPLUS, p[2])


def p_uminus(p):
    """
    uminus  : MINUS expression %prec UMINUS
    """
    p[0] = (Node.UMINUS, p[2])


def p_mul(p):
    """
    mul : expression MUL expression
    """
    p[0] = (Node.MUL, p[1], p[3])


def p_div(p):
    """
    div : expression DIV expression
    """
    p[0] = (Node.DIV, p[1], p[3])


def p_plus(p):
    """
    plus    : expression PLUS expression
    """
    p[0] = (Node.PLUS, p[1], p[3])


def p_minus(p):
    """
    minus   : expression MINUS expression
    """
    p[0] = (Node.MINUS, p[1], p[3])


def p_eq(p):
    """
    eq  : expression EQ expression
    """
    p[0] = (Node.EQ, p[1], p[3])


def p_ne(p):
    """
    ne  : expression NE expression
    """
    p[0] = (Node.NE, p[1], p[3])


def p_lt(p):
    """
    lt  : expression LT expression
    """
    p[0] = (Node.LT, p[1], p[3])


def p_gt(p):
    """
    gt  : expression GT expression
    """
    p[0] = (Node.GT, p[1], p[3])


def p_le(p):
    """
    le  : expression LE expression
    """
    p[0] = (Node.LE, p[1], p[3])


def p_ge(p):
    """
    ge  : expression GE expression
    """
    p[0] = (Node.GE, p[1], p[3])


def p_not(p):
    """
    not : NOT expression
    """
    p[0] = (Node.NOT, p[2])


def p_and(p):
    """
    and : expression AND expression
    """
    p[0] = (Node.AND, p[1], p[3])


def p_or(p):
    """
    or  : expression OR expression
    """
    p[0] = (Node.OR, p[1], p[3])


# --- Variables ---

def p_variable_declaration(p):
    """
    variable_declaration    : VAR IDENTIFIER COLON type
    """
    p[0] = (Node.VARIABLE_DECLARATION, p[2], p[4])


def p_variable_definition(p):
    """
    variable_definition : VAR IDENTIFIER COLON type ASSIGN expression
    """
    p[0] = (Node.VARIABLE_DEFINITION, p[2], p[4], p[6])


def p_constant_definition(p):
    """
    constant_definition : CONST IDENTIFIER COLON type ASSIGN expression
    """
    p[0] = (Node.CONSTANT_DEFINITION, p[2], p[4], p[6])


def p_load(p):
    """
    load    : IDENTIFIER
            | expression array_access
    """
    if len(p) == 2:
        p[0] = (Node.VARIABLE_LOAD, p[1])
    else:
        p[0] = (Node.ARRAY_LOAD, p[1], p[2])


def p_store(p):
    """
    store   : IDENTIFIER ASSIGN expression
            | IDENTIFIER array_access ASSIGN expression
    """
    if len(p) == 4:
        p[0] = (Node.VARIABLE_STORE, p[1], p[3])
    else:
        p[0] = (Node.ARRAY_STORE, p[1], p[2], p[4])


def p_array_access(p):
    """
    array_access    : LBRACKET expression RBRACKET
                    | array_access LBRACKET expression RBRACKET
    """
    if len(p) == 4:
        p[0] = [p[2]]
    else:
        p[0] = [*p[1], p[3]]


# --- Values ---

def p_value(p):
    """
    value   : value_int
            | value_real
            | value_bool
            | value_str
            | value_array
    """
    p[0] = p[1]


def p_value_int(p):
    """
    value_int : LITERAL_INT
    """
    p[0] = (Node.VALUE_INT, p[1])


def p_value_real(p):
    """
    value_real    : LITERAL_REAL
    """
    p[0] = (Node.VALUE_REAL, p[1])


def p_value_bool(p):
    """
    value_bool    : LITERAL_BOOL
    """
    p[0] = (Node.VALUE_BOOL, p[1])


def p_value_str(p):
    """
    value_str : LITERAL_STR
    """
    p[0] = (Node.VALUE_STR, p[1])


def p_value_array(p):
    """
    value_array   : LBRACKET items RBRACKET
    """
    p[0] = (Node.VALUE_ARRAY, p[2])


def p_items(p):
    """
    items   :
            | items_list
    """
    if len(p) <= 1:
        p[0] = []
    else:
        p[0] = p[1]


def p_items_list(p):
    """
    items_list  : expression
                | items_list COMMA expression
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


# --- Other ---

# Error rule for syntax errors
def p_error(p):
    if p is not None:
        print(f"Syntax error [{p.lexer.lexpos}]")
    else:
        print("Unexpected end of input")

    # print("Syntax error in input!")
