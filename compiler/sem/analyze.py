# Here goes AST analyze process
from typing import List, Optional, Tuple, Iterable

from compiler.sem.predefined import FN_MAIN, FN_MAIN_PARAMS, FN_MAIN_RETURN, FN_LEN, FN_INT, FN_REAL, FN_BOOL, FN_STR, \
    FN_SUBSTRING, FN_WRITE, FN_READ_LINE, FN_EOF
from compiler.syntax.ast import Node
from compiler.lang_types import Type, TypeInt, TypeReal, TypeStr, TypeBool, TypeArray, TypeAny, BaseType, TypeVoid
from compiler.util import is_int

_vars = []  # Key = depth, Value => Key = identifier, Value = (type, is constant)

# Key = (identifier, tuple of params types), Value = return type
_functions = {
    (FN_LEN, (TypeStr(),)): TypeInt(),

    (FN_INT, (TypeInt(),)): TypeInt(),
    (FN_INT, (TypeReal(),)): TypeInt(),
    (FN_INT, (TypeBool(),)): TypeInt(),
    (FN_INT, (TypeStr(),)): TypeInt(),

    (FN_REAL, (TypeInt(),)): TypeReal(),
    (FN_REAL, (TypeReal(),)): TypeReal(),
    (FN_REAL, (TypeBool(),)): TypeReal(),
    (FN_REAL, (TypeStr(),)): TypeReal(),

    (FN_BOOL, (TypeInt(),)): TypeBool(),
    (FN_BOOL, (TypeReal(),)): TypeBool(),
    (FN_BOOL, (TypeBool(),)): TypeBool(),
    (FN_BOOL, (TypeStr(),)): TypeBool(),

    (FN_STR, (TypeInt(),)): TypeStr(),
    (FN_STR, (TypeReal(),)): TypeStr(),
    (FN_STR, (TypeBool(),)): TypeStr(),
    (FN_STR, (TypeStr(),)): TypeStr(),

    (FN_SUBSTRING, (TypeStr(), TypeInt(), TypeInt())): TypeStr(),

    (FN_WRITE, (TypeStr(),)): TypeVoid(),
    (FN_READ_LINE, ()): TypeStr(),
    (FN_EOF, ()): TypeBool(),
}

_errors = []

# table of allowed operand types for operators and their result types
# Key = operator_node_type => variants[([operand1, ...], result)]
ALLOWED_OPERATOR_TYPES = {
    Node.UMINUS: [
        ([TypeInt], TypeInt()),
        ([TypeReal], TypeReal())
    ],
    Node.UPLUS: [
        ([TypeInt], TypeInt()),
        ([TypeReal], TypeReal())
    ],
    Node.MUL: [
        ([TypeInt, TypeInt], TypeInt()),
        ([TypeReal, TypeReal], TypeReal())
    ],
    Node.DIV: [
        ([TypeInt, TypeInt], TypeInt()),
        ([TypeReal, TypeReal], TypeReal())
    ],
    Node.PLUS: [
        ([TypeInt, TypeInt], TypeInt()),
        ([TypeReal, TypeReal], TypeReal()),
        ([TypeStr, TypeStr], TypeStr())
    ],
    Node.MINUS: [
        ([TypeInt, TypeInt], TypeInt()),
        ([TypeReal, TypeReal], TypeReal())
    ],
    Node.EQ:  [
        ([TypeInt, TypeInt], TypeBool()),
        ([TypeReal, TypeReal], TypeBool()),
        ([TypeBool, TypeBool], TypeBool()),
        ([TypeStr, TypeStr], TypeBool())
    ],
    Node.NE: [
        ([TypeInt, TypeInt], TypeBool()),
        ([TypeReal, TypeReal], TypeBool()),
        ([TypeBool, TypeBool], TypeBool()),
        ([TypeStr, TypeStr], TypeBool())
    ],
    Node.LT: [
        ([TypeInt, TypeInt], TypeBool()),
        ([TypeReal, TypeReal], TypeBool())
    ],
    Node.GT: [
        ([TypeInt, TypeInt], TypeBool()),
        ([TypeReal, TypeReal], TypeBool())
    ],
    Node.LE: [
        ([TypeInt, TypeInt], TypeBool()),
        ([TypeReal, TypeReal], TypeBool())
    ],
    Node.GE: [
        ([TypeInt, TypeInt], TypeBool()),
        ([TypeReal, TypeReal], TypeBool())
    ],
    Node.NOT: [
        ([TypeBool], TypeBool())
    ],
    Node.AND: [
        ([TypeBool, TypeBool], TypeBool())
    ],
    Node.OR: [
        ([TypeBool, TypeBool], TypeBool())
    ]
}


def analyze(ast) -> bool:
    """
    Analyze the AST types, identifiers.
    :param ast: The AST.
    :return: List of errors None otherwise
    """
    # print("ANALYZING THE INPUT...")

    if _analyze_layer(ast['statements'], False):
        _check_main()

    for e in _errors:
        print(e)

    return len(_errors) == 0


def _check_main():
    fn = _get_func(FN_MAIN, FN_MAIN_PARAMS)
    if fn != FN_MAIN_RETURN:
        _errors.append("Missing main function.")


def _analyze_layer(statements, in_loop, return_type=None, params=None) -> bool:

    # Recursive limit stop
    if len(_vars) > 32:
        _errors.append("Depth overreached the limit of 32.")
        return False

    _vars.append({})
    ok = False

    if params:
        for p in params:
            name = p['name']
            t = p['type']
            var = _get_var(name)
            if var is not None:
                _errors.append(f'Variable \'{name}\' is already defined.')
                return False

            _add_var(name, t, False)

    # Go through the all statements in the current depth
    for statement in statements:
        # This print is just for debugging
        # print("{0}: {1}".format(len(_vars), statement))

        node_type = statement['node']

        # Function definition
        if node_type == Node.FUNCTION_DEFINITION:
            name = statement['name']
            params = statement['parameters']
            ret = statement['return']
            stmts = statement['statements']

            params_types = []
            for p in params:
                t = _node_to_type(p['type'])
                p['type'] = t
                params_types.append(t)

            fn = _get_func(name, params_types)
            if fn is not None:
                _errors.append(f'Function \'{name}({", ".join(str(t) for t in params_types)})\' is already defined.')
                break

            ret_type = _node_to_type(ret)
            ret['type'] = ret_type
            _add_func(name, params_types, ret_type)
            if not _analyze_layer(stmts, in_loop, ret_type, params):
                break
            if not _validate_function_returns(stmts, Node.RETURN_VOID if isinstance(ret_type, TypeVoid) else Node.RETURN):
                print(f'Function \'{name}({", ".join(str(t) for t in params_types)})\' may end without a return.')
                break

        # Variable and constant definition
        elif node_type == Node.CONSTANT_DEFINITION or node_type == Node.VARIABLE_DEFINITION:
            name = statement['name']
            t = statement['type']
            exp = statement['expression']

            var = _get_var(name)
            if var is not None:
                _errors.append(f'Variable \'{name}\' is already defined.')
                break
            exp_type = _validate_expression(exp)

            if exp_type is None:
                break

            var_type = _node_to_type(t)

            if var_type != exp_type:
                _errors.append(
                    f'Can not assign a value of type {exp_type} into variable \'{name}\' of type {var_type}.')

            statement['type'] = var_type
            _array_type_inference(exp, var_type)
            _add_var(name, var_type, node_type == Node.CONSTANT_DEFINITION)

        elif node_type == Node.VARIABLE_STORE:
            if _validate_var_store(statement) is None:
                break

        elif node_type == Node.ARRAY_STORE:
            if _validate_array_store(statement) is None:
                break

        # Function call
        elif node_type == Node.FUNCTION_CALL:
            if _validate_function_call(statement) is None:
                break

        # Condition (IF)
        elif node_type == Node.IF:
            condition = statement['condition']
            stmts = statement['statements']
            cond_type = _validate_expression(condition)

            if cond_type is None:
                break

            if cond_type != TypeBool():
                _errors.append(f'Condition expression ({cond_type}) is not of type Bool.')
                break

            if not _analyze_layer(stmts, in_loop, return_type):
                break

        # Condition (IF-ELSE)
        elif node_type == Node.IF_ELSE:
            condition = statement['condition']
            if_stmts = statement['if_statements']
            else_stmts = statement['else_statements']
            cond_type = _validate_expression(condition)

            if cond_type is None:
                break

            if cond_type != TypeBool():
                _errors.append(f'Condition expression ({cond_type}) is not of type Bool.')
                break

            if not _analyze_layer(if_stmts, in_loop, return_type):
                break
            if not _analyze_layer(else_stmts, in_loop, return_type):
                break

        # Loop (WHILE)
        elif node_type == Node.WHILE:
            condition = statement['condition']
            stmts = statement['statements']
            cond_type = _validate_expression(condition)

            if cond_type is None:
                break

            if cond_type != TypeBool():
                _errors.append(f'Condition expression ({cond_type}) is not of type Bool.')
                break

            if not _analyze_layer(stmts, True, return_type):
                break

        # Return keyword
        elif node_type == Node.RETURN or node_type == Node.RETURN_VOID:
            if node_type == Node.RETURN_VOID:
                exp_type = TypeVoid()
            else:
                exp = statement['expression']
                exp_type = _validate_expression(exp)

                if exp_type is None:
                    break

            if exp_type != return_type:
                _errors.append(
                    f'Return expression has a different type ({exp_type}) than the function ({return_type}).')
                break

            statement['type'] = exp_type

        # Break keyword
        elif node_type == Node.BREAK:
            if not in_loop:
                _errors.append('Break definition outside of a loop.')
                break

        # Continue keyword
        elif node_type == Node.CONTINUE:
            if not in_loop:
                _errors.append('Continue definition outside of a loop.')
                break
    else:
        ok = True

    _vars.pop()
    return ok


def _validate_expression(expression) -> Optional[Type]:
    """
    Validate expression,
    :param expression: The expression.
    :return: Result type or None on failure
    """
    node_type = expression['node']

    if node_type == Node.VALUE_INT \
            or node_type == Node.VALUE_REAL \
            or node_type == Node.VALUE_BOOL \
            or node_type == Node.VALUE_STR \
            or node_type == Node.VALUE_ARRAY:
        return _validate_value(expression)

    elif node_type == Node.UMINUS \
            or node_type == Node.UPLUS \
            or node_type == Node.MUL \
            or node_type == Node.DIV \
            or node_type == Node.PLUS \
            or node_type == Node.MINUS \
            or node_type == Node.EQ \
            or node_type == Node.NE \
            or node_type == Node.LT \
            or node_type == Node.GT \
            or node_type == Node.LE \
            or node_type == Node.GE \
            or node_type == Node.NOT \
            or node_type == Node.AND \
            or node_type == Node.OR:
        return _validate_operator(expression)

    elif node_type == Node.VARIABLE_LOAD:
        name = expression['name']
        var = _get_var(name)
        if var is None:
            _errors.append(f'Variable \'{name}\' is not defined.')
            return None
        else:
            expression['type'] = var[0]
            return var[0]

    elif node_type == Node.VARIABLE_ASSIGNMENT:
        return _validate_var_store(expression)

    elif node_type == Node.ARRAY_LOAD:
        name = expression['name']
        indexes = expression['indexes']

        var = _get_var(name)
        if var is None:
            _errors.append(f'Variable \'{name}\' is not defined.')
            return None

        t = _validate_array_access(var[0], indexes)
        expression['type'] = t
        return t

    elif node_type == Node.ARRAY_ASSIGNMENT:
        return _validate_array_store(expression)

    elif node_type == Node.FUNCTION_CALL_VALUE:
        return _validate_function_call(expression)

    else:
        raise NotImplementedError()


def _validate_function_returns(statements, return_type) -> bool:
    fork_statements = []
    for statement in statements:
        node_type = statement['node']

        if node_type == return_type:
            return True

        elif node_type == Node.IF_ELSE:
            fork_statements.append(statement)

    for statement in fork_statements:
        node_type = statement['node']

        if node_type == Node.IF_ELSE:
            if_statements = statement['if_statements']
            else_statements = statement['else_statements']
            ret1 = _validate_function_returns(if_statements)
            ret2 = _validate_function_returns(else_statements)
            if ret1 and ret2:
                return True
            else:
                continue

        else:
            print("internal error")
            break

    return False


def _validate_function_call(expression) -> Optional[Type]:
    name = expression['name']
    args = expression['arguments']

    args_types = [_validate_expression(i) for i in args]

    for (i, t) in enumerate(args_types):
        if t.is_array_any():
            _errors.append(f'{i}. argument type of function \'{name}\' call is ambiguous.')
            return None

    fn_ret = _get_func(name, args_types)
    if fn_ret is None:
        _errors.append(f'Undefined function \'{name}({", ".join(str(t) for t in args_types)})\'.')
        return None

    expression['parameters'] = args_types
    expression['type'] = fn_ret
    return fn_ret


def _validate_var_store(expression) -> Optional[Type]:
    name = expression['name']
    exp = expression['expression']
    var = _get_var(name)
    if var is None:
        _errors.append(f'Variable \'{name}\' is not defined.')
        return None

    if var[1]:
        _errors.append(f'Can not assign to the constant variable \'{name}\'.')
        return None

    exp_type = _validate_expression(exp)
    if var[0] != exp_type:
        _errors.append(f'Can not assign a value of type {exp_type} into variable \'{name}\' of type {var[0]}.')
        return None

    _array_type_inference(exp, var[0])
    expression['type'] = exp_type
    return exp_type


def _validate_array_store(expression) -> Optional[Type]:
    name = expression['name']
    indexes = expression['indexes']
    exp = expression['expression']
    var = _get_var(name)
    if var is None:
        _errors.append(f'Variable \'{name}\' is not defined.')
        return None

    if var[1]:
        _errors.append(f'Can not assign to item of constant array \'{name}\'.')
        return None

    target_type = _validate_array_access(var[0], indexes)
    if target_type is None:
        return None

    exp_type = _validate_expression(exp)
    if target_type != exp_type:
        _errors.append(f'Can not store value of type {exp_type} into {target_type}.')
        return None

    expression['type'] = exp_type
    return exp_type


def _validate_array_access(exp_type: Type, indexes_exps) -> Optional[Type]:
    if not isinstance(exp_type, TypeArray):
        _errors.append(f'Can not use array access on non-array type ({exp_type}).')
        return None

    indexes_types = [_validate_expression(i) for i in indexes_exps]

    for (i, t) in enumerate(indexes_types):
        if t != TypeInt():
            _errors.append(f'{i}. index ({t}) into the array is not of type Int.')
            return None

    if len(indexes_types) > exp_type.dim:
        _errors.append(f'Can not access dim {len(indexes_types)} on the array of dim {exp_type.dim}.')
        return None

    if len(indexes_types) == exp_type.dim:
        return exp_type.inner
    else:
        return TypeArray(exp_type.dim - 1, exp_type.inner)


def _validate_operator(expression) -> Optional[Type]:
    node_type = expression['node']
    sub_exps = [expression['expression']] \
        if node_type in {Node.UMINUS, Node.UPLUS, Node.NOT} \
        else [expression['left'], expression['right']]

    sub_exp_types = [_validate_expression(e) for e in sub_exps]

    if any(s is None for s in sub_exp_types):
        # type error already registered
        return None

    allowed = ALLOWED_OPERATOR_TYPES[node_type]

    for allowed_types in allowed:
        if len(allowed_types[0]) != len(sub_exp_types):
            continue

        if all(isinstance(t, allowed_t) for (t, allowed_t) in zip(sub_exp_types, allowed_types[0])):
            t = allowed_types[1]
            expression['type'] = t
            return t

    _errors.append(
        f'Invalid operand types ({", ".join(str(s) for s in sub_exp_types)}) for operator \'{node_type.name}\'')
    return None


def _validate_value(expression):
    """
    Validate the value node and resolve its type.
    :param expression: The value expression node.
    :return: Type of the value or None on failure.
    """
    if expression['node'] == Node.VALUE_INT:
        if not is_int(expression['value']):
            _errors.append(f'Integer {expression["value"]} is out of bounds (4 bytes).')
            return None
        expression['type'] = TypeInt()
        return TypeInt()
    elif expression['node'] == Node.VALUE_REAL:
        expression['type'] = TypeReal()
        return TypeReal()
    elif expression['node'] == Node.VALUE_BOOL:
        expression['type'] = TypeBool()
        return TypeBool()
    elif expression['node'] == Node.VALUE_STR:
        expression['type'] = TypeStr()
        return TypeStr()
    elif expression['node'] == Node.VALUE_ARRAY:
        return _validate_array_value(expression)
    else:
        raise NotImplementedError()


def _validate_array_value(expression) -> Optional[TypeArray]:
    """
    Validate the array value node and resolve its dim and inner type.
    :param expression: The array value expression node.
    :return: Type of the array value or None on failure.
    """
    items = expression['items']
    items_types = [_validate_expression(item) for item in items]

    if len(items_types) == 0:
        t = TypeArray(1, TypeAny())
        expression['type'] = t
        return t

    items_type = items_types[0]
    for t in items_types[1:]:
        if t is None:
            return None

        if t != items_type:
            _errors.append(
                f'Incompatible array items types ({", ".join(str(t) for t in items_types)})')
            return None

        if not isinstance(t, TypeArray) or not isinstance(t.inner, TypeAny):
            items_type = t

    if isinstance(items_type, TypeArray):
        t = TypeArray(items_type.dim + 1, items_type.inner)
        expression['type'] = t
        return t
    elif isinstance(items_type, BaseType):
        t = TypeArray(1, items_type)
        expression['type'] = t
        return t


def _array_type_inference(expression, top_type: Type):
    """
    Walk through the array value expression tree and replace
    inner Any types for the top type.
    :param expression: The array value expression node.
    :param top_type: Type of the top expression.
    """
    if expression['node'] != Node.VALUE_ARRAY or not isinstance(top_type, TypeArray):
        return

    dim = expression['type'].dim
    expression['type'] = TypeArray(dim, top_type.inner)

    if dim > 1:
        for item in expression['items']:
            _array_type_inference(item, top_type)


def _get_var(identifier: str) -> Optional[Tuple[Type, bool]]:
    """
    Get the variable record from symbols table.
    :param identifier: Identifier of the searched variable.
    :return: The variable type and is_const or None if not found.
    """
    for depth in _vars:
        if identifier in depth:
            return depth[identifier]
    return None


def _add_var(identifier: str, t: Type, is_const: bool):
    """
    Add the variable record into the symbols table.
    :param identifier: Identifier of variable.
    :param t: Type of the searched variable.
    :param is_const: True if the variable is constant.
    """
    # place the variable into the lowest layer
    _vars[-1][identifier] = (t, is_const)


def _get_func(identifier: str, params_types: Iterable[Type]) -> Optional[Type]:
    """
    Get the function record from the symbols table.
    :param identifier: Identifier of the searched function.
    :param params_types: Function params types.
    :return: The function and return_type or None if no func found
    """
    params_types = tuple(params_types)
    if identifier == FN_LEN and len(params_types) == 1 and isinstance(params_types[0], TypeArray):
        return TypeInt()
    if (identifier, params_types) in _functions:
        return _functions[(identifier, params_types)]
    return None


def _add_func(identifier: str, params_types: Iterable[Type], return_type: Type):
    """
    Add the function record into the symbols table.
    :param identifier: Identifier of the searched function.
    :param params_types: Function params types.
    :param return_type: Function return types.
    """
    params_types = tuple(params_types)
    _functions[(identifier, params_types)] = return_type


def _node_to_type(node):
    if node['node'] == Node.TYPE_INT:
        return TypeInt()
    elif node['node'] == Node.TYPE_REAL:
        return TypeReal()
    elif node['node'] == Node.TYPE_BOOL:
        return TypeBool()
    elif node['node'] == Node.TYPE_STR:
        return TypeStr()
    elif node['node'] == Node.TYPE_ARRAY:
        return TypeArray(node['dim'], _node_to_type(node['inner']))
    elif node['node'] == Node.TYPE_VOID:
        return TypeVoid()
    else:
        raise NotImplementedError(node[0])
