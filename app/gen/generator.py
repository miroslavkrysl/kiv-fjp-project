from typing import Optional, List, Dict

from app.gen.code import Code
from app.gen.descriptor import ArrayDesc, FieldDescriptor, IntDesc, DoubleDesc, BooleanDesc, ObjectDesc, \
    MethodDescriptor
from app.gen.predefined import J_CLINIT_NAME, J_CLINIT_DESCRIPTOR, JC_STRING, J_MAIN_NAME, J_MAIN_DESCRIPTOR
from app.gen.struct import Class
from app.names import FN_MAIN, MAIN_PARAMS, MAIN_RETURN, BOOL_INT_FALSE, BOOL_INT_TRUE
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


def _get_variable(variables, name) -> Union[int, ]:
    for i in symbols:


    raise KeyError(f'Symbol {symbol} is not in the symbols table')

def _generate_statement(code: Code, symbols, statement, loop_target: Optional[int] = None):
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


def _exp_uminus(code: Code, exp):
    r = exp[1]
    t = exp[2]
    _expression(code, r)

    if isinstance(t, TypeInt):
        code.neg_int()
    elif isinstance(t, TypeReal):
        code.neg_double()
    else:
        NotImplementedError()


def _exp_uplus(code: Code, exp):
    # nothing to do
    pass


def _exp_mul(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeInt):
        code.mul_int()
    elif isinstance(t, TypeReal):
        code.mul_double()
    else:
        NotImplementedError()


def _exp_div(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeInt):
        code.div_int()
    elif isinstance(t, TypeReal):
        code.div_double()
    else:
        NotImplementedError()


def _exp_plus(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeInt):
        code.add_int()
    elif isinstance(t, TypeReal):
        code.add_double()
    elif isinstance(t, TypeStr):
        # TODO string concat
        pass
    elif isinstance(t, ArrayDesc):
        # TODO array concat
        pass
    else:
        NotImplementedError()


def _exp_minus(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeInt):
        code.sub_int()
    elif isinstance(t, TypeReal):
        code.sub_double()
    else:
        NotImplementedError()


def _exp_sub(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeInt):
        code.add_int()
    elif isinstance(t, TypeReal):
        code.add_double()
    elif isinstance(t, TypeStr):
        # TODO string concat
        pass
    elif isinstance(t, ArrayDesc):
        # TODO array concat
        pass
    else:
        NotImplementedError()


def _exp_eq(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)


    if isinstance(t, TypeInt) or isinstance(t, TypeBool) or isinstance(t, TypeReal):
        if isinstance(t, TypeReal):
            code.cmp_double_l()
            cmp_pos = code.pos()
            code.if_eq()
        else:
            cmp_pos = code.pos()
            code.if_cmp_int_eq()
        code.const_int(BOOL_INT_FALSE)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(BOOL_INT_TRUE)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    elif isinstance(t, TypeStr):
        # TODO string cmp
        pass
    elif isinstance(t, TypeArray):
        # TODO array cmp
        pass
    else:
        NotImplementedError()


def _exp_ne(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeInt) or isinstance(t, TypeBool) or isinstance(t, TypeReal):
        if isinstance(t, TypeReal):
            code.cmp_double_l()
            cmp_pos = code.pos()
            code.if_ne()
        else:
            cmp_pos = code.pos()
            code.if_cmp_int_ne()
        code.const_int(BOOL_INT_FALSE)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(BOOL_INT_TRUE)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    elif isinstance(t, TypeStr):
        # TODO string cmp
        pass
    elif isinstance(t, TypeArray):
        # TODO array cmp
        pass
    else:
        NotImplementedError()


def _exp_lt(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeInt) or isinstance(t, TypeReal):
        if isinstance(t, TypeReal):
            code.cmp_double_l()
            cmp_pos = code.pos()
            code.if_lt()
        else:
            cmp_pos = code.pos()
            code.if_cmp_int_lt()
        code.const_int(BOOL_INT_FALSE)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(BOOL_INT_TRUE)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_gt(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeInt) or isinstance(t, TypeReal):
        if isinstance(t, TypeReal):
            code.cmp_double_g()
            cmp_pos = code.pos()
            code.if_gt()
        else:
            cmp_pos = code.pos()
            code.if_cmp_int_gt()
        code.const_int(BOOL_INT_FALSE)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(BOOL_INT_TRUE)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_le(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeInt) or isinstance(t, TypeReal):
        if isinstance(t, TypeReal):
            code.cmp_double_l()
            cmp_pos = code.pos()
            code.if_le()
        else:
            cmp_pos = code.pos()
            code.if_cmp_int_le()
        code.const_int(BOOL_INT_FALSE)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(BOOL_INT_TRUE)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_ge(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeInt) or isinstance(t, TypeReal):
        if isinstance(t, TypeReal):
            code.cmp_double_g()
            cmp_pos = code.pos()
            code.if_ge()
        else:
            cmp_pos = code.pos()
            code.if_cmp_int_ge()
        code.const_int(BOOL_INT_FALSE)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(BOOL_INT_TRUE)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_not(code: Code, exp):
    r = exp[2]
    t = exp[3]
    _expression(code, r)

    if isinstance(t, TypeBool):
        cmp_pos = code.pos()
        code.if_eq()
        code.const_int(BOOL_INT_FALSE)
        goto_pos = code.pos()
        code.goto()
        false_pos = code.pos()
        code.const_int(BOOL_INT_TRUE)
        end_pos = code.pos()

        code.update_jump(cmp_pos, false_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_and(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeBool):
        cmp1_pos = code.pos()
        code.if_eq()
        cmp2_pos = code.pos()
        code.if_eq()
        code.const_int(BOOL_INT_TRUE)
        goto_pos = code.pos()
        code.goto()
        false_pos = code.pos()
        code.const_int(BOOL_INT_FALSE)
        end_pos = code.pos()

        code.update_jump(cmp1_pos, false_pos)
        code.update_jump(cmp2_pos, false_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_or(code: Code, exp):
    l = exp[1]
    r = exp[2]
    t = exp[3]
    _expression(code, l)
    _expression(code, r)

    if isinstance(t, TypeBool):
        cmp1_pos = code.pos()
        code.if_ne()
        cmp2_pos = code.pos()
        code.if_ne()
        code.const_int(BOOL_INT_FALSE)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(BOOL_INT_TRUE)
        end_pos = code.pos()

        code.update_jump(cmp1_pos, true_pos)
        code.update_jump(cmp2_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _expression(code: Code, expression):
    t = expression[1]

    if expression[0] == Node.UMINUS:
        _exp_uminus(code, expression)
    elif expression[0] == Node.UPLUS:
        _exp_uplus(code, expression)
    elif expression[0] == Node.MUL:
        _exp_mul(code, expression)
    elif expression[0] == Node.DIV:
        _exp_div(code, expression)
    elif expression[0] == Node.PLUS:
        _exp_plus(code, expression)
    elif expression[0] == Node.MINUS:
        _exp_minus(code, expression)
    elif expression[0] == Node.EQ:
        _exp_eq(code, expression)
    elif expression[0] == Node.NE:
        _exp_ne(code, expression)
    elif expression[0] == Node.LT:
        _exp_lt(code, expression)
    elif expression[0] == Node.GT:
        _exp_gt(code, expression)
    elif expression[0] == Node.LE:
        _exp_le(code, expression)
    elif expression[0] == Node.GE:
        _exp_ge(code, expression)
    elif expression[0] == Node.NOT:
        _exp_not(code, expression)
    elif expression[0] == Node.AND:
        _exp_and(code, expression)
    elif expression[0] == Node.OR:
        _exp_or(code, expression)
    else:
        raise NotImplementedError()


def _generate_clinit(cls: Class, constants):
    clinit = cls.method(J_CLINIT_NAME, J_CLINIT_DESCRIPTOR)
    code = clinit.code

    for c in constants:
        name = c[1]
        const_type = c[2]
        expression = c[3]
        descriptor = _create_field_descriptor(const_type)

        cls.field(name, descriptor)
        _expression(code, expression)


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

    _generate_main(cls, class_name)
    _generate_clinit(cls, constants)
    _generate_functions(cls, functions)

    return cls
