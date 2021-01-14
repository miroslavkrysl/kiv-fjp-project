from typing import Optional, List, Dict, Tuple

from app.gen.code import Code
from app.gen.descriptor import ArrayDesc, FieldDescriptor, IntDesc, DoubleDesc, BooleanDesc, ClassDesc, \
    MethodDescriptor
from app.gen.predefined import J_CLINIT_NAME, J_CLINIT_DESCRIPTOR, JC_STRING, J_MAIN_NAME, J_MAIN_DESCRIPTOR, \
    JM_STRING_LENGTH, JSM_INT_TO_STRING, JSM_INT_PARSE, JSM_BOOLEAN_PARSE, JSM_DOUBLE_PARSE, JSM_DOUBLE_TO_STRING, \
    JSM_BOOLEAN_TO_STRING, JSF_STDIN, JM_PRINT, JSF_STDOUT, JC_BUFF_READER, JM_READLINE, JM_STRING_CONCAT, \
    JM_STRING_EQUALS, JC_INPUT_STREAM_READER, JIM_INPUT_STREAM_READER, JIM_BUFF_READER, JM_STRING_SUBSTRING
from app.gen.structs import Class, Method
from app.sem.predefined import FN_MAIN, FN_MAIN_PARAMS, FN_MAIN_RETURN, FN_LEN, FN_INT, \
    FN_REAL, FN_BOOL, FN_STR, FN_WRITE, FN_READ_LINE, FN_SUBSTRING, FN_EOF
from app.lang_types import TypeInt, TypeReal, TypeBool, TypeStr, Type, TypeArray, TypeVoid
from app.syntax import Node


BUFF_READER_FIELD = '$input'
EOF_FIELD = '$eof'

_locals: Dict[str, int]
_fields: Dict[str, Tuple[str, str, FieldDescriptor]]
_class_name: str
_class: Class
_clinit: Method


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
        raise NotImplementedError(t)


def _create_method_descriptor(params: List[Type], ret: Optional[Type]) -> MethodDescriptor:
    params_desc = [_create_field_descriptor(p) for p in params]
    ret_desc = None if ret is None else _create_field_descriptor(ret)
    return MethodDescriptor(params_desc, ret_desc)


def _statement_while(code: Code, statement):
    condition = statement['condition']
    statements = statement['statements']

    start = code.pos()
    _expression(code, condition)
    cond_pos = code.pos()
    code.if_eq()

    breaks = []
    for s in statements:
        _statement(code, s, start, breaks)

    end_pos = code.pos()
    code.update_jump(cond_pos, end_pos)
    for b in breaks:
        code.update_jump(b, end_pos)


def _statement_if(code: Code, statement):
    condition = statement['condition']
    statements = statement['statements']

    _expression(code, condition)
    cond_pos = code.pos()
    code.if_eq()

    for s in statements:
        _statement(code, s)

    end_pos = code.pos()
    code.update_jump(cond_pos, end_pos)


def _statement_if_else(code: Code, statement):
    condition = statement['condition']
    if_statements = statement['if_statements']
    else_statements = statement['else_statements']

    _expression(code, condition)
    cond_pos = code.pos()
    code.if_eq()

    for s in if_statements:
        _statement(code, s)

    goto_pos = code.pos()
    code.goto()

    else_pos = code.pos()
    for s in else_statements:
        _statement(code, s)

    end_pos = code.pos()

    code.update_jump(cond_pos, else_pos)
    code.update_jump(goto_pos, end_pos)


def _statement_return(code: Code, statement):
    expression = statement['expression']
    t = statement['type']

    if expression:
        _expression(code, expression)

    if isinstance(t, TypeVoid):
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
    name = statement['name']
    t = statement['type']
    expression = statement['expression']

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

    _locals[name] = index


def _function_def(statement):
    name = statement['name']
    params = statement['parameters']
    ret = statement['return']
    statements = statement['statements']

    method_desc = _create_method_descriptor([p['type'] for p in params], ret['type'])

    method = _class.method(name, method_desc)

    # initialize method parameters
    for p in params:
        t = p['type']
        if isinstance(t, TypeInt):
            index = method.code.variable_int()
        elif isinstance(t, TypeReal):
            index = method.code.variable_double()
        elif isinstance(t, TypeBool):
            index = method.code.variable_int()
        elif isinstance(t, TypeStr):
            index = method.code.variable_reference()
        elif isinstance(t, TypeArray):
            index = method.code.variable_reference()
        else:
            raise NotImplementedError()

        _locals[name] = index

    for s in statements:
        _statement(method.code, s)


def _constant_def(statement):
    name = statement['name']
    const_type = statement['type']
    expression = statement['expression']
    descriptor = _create_field_descriptor(const_type)

    code = _clinit.code

    _fields[name] = (_class_name, name, descriptor)
    _class.field(name, descriptor)
    _expression(code, expression)
    code.store_static_field(_class_name, name, descriptor)


def _statement_var_store(code: Code, exp):
    name = exp['name']
    expression = exp['expression']
    t = exp['type']

    index = _locals[name]

    _expression(code, expression)

    if isinstance(t, TypeInt):
        code.store_int(index)
    elif isinstance(t, TypeReal):
        code.store_double(index)
    elif isinstance(t, TypeBool):
        code.store_int(index)
    elif isinstance(t, TypeStr):
        code.store_reference(index)
    elif isinstance(t, TypeArray):
        code.store_reference(index)
    else:
        raise NotImplementedError()


def _statement_array_store(code: Code, exp):
    name = exp['name']
    index_exps = exp['indexes']
    expression = exp['expression']
    t = exp['type']

    # top array load
    index = _locals[name]
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
    elif isinstance(t.inner, TypeReal):
        code.array_store_double()
    elif isinstance(t.inner, TypeBool):
        code.array_store_boolean()
    elif isinstance(t.inner, TypeStr):
        code.array_store_reference()
    elif isinstance(t.inner, TypeArray):
        code.array_store_reference()
    else:
        raise NotImplementedError()


def _statement_function_call(code: Code, exp):
    ret = exp['return_type']
    _exp_function_call(code, exp)

    if isinstance(ret, TypeInt) \
            or isinstance(ret, TypeBool) \
            or isinstance(ret, TypeStr) \
            or isinstance(ret, TypeArray):
        code.pop()
    elif isinstance(ret, TypeReal):
        code.pop2()


def _top_statement(statement):
    node_type = statement['node']

    if node_type == Node.FUNCTION_DEFINITION:
        _function_def(statement)
    elif node_type == Node.CONSTANT_DEFINITION:
        _constant_def(statement)
    else:
        raise NotImplementedError()


def _statement(code: Code, statement, loop_start: Optional[int] = None, breaks: Optional[List[int]] = None):
    node_type = statement['node']

    if node_type == Node.VARIABLE_DEFINITION:
        _statement_var_def(code, statement)
    elif node_type == Node.CONSTANT_DEFINITION:
        _statement_var_def(code, statement)
    elif node_type == Node.VARIABLE_STORE:
        _statement_var_store(code, statement)
    elif node_type == Node.ARRAY_STORE:
        _statement_array_store(code, statement)
    elif node_type == Node.FUNCTION_CALL:
        _statement_function_call(code, statement)
    elif node_type == Node.RETURN:
        _statement_return(code, statement)
    elif node_type == Node.IF:
        _statement_if(code, statement)
    elif node_type == Node.IF_ELSE:
        _statement_if_else(code, statement)
    elif node_type == Node.WHILE:
        _statement_while(code, statement)
    elif node_type == Node.BREAK:
        break_pos = code.pos()
        code.goto()
        breaks.append(break_pos)
    elif node_type == Node.CONTINUE:
        code.goto(loop_start)
    else:
        raise NotImplementedError()


def _exp_uminus(code: Code, exp):
    expression = exp['expression']
    t = exp['type']
    _expression(code, expression)

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
    left = exp['left']
    right = exp['right']
    t = exp['type']
    _expression(code, left)
    _expression(code, right)

    if isinstance(t, TypeInt):
        code.mul_int()
    elif isinstance(t, TypeReal):
        code.mul_double()
    else:
        NotImplementedError()


def _exp_div(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
    _expression(code, left)
    _expression(code, right)

    if isinstance(t, TypeInt):
        code.div_int()
    elif isinstance(t, TypeReal):
        code.div_double()
    else:
        NotImplementedError()


def _exp_plus(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
    _expression(code, left)
    _expression(code, right)

    if isinstance(t, TypeInt):
        code.add_int()
    elif isinstance(t, TypeReal):
        code.add_double()
    elif isinstance(t, TypeStr):
        code.invoke_virtual(*JM_STRING_CONCAT)
    else:
        NotImplementedError()


def _exp_minus(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
    _expression(code, left)
    _expression(code, right)

    if isinstance(t, TypeInt):
        code.sub_int()
    elif isinstance(t, TypeReal):
        code.sub_double()
    else:
        NotImplementedError()


def _exp_sub(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
    _expression(code, left)
    _expression(code, right)

    if isinstance(t, TypeInt):
        code.add_int()
    elif isinstance(t, TypeReal):
        code.add_double()
    else:
        NotImplementedError()


def _exp_eq(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
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
        code.const_int(0)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(1)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    elif isinstance(t, TypeStr):
        code.invoke_virtual(*JM_STRING_EQUALS)
    else:
        NotImplementedError()


def _exp_ne(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
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
        code.const_int(0)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(1)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    elif isinstance(t, TypeStr):
        code.invoke_virtual(*JM_STRING_EQUALS)
        cmp_pos = code.pos()
        code.if_eq()
        code.const_int(0)
        goto_pos = code.pos()
        code.goto()
        false_pos = code.pos()
        code.const_int(1)
        end_pos = code.pos()

        code.update_jump(cmp_pos, false_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_lt(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
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
        code.const_int(0)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(1)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_gt(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
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
        code.const_int(0)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(1)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_le(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
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
        code.const_int(0)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(1)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_ge(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
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
        code.const_int(0)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(1)
        end_pos = code.pos()

        code.update_jump(cmp_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_not(code: Code, exp):
    r = exp[2]
    t = exp['type']
    _expression(code, r)

    if isinstance(t, TypeBool):
        cmp_pos = code.pos()
        code.if_eq()
        code.const_int(0)
        goto_pos = code.pos()
        code.goto()
        false_pos = code.pos()
        code.const_int(1)
        end_pos = code.pos()

        code.update_jump(cmp_pos, false_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_and(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
    _expression(code, left)
    _expression(code, right)

    if isinstance(t, TypeBool):
        cmp1_pos = code.pos()
        code.if_eq()
        cmp2_pos = code.pos()
        code.if_eq()
        code.const_int(1)
        goto_pos = code.pos()
        code.goto()
        false_pos = code.pos()
        code.const_int(0)
        end_pos = code.pos()

        code.update_jump(cmp1_pos, false_pos)
        code.update_jump(cmp2_pos, false_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_or(code: Code, exp):
    left = exp['left']
    right = exp['right']
    t = exp['type']
    _expression(code, left)
    _expression(code, right)

    if isinstance(t, TypeBool):
        cmp1_pos = code.pos()
        code.if_ne()
        cmp2_pos = code.pos()
        code.if_ne()
        code.const_int(0)
        goto_pos = code.pos()
        code.goto()
        true_pos = code.pos()
        code.const_int(1)
        end_pos = code.pos()

        code.update_jump(cmp1_pos, true_pos)
        code.update_jump(cmp2_pos, true_pos)
        code.update_jump(goto_pos, end_pos)
    else:
        NotImplementedError()


def _exp_var_load(code: Code, exp):
    name = exp['name']
    t = exp['type']

    index = _locals.get(name)
    if index:
        if isinstance(t, TypeInt):
            code.load_int(index)
        elif isinstance(t, TypeReal):
            code.load_double(index)
        elif isinstance(t, TypeBool):
            code.load_int(index)
        elif isinstance(t, TypeStr):
            code.load_reference(index)
        elif isinstance(t, TypeArray):
            code.load_reference(index)
        else:
            raise NotImplementedError()
    else:
        field = _fields.get(name)
        code.load_field(field[0], field[1], field[2])


def _exp_array_load(code: Code, exp):
    array_exp = exp['expression']
    index_exps = exp['indexes']
    t = exp['type']

    _expression(code, array_exp)

    # subarrays load if multidim
    for e in index_exps[:-1]:
        _expression(code, e)
        code.array_load_reference()

    # item load
    _expression(code, index_exps[-1])
    if isinstance(t, TypeInt):
        code.array_load_int()
    elif isinstance(t, TypeReal):
        code.array_load_double()
    elif isinstance(t, TypeBool):
        code.array_load_boolean()
    elif isinstance(t, TypeStr):
        code.array_load_reference()
    elif isinstance(t, TypeArray):
        code.array_load_reference()
    else:
        raise NotImplementedError()


def _exp_value_array(code: Code, exp):
    items = exp['items']
    t = exp['type']

    if t.dim > 1:
        desc = _create_field_descriptor(TypeArray(t.dim - 1, t.inner))
    else:
        desc = _create_field_descriptor(t.inner)

    code.new_array(desc)

    for (i, item) in enumerate(items):
        code.dup()
        code.const_int(i)
        _expression(code, item)
        if isinstance(t.inner, TypeInt):
            code.array_store_int()
        elif isinstance(t.inner, TypeReal):
            code.array_store_double()
        elif isinstance(t.inner, TypeBool):
            code.array_store_boolean()
        elif isinstance(t.inner, TypeStr):
            code.array_store_reference()
        elif isinstance(t.inner, TypeArray):
            code.array_store_reference()
        else:
            raise NotImplementedError()


def _exp_var_assign(code: Code, exp):
    name = exp['name']
    expression = exp['expression']
    t = exp['type']

    index = _locals[name]
    _expression(code, expression)

    if isinstance(t, TypeInt):
        code.dup()
        code.store_int(index)
    elif isinstance(t, TypeReal):
        code.dup2()
        code.store_double(index)
    elif isinstance(t, TypeBool):
        code.dup()
        code.store_int(index)
    elif isinstance(t, TypeStr):
        code.dup()
        code.store_reference(index)
    elif isinstance(t, TypeArray):
        code.dup()
        code.store_reference(index)
    else:
        raise NotImplementedError()


def _exp_array_assign(code: Code, exp):
    name = exp['name']
    index_exps = exp['indexes']
    expression = exp['expression']
    t = exp['type']

    # top array load
    index = _locals[name]
    code.load_reference(index)

    # subarrays load if multidim
    for e in index_exps[:-1]:
        _expression(code, e)
        code.array_load_reference()

    # item store
    _expression(code, index_exps[-1])
    _expression(code, expression)
    if isinstance(t.inner, TypeInt):
        code.dup_x1()
        code.array_store_int()
    elif isinstance(t.inner, TypeReal):
        code.dup2_x1()
        code.array_store_double()
    elif isinstance(t.inner, TypeBool):
        code.dup_x1()
        code.array_store_boolean()
    elif isinstance(t.inner, TypeStr):
        code.dup_x1()
        code.array_store_reference()
    elif isinstance(t.inner, TypeArray):
        code.dup_x1()
        code.array_store_reference()
    else:
        raise NotImplementedError()


def _exp_function_call(code: Code, exp):
    name = exp['name']
    args_exps = exp['arguments']
    params = exp['parameters_types']
    ret = exp['return_type']

    for e in args_exps:
        _expression(code, e)

    # check for predefined functions
    if name == FN_LEN and len(params) == 1:
        if isinstance(params[0], TypeStr):
            code.invoke_virtual(*JM_STRING_LENGTH)
            return
        elif isinstance(params[0], TypeArray):
            code.array_length()
            return

    if name == FN_INT and len(params) == 1:
        if isinstance(params[0], TypeInt):
            # nothing to do
            return
        elif isinstance(params[0], TypeReal):
            code.double_to_int()
            return
        elif isinstance(params[0], TypeBool):
            # nothing to do
            return
        elif isinstance(params[0], TypeStr):
            code.invoke_static(*JSM_INT_PARSE)
            return

    if name == FN_REAL and len(params) == 1:
        if isinstance(params[0], TypeInt):
            code.int_to_double()
            return
        elif isinstance(params[0], TypeReal):
            # nothing to do
            return
        elif isinstance(params[0], TypeBool):
            code.int_to_double()
            return
        elif isinstance(params[0], TypeStr):
            code.invoke_static(*JSM_DOUBLE_PARSE)
            return

    if name == FN_BOOL and len(params) == 1:
        if isinstance(params[0], TypeInt):
            code.const_int(1)
            code.add_int()
            return
        elif isinstance(params[0], TypeReal):
            code.const_double(0.0)
            code.cmp_double_l()
            cmp_pos = code.pos()
            code.if_eq()
            code.const_int(1)
            goto_pos = code.pos()
            code.goto()
            false_pos = code.pos()
            code.const_int(0)
            end_pos = code.pos()

            code.update_jump(cmp_pos, false_pos)
            code.update_jump(goto_pos, end_pos)
            return
        elif isinstance(params[0], TypeBool):
            # nothing to do
            return
        elif isinstance(params[0], TypeStr):
            code.invoke_static(*JSM_BOOLEAN_PARSE)
            return

    if name == FN_STR and len(params) == 1:
        if isinstance(params[0], TypeInt):
            code.invoke_static(*JSM_INT_TO_STRING)
            return
        elif isinstance(params[0], TypeReal):
            code.invoke_static(*JSM_DOUBLE_TO_STRING)
            return
        elif isinstance(params[0], TypeBool):
            code.invoke_static(*JSM_BOOLEAN_TO_STRING)
            return

    if name == FN_SUBSTRING and len(params) == 3:
        if isinstance(params[0], TypeStr) and isinstance(params[1], TypeInt) and isinstance(params[2], TypeInt):
            code.invoke_static(*JM_STRING_SUBSTRING)
            return

    if name == FN_WRITE and len(params) == 1:
        if isinstance(params[0], TypeStr):
            code.load_static_field(*JSF_STDOUT)
            code.swap()
            code.invoke_virtual(*JM_PRINT)
            return

    if name == FN_READ_LINE and len(params) == 0:
        code.load_static_field(_class_name, BUFF_READER_FIELD, ClassDesc(JC_BUFF_READER))
        code.swap()
        code.invoke_virtual(*JM_READLINE)

        # if result null, set the eof field to true and load empty string
        cmp_pos = code.pos()
        code.if_non_null()
        code.const_int(1)
        code.store_static_field(_class_name, EOF_FIELD, BooleanDesc())
        code.const_string('')
        end_pos = code.pos()
        code.update_jump(cmp_pos, end_pos)
        return

    if name == FN_EOF and len(params) == 0:
        code.load_static_field(_class_name, EOF_FIELD, BooleanDesc())
        return

    # custom function
    desc = _create_method_descriptor(params, ret)
    code.invoke_static(_class_name, name, desc)


def _expression(code: Code, expression):
    node_type = expression['node']

    if node_type == Node.UMINUS:
        _exp_uminus(code, expression)
    elif node_type == Node.UPLUS:
        _exp_uplus(code, expression)
    elif node_type == Node.MUL:
        _exp_mul(code, expression)
    elif node_type == Node.DIV:
        _exp_div(code, expression)
    elif node_type == Node.PLUS:
        _exp_plus(code, expression)
    elif node_type == Node.MINUS:
        _exp_minus(code, expression)
    elif node_type == Node.EQ:
        _exp_eq(code, expression)
    elif node_type == Node.NE:
        _exp_ne(code, expression)
    elif node_type == Node.LT:
        _exp_lt(code, expression)
    elif node_type == Node.GT:
        _exp_gt(code, expression)
    elif node_type == Node.LE:
        _exp_le(code, expression)
    elif node_type == Node.GE:
        _exp_ge(code, expression)
    elif node_type == Node.NOT:
        _exp_not(code, expression)
    elif node_type == Node.AND:
        _exp_and(code, expression)
    elif node_type == Node.OR:
        _exp_or(code, expression)
    elif node_type == Node.VARIABLE_LOAD:
        _exp_var_load(code, expression)
    elif node_type == Node.ARRAY_LOAD:
        _exp_array_load(code, expression)
    elif node_type == Node.VARIABLE_ASSIGNMENT:
        _exp_var_assign(code, expression)
    elif node_type == Node.ARRAY_ASSIGNMENT:
        _exp_array_assign(code, expression)
    elif node_type == Node.VALUE_INT:
        code.const_int(expression['value'])
    elif node_type == Node.VALUE_REAL:
        code.const_double(expression['value'])
    elif node_type == Node.VALUE_BOOL:
        code.const_int(int(expression['value']))
    elif node_type == Node.VALUE_STR:
        code.const_string(expression['value'])
    elif node_type == Node.VALUE_ARRAY:
        _exp_value_array(code, expression)
    elif node_type == Node.FUNCTION_CALL_VALUE:
        _exp_function_call(code, expression)
    else:
        raise NotImplementedError()


def _generate_clinit():
    global _fields
    global _clinit
    _fields = {}

    _clinit = _class.method(J_CLINIT_NAME, J_CLINIT_DESCRIPTOR)
    code = _clinit.code

    # generate eof indicator
    _class.field(EOF_FIELD, BooleanDesc())
    code.const_int(0)
    code.store_static_field(_class_name, EOF_FIELD, BooleanDesc())

    # generate input buff reader
    _class.field(BUFF_READER_FIELD, ClassDesc(JC_BUFF_READER))
    code.new(JC_BUFF_READER)
    code.dup()
    code.new(JC_INPUT_STREAM_READER)
    code.dup()
    code.load_static_field(*JSF_STDIN)
    code.invoke_special(*JIM_INPUT_STREAM_READER)
    code.invoke_special(*JIM_BUFF_READER)
    code.store_static_field(_class_name, BUFF_READER_FIELD, ClassDesc(JC_BUFF_READER))


def _close_clinit():
    code = _clinit.code
    code.return_void()


def _generate_main():
    method = _class.method(J_MAIN_NAME, J_MAIN_DESCRIPTOR)
    method.code.invoke_static(_class_name, FN_MAIN, _create_method_descriptor(FN_MAIN_PARAMS, FN_MAIN_RETURN))
    method.code.return_void()


def generate(class_name: str, ast) -> Class:
    global _class_name
    global _fields
    global _locals
    global _class

    _locals = {}
    _fields = {}

    _class_name = class_name
    _class_name = class_name
    _class = Class(class_name)

    _generate_clinit()

    for node in ast['statements']:
        _top_statement(node)

    _generate_main()
    _close_clinit()

    return _class
