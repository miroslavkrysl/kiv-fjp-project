from typing import Optional, List

from app.gen.code import Code
from app.gen.descriptor import ArrayDesc, FieldDescriptor, IntDesc, DoubleDesc, BooleanDesc, ObjectDesc, \
    MethodDescriptor
from app.gen.predefined import J_CLINIT_NAME, J_CLINIT_DESCRIPTOR, JC_STRING, J_MAIN_NAME, J_MAIN_DESCRIPTOR
from app.gen.struct import Class
from app.names import FN_MAIN, MAIN_PARAMS, MAIN_RETURN
from app.types import TypeInt, TypeReal, TypeBool, TypeStr, Type, TypeArray
from app.syntax import Node


def _create_field_descriptor(t: Type) -> FieldDescriptor:
    if isinstance(t, TypeInt):
        return IntDesc()
    elif isinstance(t, TypeReal):
        return DoubleDesc()
    elif isinstance(t, TypeBool):
        return BooleanDesc()
    elif isinstance(t, TypeStr):
        return ObjectDesc(JC_STRING)
    elif isinstance(t, TypeArray):
        if isinstance(t.inner, TypeInt):
            inner = IntDesc()
        elif isinstance(t.inner, TypeReal):
            inner = DoubleDesc()
        elif isinstance(t.inner, TypeBool):
            inner = BooleanDesc()
        elif isinstance(t.inner, TypeStr):
            inner = ObjectDesc(JC_STRING)
        else:
            raise NotImplementedError()

        return ArrayDesc(t.dim, inner)
    else:
        raise NotImplementedError()


def _create_method_descriptor(params: List[Type], ret: Optional[Type]) -> MethodDescriptor:
    params_desc = [_create_field_descriptor(p) for p in params]
    ret_desc = None if ret is None else _create_field_descriptor(ret)
    return MethodDescriptor(params_desc, ret_desc)


def _generate_statement(code: Code, statement, loop_target: Optional[int] = None):
    if statement[0] == Node.VARIABLE_DECLARATION:
        # TODO
        pass
    elif statement[0] == Node.VARIABLE_DEFINITION:
        # TODO
        pass
    elif statement[0] == Node.CONSTANT_DEFINITION:
        # TODO
        pass
    elif statement[0] == Node.STORE:
        # TODO
        pass
    elif statement[0] == Node.FUNCTION_CALL:
        # TODO
        pass
    elif statement[0] == Node.RETURN:
        # TODO
        pass
    elif statement[0] == Node.IF:
        # TODO
        pass
    elif statement[0] == Node.IF_ELSE:
        # TODO
        pass
    elif statement[0] == Node.WHILE:
        # TODO
        pass
    elif statement[0] == Node.BREAK:
        # TODO
        pass
    elif statement[0] == Node.CONTINUE:
        # TODO
        pass
    else:
        raise NotImplementedError()


def _generate_expression(code: Code, expression):
    # TODO
    pass


def _generate_clinit(cls: Class, symbols, constants):
    clinit = cls.method(J_CLINIT_NAME, J_CLINIT_DESCRIPTOR)
    code = clinit.code

    for c in constants:
        name = c[1]
        const_type = c[2]
        expression = c[3]
        descriptor = _create_field_descriptor(const_type)

        cls.field(name, descriptor)
        _generate_expression(code, expression)


def _generate_functions(cls: Class, functions):
    for f in functions:
        name = f[1]
        params = f[2]
        ret = f[3]
        statements = f[4]

        method_desc = _create_method_descriptor(params, ret)

        method = cls.method(name, method_desc)
        for s in statements:
            _generate_statement(method.code, s)


def _generate_main(cls: Class, main_class_name: str):
    method = cls.method(J_MAIN_NAME, J_MAIN_DESCRIPTOR)
    method.code.invoke_static(main_class_name, FN_MAIN, _create_method_descriptor(MAIN_PARAMS, MAIN_RETURN))
    method.code.return_void()


def generate(self, class_name, ast) -> Class:
    cls = Class(class_name)
    constants = []
    functions = []

    for node in ast[1]:
        if node[0] == Node.CONSTANT_DEFINITION:
            constants.append(node)
        elif node[0] == Node.FUNCTION_DEFINITION:
            functions.append(node)
        else:
            NotImplementedError()

    self._generate_main()
    self._generate_clinit(constants)
    self._generate_functions(functions)

    return cls
