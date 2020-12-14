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
    'Expression : ArithmeticExpression'
    p[0] = ('Expression', p[1])


def p_Expression_4(p):
    'Expression : FunctionCall'
    p[0] = ('Expression', p[1])


def p_ExpressionBlock_1(p):
    'ExpressionBlock : Expression'
    p[0] = ('ExpressionBlock', p[1])


def p_VariableDeclare_1(p):
    'VariableDeclare : IDENTIFIER DATA_TYPE_DEF'
    p[0] = ('VariableDeclare', p[1], p[2])


def p_VariableDeclareAssign_1(p):
    'VariableDeclareAssign : IDENTIFIER DATA_TYPE_DEF EQUAL Expression'
    p[0] = ('VariableDeclareAssign', p[1], p[2], p[4])


def p_ArithmeticExpression_1(p):
    'ArithmeticExpression : ExpressionPlus'
    p[0] = ('ArithmeticExpression', p[1])


def p_ArithmeticExpression_2(p):
    'ArithmeticExpression : ExpressionMinus'
    p[0] = ('ArithmeticExpression', p[1])


# def p_ArithmeticExpression_3(p):
#     'ArithmeticExpression : ExpressionUnaryMinus'
#     p[0] = ('ArithmeticExpression', p[1])


# def p_ArithmeticExpression_4(p):
#     'ArithmeticExpression : ExpressionUnaryPlus'
#     p[0] = ('ArithmeticExpression', p[1])


def p_ArithmeticExpression_5(p):
    'ArithmeticExpression : ExpressionMultiply'
    p[0] = ('ArithmeticExpression', p[1])


def p_ArithmeticExpression_6(p):
    'ArithmeticExpression : ExpressionDivide'
    p[0] = ('ArithmeticExpression', p[1])


def p_ArithmeticExpression_7(p):
    'ArithmeticExpression : LPAREN ArithmeticExpression RPAREN'
    p[0] = ('ArithmeticExpression', p[2])


def p_ExpressionPlus_1(p):
    'ExpressionPlus : Expression PLUS Expression'
    p[0] = ('ExpressionPlus', p[2], p[1], p[3])


# def p_ExpressionUnaryPlus_1(p):
#     'ExpressionUnaryPlus : Expression PLUS Expression'
#     p[0] = ('ExpressionUnaryPlus', p[2], p[1], p[3])


def p_ExpressionMinus_1(p):
    'ExpressionMinus : Expression MINUS Expression'
    p[0] = ('ExpressionMinus', p[2], p[1], p[3])


# def p_ExpressionUnaryMinus_1(p):
#     'ExpressionUnaryMinus : Expression MINUS Expression'
#     p[0] = ('ExpressionUnaryMinus', p[2], p[1], p[3])


def p_ExpressionMultiply_1(p):
    'ExpressionMultiply : Expression TIMES Expression'
    p[0] = ('ExpressionMultiply', p[2], p[1], p[3])


def p_ExpressionDivide_1(p):
    'ExpressionDivide : Expression DIVIDE Expression'
    p[0] = ('ExpressionDivide', p[2], p[1], p[3])


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
    'FunctionCall : IDENTIFIER LPAREN FunctionCallParameters RPAREN LBRACE ExpressionBlock RBRACE'
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

