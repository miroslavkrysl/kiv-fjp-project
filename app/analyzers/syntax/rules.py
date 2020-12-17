# Get the token map from the lexer. This is required.
from app.analyzers.lex import *


# ##################################################
# General parse rule definitions
# ########################################


def p_Expression_1(p):
    'Expression : VariableDeclare'
    p[0] = ('Expression', p[1])


def p_Expression_2(p):
    'Expression : VariableDeclareAssign'
    p[0] = ('Expression', p[1])


def p_Expression_3(p):
    'Expression : Operator'
    p[0] = ('Expression', p[1])


def p_Expression_4(p):
    'Expression : FunctionCall'
    p[0] = ('Expression', p[1])


def p_Expression_5(p):
    'Expression : IDENTIFIER'
    p[0] = ('Expression', p[1])


def p_Expression_6(p):
    'Expression : Literal'
    p[0] = ('Expression', p[1])


def p_ExpressionBlock_1(p):
    'ExpressionBlock : Expression'
    p[0] = ('ExpressionBlock', p[1])


def p_Literal_1(p):
    'Literal : INTEGER'
    p[0] = ('Literal', p[1], 'int')


def p_Literal_2(p):
    'Literal : FLOAT'
    p[0] = ('Literal', p[1], 'float')


def p_Literal_3(p):
    'Literal : BOOLEAN'
    p[0] = ('Literal', p[1], 'bool')


def p_Literal_4(p):
    'Literal : STRING'
    p[0] = ('Literal', p[1], 'string')


def p_VariableDeclare_1(p):
    'VariableDeclare : IDENTIFIER DATA_TYPE_DEF'
    p[0] = ('VariableDeclare', p[1], p[2])


def p_VariableDeclareAssign_1(p):
    'VariableDeclareAssign : IDENTIFIER DATA_TYPE_DEF EQUAL Expression'
    p[0] = ('VariableDeclareAssign', p[1], p[2], p[4])


def p_Operator_1(p):
    'Operator : Plus'
    p[0] = ('Operator', p[1])


def p_Operator_2(p):
    'Operator : Minus'
    p[0] = ('Operator', p[1])


# def p_Operator_3(p):
#     'Operator : UnaryMinus'
#     p[0] = ('Operator', p[1])


# def p_Operator_4(p):
#     'Operator : UnaryPlus'
#     p[0] = ('Operator', p[1])


def p_Operator_5(p):
    'Operator : Multiply'
    p[0] = ('Operator', p[1])


def p_Operator_6(p):
    'Operator : Divide'
    p[0] = ('Operator', p[1])


def p_Operator_7(p):
    'Operator : LPAREN Operator RPAREN'
    p[0] = ('Operator', p[2])


def p_Plus_1(p):
    'Plus : Expression PLUS Expression'
    p[0] = ('Plus', p[2], p[1], p[3])


# def p_UnaryPlus_1(p):
#     'UnaryPlus : Expression PLUS Expression'
#     p[0] = ('UnaryPlus', p[2], p[1], p[3])


def p_Minus_1(p):
    'Minus : Expression MINUS Expression'
    p[0] = ('Minus', p[2], p[1], p[3])


# def p_UnaryMinus_1(p):
#     'UnaryMinus : Expression MINUS Expression'
#     p[0] = ('UnaryMinus', p[2], p[1], p[3])


def p_Multiply_1(p):
    'Multiply : Expression TIMES Expression'
    p[0] = ('Multiply', p[2], p[1], p[3])


def p_Divide_1(p):
    'Divide : Expression DIVIDE Expression'
    p[0] = ('Divide', p[2], p[1], p[3])


def p_ConditionExpression_1(p):
    'ConditionExpression : IF LPAREN Expression RPAREN LBRACE ExpressionBlock RBRACE'
    p[0] = ('ConditionExpression', p[3], p[6])


def p_ConditionExpression_2(p):
    'ConditionExpression : IF LPAREN Expression RPAREN LBRACE ExpressionBlock RBRACE ELSE LBRACE ExpressionBlock RBRACE'
    p[0] = ('ConditionExpression', p[3], p[6], p[10])


def p_WhileLoopExpression_1(p):
    'WhileLoopExpression : WHILE LPAREN Expression RPAREN LBRACE ExpressionBlock RBRACE'
    p[0] = ('WhileLoopExpression', p[3], p[6])


def p_FunctionDeclare_1(p):
    'FunctionDeclare : FUNCTION IDENTIFIER LPAREN FunctionDeclareParameters RPAREN LBRACE ExpressionBlock RBRACE'
    p[0] = ('FunctionDeclare', p[2], p[4], p[7])


def p_FunctionCall_1(p):
    'FunctionCall : IDENTIFIER LPAREN FunctionCallParameters RPAREN'
    p[0] = ('FunctionCall', p[1], p[3], p[6])


def p_FunctionDeclareParameters_1(p):
    'FunctionDeclareParameters : Expression'
    p[0] = ('FunctionDeclareParameters', p[1])


def p_FunctionDeclareParameters_2(p):
    'FunctionDeclareParameters : FunctionDeclareParameters COMMA VariableDeclare'
    p[0] = ('FunctionDeclareParameters', p[1], p[3])


def p_FunctionCallParameters_1(p):
    'FunctionCallParameters : Expression'
    p[0] = ('FunctionCallParameters', p[1])


def p_FunctionCallParameters_2(p):
    'FunctionCallParameters : FunctionCallParameters COMMA Expression'
    p[0] = ('FunctionCallParameters', p[1], p[3])


# ##################################################
# Basic structure parse rule definitions
# ########################################


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

