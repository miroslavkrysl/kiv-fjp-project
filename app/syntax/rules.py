from app.syntax.ast import Node

from app.lex import tokens

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQ', 'NE', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV'),
    ('right', 'UMINUS', 'UPLUS'),
    ('right', 'LBRACKET', 'RBRACKET')
)


def p_program(p):
    """
    definitions :
                | definitions constant_definition SEMICOLON
                | definitions function_definition
    """
    if len(p) <= 1:
        p[0] = {'node': Node.PROGRAM, 'statements': []}
    else:
        p[0] = {'node': Node.PROGRAM, 'statements': [*p[1]['statements'], p[2]]}


def p_statements(p):
    """
    statements  :
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
        p[0] = []
    else:
        p[0] = [*p[1], p[2]]


# --- Functions ---

def p_function_definition(p):
    """
    function_definition : FN IDENTIFIER LPAREN parameters RPAREN LBRACE statements RBRACE
                        | FN IDENTIFIER LPAREN parameters RPAREN COLON type LBRACE statements RBRACE
    """
    ret = {'node': Node.TYPE_VOID} if len(p) == 9 else p[7]
    statements = p[7] if len(p) == 9 else p[9]

    # (node, name, [parameters], return, [statements])
    p[0] = {'node': Node.FUNCTION_DEFINITION, 'name': p[2], 'parameters': p[4], 'return': ret, 'statements': statements}


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
    p[0] = {'node': Node.PARAM, 'name': p[1], 'type': p[3]}


def p_function_call(p):
    """
    function_call   : IDENTIFIER LPAREN arguments RPAREN
    """
    p[0] = {'node': Node.FUNCTION_CALL, 'name': p[1], 'arguments': p[3]}


def p_function_call_value(p):
    """
    function_call_value : function_call
    """
    p[0] = {'node': Node.FUNCTION_CALL_VALUE, 'name': p[1]['name'], 'arguments': p[1]['arguments']}


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
        p[0] = [*p[1], p[3]]


def p_return(p):
    """
    return  : RETURN expression
            | RETURN
    """
    if len(p) == 3:
        p[0] = {'node': Node.RETURN, 'expression': p[2]}
    else:
        p[0] = {'node': Node.RETURN_VOID}


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
    p[0] = {'node': Node.TYPE_INT}


def p_type_real(p):
    """
    type_real    : TYPE_REAL
    """
    p[0] = {'node': Node.TYPE_REAL}


def p_type_bool(p):
    """
    type_bool    : TYPE_BOOL
    """
    p[0] = {'node': Node.TYPE_BOOL}


def p_type_str(p):
    """
    type_str : TYPE_STR
    """
    p[0] = {'node': Node.TYPE_STR}


def p_type_array(p):
    """
    type_array   : LBRACKET type RBRACKET
    """
    if p[2]['node'] == Node.TYPE_ARRAY:
        p[0] = {'node': Node.TYPE_ARRAY, 'dim': p[2]['dim'] + 1, 'inner': p[2]['inner']}
    else:
        p[0] = {'node': Node.TYPE_ARRAY, 'dim': 1, 'inner': p[2]}


# --- Conditions ---

def p_if(p):
    """
    if  : IF expression LBRACE statements RBRACE
    """
    p[0] = {'node': Node.IF, 'condition': p[2], 'statements': p[4]}


def p_if_else(p):
    """
    if_else : IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE
    """
    p[0] = {'node': Node.IF_ELSE, 'condition': p[2], 'if_statements': p[4], 'else_statements': p[8]}


# --- Cycles ---

def p_while(p):
    """
    while   : WHILE expression LBRACE statements RBRACE
    """
    p[0] = {'node': Node.WHILE, 'condition': p[2], 'statements': p[4]}


def p_break(p):
    """
    break   : BREAK
    """
    p[0] = {'node': Node.BREAK}


def p_continue(p):
    """
    continue    : CONTINUE
    """
    p[0] = {'node': Node.CONTINUE}


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
    if p[1]['node'] == Node.VARIABLE_STORE:
        p[0] = {'node': Node.VARIABLE_ASSIGNMENT, 'name': p[1]['name'], 'expression': p[1]['expression']}
    else:
        p[0] = {'node': Node.ARRAY_ASSIGNMENT, 'name': p[1]['name'], 'indexes': p[1]['indexes'], 'expression': p[1]['expression']}


def p_uplus(p):
    """
    uplus   : PLUS expression %prec UPLUS
    """
    p[0] = {'node': Node.UPLUS, 'expression': p[2]}


def p_uminus(p):
    """
    uminus  : MINUS expression %prec UMINUS
    """
    p[0] = {'node': Node.UMINUS, 'expression': p[2]}


def p_mul(p):
    """
    mul : expression MUL expression
    """
    p[0] = {'node': Node.MUL, 'left': p[1], 'right': p[3]}


def p_div(p):
    """
    div : expression DIV expression
    """
    p[0] = {'node': Node.DIV, 'left': p[1], 'right': p[3]}


def p_plus(p):
    """
    plus    : expression PLUS expression
    """
    p[0] = {'node': Node.PLUS, 'left': p[1], 'right': p[3]}


def p_minus(p):
    """
    minus   : expression MINUS expression
    """
    p[0] = {'node': Node.MINUS, 'left': p[1], 'right': p[3]}


def p_eq(p):
    """
    eq  : expression EQ expression
    """
    p[0] = {'node': Node.EQ, 'left': p[1], 'right': p[3]}


def p_ne(p):
    """
    ne  : expression NE expression
    """
    p[0] = {'node': Node.NE, 'left': p[1], 'right': p[3]}


def p_lt(p):
    """
    lt  : expression LT expression
    """
    p[0] = {'node': Node.LT, 'left': p[1], 'right': p[3]}


def p_gt(p):
    """
    gt  : expression GT expression
    """
    p[0] = {'node': Node.GT, 'left': p[1], 'right': p[3]}


def p_le(p):
    """
    le  : expression LE expression
    """
    p[0] = {'node': Node.LE, 'left': p[1], 'right': p[3]}


def p_ge(p):
    """
    ge  : expression GE expression
    """
    p[0] = {'node': Node.GE, 'left': p[1], 'right': p[3]}


def p_not(p):
    """
    not : NOT expression
    """
    p[0] = {'node': Node.NOT, 'expression': p[2]}


def p_and(p):
    """
    and : expression AND expression
    """
    p[0] = {'node': Node.AND, 'left': p[1], 'right': p[3]}


def p_or(p):
    """
    or  : expression OR expression
    """
    p[0] = {'node': Node.OR, 'left': p[1], 'right': p[3]}


# --- Variables ---

def p_variable_definition(p):
    """
    variable_definition : VAR IDENTIFIER COLON type ASSIGN expression
    """
    p[0] = {'node': Node.VARIABLE_DEFINITION, 'name': p[2], 'type': p[4], 'expression': p[6]}


def p_constant_definition(p):
    """
    constant_definition : CONST IDENTIFIER COLON type ASSIGN expression
    """
    # (node, name, type, expression)
    p[0] = {'node': Node.CONSTANT_DEFINITION, 'name': p[2], 'type': p[4], 'expression': p[6]}


def p_load(p):
    """
    load    : IDENTIFIER
            | IDENTIFIER array_access
    """
    if len(p) == 2:
        p[0] = {'node': Node.VARIABLE_LOAD, 'name': p[1]}
    else:
        p[0] = {'node': Node.ARRAY_LOAD, 'name': p[1], 'indexes': p[2]}


def p_var(p):
    """
    var     : IDENTIFIER
    """
    if len(p) == 4:
        p[0] = {'node': Node.VARIABLE_STORE, 'name': p[1], 'expression': p[3]}
    else:
        p[0] = {'node': Node.ARRAY_STORE, 'name': p[1], 'indexes': p[2], 'expression': p[4]}


def p_store(p):
    """
    store   : IDENTIFIER ASSIGN expression
            | IDENTIFIER array_access ASSIGN expression
    """
    if len(p) == 4:
        p[0] = {'node': Node.VARIABLE_STORE, 'name': p[1], 'expression': p[3]}
    else:
        p[0] = {'node': Node.ARRAY_STORE, 'name': p[1], 'indexes': p[2], 'expression': p[4]}


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
    p[0] = {'node': Node.VALUE_INT, 'value': p[1]}


def p_value_real(p):
    """
    value_real    : LITERAL_REAL
    """
    p[0] = {'node': Node.VALUE_REAL, 'value': p[1]}


def p_value_bool(p):
    """
    value_bool    : LITERAL_BOOL
    """
    p[0] = {'node': Node.VALUE_BOOL, 'value': p[1]}


def p_value_str(p):
    """
    value_str : LITERAL_STR
    """
    p[0] = {'node': Node.VALUE_STR, 'value': p[1]}


def p_value_array(p):
    """
    value_array   : LBRACKET items RBRACKET
    """
    p[0] = {'node': Node.VALUE_ARRAY, 'items': p[2]}


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

    raise SyntaxError()

    # print("Syntax error in input!")
