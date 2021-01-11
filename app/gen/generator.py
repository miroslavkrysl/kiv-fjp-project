from app.gen.code import CodeBuilder
from app.gen.descriptor import ArrayDesc
from app.gen.predefined import JAVA_STRING_CLASS
from app.types import TypeInt, TypeReal, TypeBool, TypeStr
from app.syntax import Node


def _value_array(code: CodeBuilder, items, array_type: ArrayDesc):
    if array_type.dim == 1:
        if array_type.inner == TypeInt():
            code.new_array_int()
        elif array_type.inner == TypeReal():
            code.new_array_double()
        elif array_type.inner == TypeBool():
            code.new_array_boolean()
        elif array_type.inner == TypeStr():
            code.new_array_reference(JAVA_STRING_CLASS)
        else:
            raise NotImplementedError()
    else:
        code.new_array_reference(ArrayDesc(array_type.dim, array_type.inner).utf8())


def _node(code: CodeBuilder, node):

    if node[0] == Node.VALUE_INT:
        code.const_int(node[1])
    elif node[0] == Node.VALUE_REAL:
        code.const_double(node[1])
    elif node[0] == Node.VALUE_BOOL:
        code.const_int(int(node[1]))
    elif node[0] == Node.VALUE_STR:
        code.const_string(node[1])
    elif node[0] == Node.VALUE_ARRAY:
        _value_array(code, node[1], node[2])
    else:
        raise NotImplementedError()


        VALUE_ARRAY = auto()
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


    # Variables
    VARIABLE_VALUE = auto()
    VARIABLE_DECLARATION = auto()
    VARIABLE_DEFINITION = auto()
    CONSTANT_DEFINITION = auto()
    VARIABLE_ASSIGN = auto()
