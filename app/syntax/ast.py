from abc import ABC
from enum import Enum, auto


class Node(Enum):
    # Conditions
    IF = auto()
    IF_ELSE = auto()

    # Cycles
    WHILE = auto()
    BREAK = auto()
    CONTINUE = auto()

    # Operators
    ASSIGN = auto()
    INDEX = auto()
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
    RETURN = auto()

    # Literals
    VALUE_INT = auto()
    VALUE_REAL = auto()
    VALUE_BOOL = auto()
    VALUE_STR = auto()
    VALUE_ARRAY = auto()

    # Variables
    VARIABLE_VALUE = auto()
    VARIABLE_DECLARATION = auto()
    VARIABLE_DEFINITION = auto()
    CONSTANT_DEFINITION = auto()
    VARIABLE_ASSIGN = auto()

    # Types
    TYPE_INT = auto()
    TYPE_REAL = auto()
    TYPE_BOOL = auto()
    TYPE_STR = auto()
    TYPE_ARRAY = auto()

    def __repr__(self):
        return f'<{self.__class__.__name__}.{self._name_}>'