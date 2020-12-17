# Get the token map from the lexer. This is required.
from app.analyzers.lex import *


# ##################################################
# General parse rule definitions
# ########################################


def p_Expression(p):
    '''
    Expression : VariableDeclare
               | VariableDeclareAssign
               | Operator
               | FunctionCall
               | IDENTIFIER
               | Literal
    '''
    p[0] = ('Expression', p[1])


def p_ExpressionBlock(p):
    '''
    ExpressionBlock : Expression
    '''
    p[0] = ('ExpressionBlock', p[1])


def p_Literal(p):
    '''
    Literal : INTEGER
            | FLOAT
            | BOOLEAN
            | STRING
    '''
    p[0] = ('Literal', p[1])


def p_VariableDeclare(p):
    '''
    VariableDeclare : IDENTIFIER DATA_TYPE_DEF
    '''
    p[0] = ('VariableDeclare', p[1], p[2])


def p_VariableDeclareAssign(p):
    '''
    VariableDeclareAssign : IDENTIFIER DATA_TYPE_DEF EQUAL Expression
    '''
    p[0] = ('VariableDeclareAssign', p[1], p[2], p[4])


def p_Operator(p):
    '''
    Operator : Plus
             | Minus
             | Multiply
             | Divide
             | LPAREN Operator RPAREN
    '''
    p[0] = ('Operator', p[1])


def p_Plus(p):
    '''
    Plus : Expression PLUS Expression
    '''
    p[0] = ('Plus', p[2], p[1], p[3])


# def p_UnaryPlus(p):
#     'UnaryPlus : Expression PLUS Expression'
#     p[0] = ('UnaryPlus', p[2], p[1], p[3])


def p_Minus(p):
    '''
    Minus : Expression MINUS Expression
    '''
    p[0] = ('Minus', p[2], p[1], p[3])


# def p_UnaryMinus(p):
#     'UnaryMinus : Expression MINUS Expression'
#     p[0] = ('UnaryMinus', p[2], p[1], p[3])


def p_Multiply(p):
    '''
    Multiply : Expression TIMES Expression
    '''
    p[0] = ('Multiply', p[2], p[1], p[3])


def p_Divide(p):
    '''
    Divide : Expression DIVIDE Expression
    '''
    p[0] = ('Divide', p[2], p[1], p[3])


def p_ConditionExpression(p):
    '''
    ConditionExpression : IF LPAREN Expression RPAREN LBRACE ExpressionBlock RBRACE
                        | IF LPAREN Expression RPAREN LBRACE ExpressionBlock RBRACE ELSE LBRACE ExpressionBlock RBRACE
    '''
    p[0] = ('ConditionExpression', p[3], p[6], p[10] if len(p) > 10 else None)


def p_WhileLoopExpression(p):
    '''
    WhileLoopExpression : WHILE LPAREN Expression RPAREN LBRACE ExpressionBlock RBRACE
    '''
    p[0] = ('WhileLoopExpression', p[3], p[6])


def p_FunctionDeclare(p):
    '''
    FunctionDeclare : FUNCTION IDENTIFIER LPAREN FunctionDeclareParameters RPAREN LBRACE ExpressionBlock RBRACE
    '''
    p[0] = ('FunctionDeclare', p[2], p[4], p[7])


def p_FunctionCall(p):
    '''
    FunctionCall : IDENTIFIER LPAREN FunctionCallParameters RPAREN
    '''
    p[0] = ('FunctionCall', p[1], p[3])


def p_FunctionDeclareParameters(p):
    '''
    FunctionDeclareParameters :
                              | Expression
                              | FunctionDeclareParameters COMMA VariableDeclare
    '''
    p[0] = ('FunctionDeclareParameters', p[1] if len(p) > 1 else None, p[3] if len(p) > 3 else None)


def p_FunctionCallParameters(p):
    '''
    FunctionCallParameters :
                           | Expression
                           | FunctionCallParameters COMMA Expression
    '''
    p[0] = ('FunctionCallParameters', p[1] if len(p) > 1 else None, p[3] if len(p) > 3 else None)


# ##################################################
# Basic structure parse rule definitions
# ########################################


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

