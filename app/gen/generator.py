from typing import Optional, List, Dict

from app.gen.code import Code
from app.gen.descriptor import ArrayDesc, FieldDescriptor, IntDesc, DoubleDesc, BooleanDesc, ClassDesc, \
    MethodDescriptor
from app.gen.predefined import J_CLINIT_NAME, J_CLINIT_DESCRIPTOR, JC_STRING, J_MAIN_NAME, J_MAIN_DESCRIPTOR
from app.gen.struct import Class
from app.names import FN_MAIN, MAIN_PARAMS, MAIN_RETURN, BOOL_INT_FALSE, BOOL_INT_TRUE
from app.types import TypeInt, TypeReal, TypeBool, TypeStr, Type, TypeArray
from app.syntax import Node


_variables: Dict[str, int] = {}


def _create_field_descriptor(t: Type) -> FieldDescriptor:
    if isinstance(t, TypeInt):
        return IntDesc()
    elif isinstance(t, TypeReal):
        return DoubleDesc()
    elif isinstance(t, TypeBool):
        return BooleanDesc()
    elif isinstance(t, TypeStr):
        return ClassDesc(JC_STRING)
    elif isinstance(t, TypeArray):
        if isinstance(t.inner, TypeInt):
            inner = IntDesc()
        elif isinstance(t.inner, TypeReal):
            inner = DoubleDesc()
        elif isinstance(t.inner, TypeBool):
            inner = BooleanDesc()
        elif isinstance(t.inner, TypeStr):
            inner = ClassDesc(JC_STRING)
        else:
            raise NotImplementedError()

        return ArrayDesc(t.dim, inner)
    else:
        raise NotImplementedError()


def _create_method_descriptor(params: List[Type], ret: Optional[Type]) -> MethodDescriptor:
    params_desc = [_create_field_descriptor(p) for p in params]
    ret_desc = None if ret is None else _create_field_descriptor(ret)
    return MethodDescriptor(params_desc, ret_desc)


def _statement_while(code: Code, statement):
    condition = statement[1]
    block = statement[2]

    start = code.pos()
    _expression(code, condition)
    cond_pos = code.pos()
    code.if_eq()

    breaks = []
    for s in block:
        _statement(code, s, start, breaks)

    end_pos = code.pos()
    code.update_jump(cond_pos, end_pos)
    for b in breaks:
        code.update_jump(b, end_pos)


def _statement_if(code: Code, statement):
    condition = statement[1]
    block = statement[2]

    _expression(code, condition)
    cond_pos = code.pos()
    code.if_eq()

    for s in block:
        _statement(code, s)

    end_pos = code.pos()
    code.update_jump(cond_pos, end_pos)


def _statement_if_else(code: Code, statement):
    condition = statement[1]
    if_block = statement[2]
    else_block = statement[3]

    _expression(code, condition)
    cond_pos = code.pos()
    code.if_eq()

    for s in if_block:
        _statement(code, s)

    goto_pos = code.pos()
    code.goto()

    else_pos = code.pos()
    for s in else_block:
        _statement(code, s)

    end_pos = code.pos()

    code.update_jump(cond_pos, else_pos)
    code.update_jump(goto_pos, end_pos)


def _statement_return(code: Code, statement):
    expression = statement[1]
    t = statement[2]

    if expression:
        _expression(code, expression)

    if t is None:
        code.return_void()
    elif isinstance(t, TypeInt):
        code.return_int()
    elif isinstance(t, TypeReal):
        code.return_double()
    elif isinstance(t, TypeBool):
        code.return_int()
    elif isinstance(t, TypeStr):
        code.return_reference()
    elif isinstance(t, TypeArray):
        code.return_reference()
    else:
        raise NotImplementedError()


def _statement_var_def(code: Code, statement):
    name = statement[1]
    t = statement[2]
    expression = statement[3]

    _expression(code, expression)

    if isinstance(t, TypeInt):
        index = code.variable_int()
        code.store_int(index)
    elif isinstance(t, TypeReal):
        index = code.variable_double()
        code.store_double(index)
    elif isinstance(t, TypeBool):
        index = code.variable_int()
        code.store_int(index)
    elif isinstance(t, TypeStr):
        index = code.variable_reference()
        code.store_reference(index)
    elif isinstance(t, TypeArray):
        index = code.variable_reference()
        code.store_reference(index)
    else:
        raise NotImplementedError()

    _variables[name] = index


def _statement_var_store(code: Code, exp):
    name = exp[1]
    expression = exp[2]
    t = exp[3]

    index = _variables[name]

    _expression(code, expression)

    if isinstance(t, TypeInt):
        code.store_int(index)
    if isinstance(t, TypeReal):
        code.store_double(index)
    if isinstance(t, TypeBool):
        code.store_int(index)
    if isinstance(t, TypeStr):
        code.store_reference(index)
    if isinstance(t, TypeArray):
        code.store_reference(index)


def _statement_array_store(code: Code, exp):
    name = exp[1]
    index_exps = exp[2]
    expression = exp[3]
    t = exp[4]

    # top array load
    index = _variables[name]
    code.load_reference(index)

    # subarrays load if multidim
    for e in index_exps[:-1]:
        _expression(code, e)
        code.array_load_reference()

    # item store
    _expression(code, index_exps[-1])
    _expression(code, expression)
    if isinstance(t.inner, TypeInt):
        code.array_store_int()
    if isinstance(t.inner, TypeReal):
        code.array_store_double()
    if isinstance(t.inner, TypeBool):
        code.array_store_boolean()
    if isinstance(t.inner, TypeStr):
        code.array_store_reference()
    if isinstance(t.inner, TypeArray):
        code.array_store_reference()


def _statement_function_call(code: Code, exp):
    name = exp[1]
    index_exps = exp[2]
    expression = exp[3]
    t = exp[4]

    # top array load
    index = _variables[name]
    code.load_reference(index)

    # subarrays load if multidim
    for e in index_exps[:-1]:
        _expression(code, e)
        code.array_load_reference()

    # item store
    _expression(code, index_exps[-1])
    _expression(code, expression)
    if isinstance(t.inner, TypeInt):
        code.array_store_int()
    if isinstance(t.inner, TypeReal):
        code.array_store_double()
    if isinstance(t.inner, TypeBool):
        code.array_store_boolean()
    if isinstance(t.inner, TypeStr):
        code.array_store_reference()
    if isinstance(t.inner, TypeArray):
        code.array_store_reference()


def _statement(code: Code, statement, loop_start: Optional[int] = None, breaks: Optional[List[int]] = None):
    if statement[0] == Node.VARIABLE_DEFINITION:
        _statement_var_def(code, statement)
    elif statement[0] == Node.CONSTANT_DEFINITION:
        _statement_var_def(code, statement)
    elif statement[0] == Node.VARIABLE_STORE:
        _statement_var_store(code, statement)
    elif statement[0] == Node.ARRAY_STORE:
        _statement_array_store(code, statement)
    elif statement[0] == Node.FUNCTION_CALL:
        _statement_function_call(code, statement)
    elif statement[0] == Node.RETURN:
        _statement_return(code, statement)
    elif statement[0] == Node.IF:
        _statement_if(code, statement)
    elif statement[0] == Node.IF_ELSE:
        _statement_if_else(code, statement)
    elif statement[0] == Node.WHILE:
        _statement_while(code, statement)
    elif statement[0] == Node.BREAK:
        break_pos = code.pos()
        code.goto()
        breaks.append(break_pos)
    elif statement[0] == Node.CONTINUE:
        code.goto(loop_start)
    else:
        raise NotImplementedError()


def _exp_uminus(code: Code, exp):
    right = exp[1]
    t = exp[2]
    _expression(code, right)

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
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

    if isinstance(t, TypeInt):
        code.mul_int()
    elif isinstance(t, TypeReal):
        code.mul_double()
    else:
        NotImplementedError()


def _exp_div(code: Code, exp):
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

    if isinstance(t, TypeInt):
        code.div_int()
    elif isinstance(t, TypeReal):
        code.div_double()
    else:
        NotImplementedError()


def _exp_plus(code: Code, exp):
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

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
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

    if isinstance(t, TypeInt):
        code.sub_int()
    elif isinstance(t, TypeReal):
        code.sub_double()
    else:
        NotImplementedError()


def _exp_sub(code: Code, exp):
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

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
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

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
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

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
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

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
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

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
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

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
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

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
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

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
    left = exp[1]
    right = exp[2]
    t = exp[3]
    _expression(code, left)
    _expression(code, right)

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


def _exp_var_load(code: Code, exp):
    name = exp[1]
    t = exp[2]

    index = _variables[name]

    if isinstance(t, TypeInt):
        code.load_int(index)
    if isinstance(t, TypeReal):
        code.load_double(index)
    if isinstance(t, TypeBool):
        code.load_int(index)
    if isinstance(t, TypeStr):
        code.load_reference(index)
    if isinstance(t, TypeArray):
        code.load_reference(index)


def _exp_array_load(code: Code, exp):
    array_exp = exp[1]
    index_exps = exp[2]
    t = exp[3]

    _expression(code, array_exp)

    # subarrays load if multidim
    for e in index_exps[:-1]:
        _expression(code, e)
        code.array_load_reference()

    # item load
    _expression(code, index_exps[-1])
    if isinstance(t, TypeInt):
        code.array_load_int()
    if isinstance(t, TypeReal):
        code.array_load_double()
    if isinstance(t, TypeBool):
        code.array_load_boolean()
    if isinstance(t, TypeStr):
        code.array_load_reference()
    if isinstance(t, TypeArray):
        code.array_load_reference()


def _exp_value_array(code: Code, exp):
    expressions = exp[1]
    t = exp[2]

    if t.dim > 1:
        desc = _create_field_descriptor(TypeArray(t.dim - 1, t.inner))
    else:
        desc = _create_field_descriptor(t.inner)

    code.new_array(desc)

    for (i, e) in enumerate(expressions):
        code.dup()
        code.const_int(i)
        _expression(code, e)
        if isinstance(t.inner, TypeInt):
            code.array_store_int()
        if isinstance(t.inner, TypeReal):
            code.array_store_double()
        if isinstance(t.inner, TypeBool):
            code.array_store_boolean()
        if isinstance(t.inner, TypeStr):
            code.array_store_reference()
        if isinstance(t.inner, TypeArray):
            code.array_store_reference()


def _exp_var_assign(code: Code, exp):
    name = exp[1]
    expression = exp[2]
    t = exp[3]

    index = _variables[name]

    _expression(code, expression)

    if isinstance(t, TypeInt):
        code.dup()
        code.store_int(index)
    if isinstance(t, TypeReal):
        code.dup2()
        code.store_double(index)
    if isinstance(t, TypeBool):
        code.dup()
        code.store_int(index)
    if isinstance(t, TypeStr):
        code.dup()
        code.store_reference(index)
    if isinstance(t, TypeArray):
        code.dup()
        code.store_reference(index)


def _exp_array_assign(code: Code, exp):
    name = exp[1]
    index_exps = exp[2]
    expression = exp[3]
    t = exp[4]

    # top array load
    index = _variables[name]
    code.load_reference(index)

    # subarrays load if multidim
    for e in index_exps[:-1]:
        _expression(code, e)
        code.array_load_reference()

    # item store
    _expression(code, index_exps[-1])
    _expression(code, expression)
    if isinstance(t.inner, TypeInt):
        code.dup()
        code.array_store_int()
    if isinstance(t.inner, TypeReal):
        code.dup2()
        code.array_store_double()
    if isinstance(t.inner, TypeBool):
        code.dup()
        code.array_store_boolean()
    if isinstance(t.inner, TypeStr):
        code.dup()
        code.array_store_reference()
    if isinstance(t.inner, TypeArray):
        code.dup()
        code.array_store_reference()


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
    elif expression[0] == Node.VARIABLE_LOAD:
        _exp_var_load(code, expression)
    elif expression[0] == Node.ARRAY_LOAD:
        _exp_array_load(code, expression)
    elif expression[0] == Node.VARIABLE_ASSIGNMENT:
        _exp_var_assign(code, expression)
    elif expression[0] == Node.ARRAY_ASSIGNMENT:
        _exp_array_assign(code, expression)
    elif expression[0] == Node.VALUE_INT:
        code.const_int(expression[1])
    elif expression[0] == Node.VALUE_REAL:
        code.const_double(expression[1])
    elif expression[0] == Node.VALUE_BOOL:
        code.const_int(int(expression[1]))
    elif expression[0] == Node.VALUE_STR:
        code.const_string(expression[1])
    elif expression[0] == Node.VALUE_ARRAY:
        _exp_value_array(expression)
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
        _variables.clear()

        name = f[1]
        params = f[2]
        ret = f[3]
        statements = f[4]

        method_desc = _create_method_descriptor(params, ret)

        method = cls.method(name, method_desc)
        for s in statements:
            _statement(method.code, s)


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
