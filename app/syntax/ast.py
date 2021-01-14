from abc import ABC
from enum import Enum, auto


class Node(Enum):

    def _generate_next_value_(name, start, count, last_values):
        return name

    PROGRAM = auto()

    # Conditions
    IF = auto()

    IF_ELSE = auto()
    # Cycles
    WHILE = auto()
    BREAK = auto()

    CONTINUE = auto()
    # Operators
    UMINUS = auto()
    UPLUS = auto()
    MUL = auto()
    DIV = auto()
    PLUS = auto()
    MINUS = auto()
    EQ = auto()
    NE = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()
    NOT = auto()
    AND = auto()

    OR = auto()
    # Functions
    FUNCTION_DEFINITION = auto()
    FUNCTION_CALL = auto()
    FUNCTION_CALL_VALUE = auto()
    PARAM = auto()
    RETURN = auto()

    RETURN_VOID = auto()
    # Literals
    VALUE_INT = auto()
    VALUE_REAL = auto()
    VALUE_BOOL = auto()
    VALUE_STR = auto()

    VALUE_ARRAY = auto()
    # Variables
    VARIABLE_STORE = auto()
    ARRAY_STORE = auto()
    VARIABLE_LOAD = auto()
    ARRAY_LOAD = auto()
    VARIABLE_ASSIGNMENT = auto()
    ARRAY_ASSIGNMENT = auto()
    VARIABLE_DEFINITION = auto()

    CONSTANT_DEFINITION = auto()
    # Types
    TYPE_INT = auto()
    TYPE_REAL = auto()
    TYPE_BOOL = auto()
    TYPE_STR = auto()
    TYPE_ARRAY = auto()

    TYPE_VOID = auto()

    def __str__(self):
        return f'{self._name_}'
