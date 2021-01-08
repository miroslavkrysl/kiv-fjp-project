# Here goes AST analyze process
from app.syntax import Node

sem_var_def = {}  # Key = depth, Value => Key = identifier, Value = (AST definition type tuple, is constant)
sem_func_def = {}  # Key = identifier, Value = tuple (AST parameter list of type tuples, AST return type tuple)
sem_errors = []


def analyze(ast):
    print("ANALYZING THE INPUT...")
    _analyze_layer(ast, 0, False, False)

    # Print errors
    if len(sem_errors) > 0:
        print(sem_errors)


def _analyze_layer(items, depth, func_ins, loop_ins):
    sem_var_def[depth] = {}

    # Recursive limit stop statement
    if depth > 32:
        sem_errors.append("Depth overreached the limit of 32.")
        return

    # Go through all the items and register all the functions first in the root (depth-0)
    if depth == 0:
        for item in items:
            if item[0] == Node.FUNCTION_DEFINITION:
                if not _is_identifier_free(item[1], depth):
                    sem_errors.append("Identifier '{1}' is already taken. Depth: {0}".format(depth, item[1]))
                    break
                sem_func_def[item[1]] = (item[2], item[3])

    # Go through the all items in the current depth
    for item in items:
        # TODO: This print is just for debugging
        print("{0}: {1}".format(depth, item))

        # Function definition
        if item[0] == Node.FUNCTION_DEFINITION:
            _analyze_layer(item[4], depth + 1, True, loop_ins)
            if len(sem_errors) > 0:
                break

        # Constant definition
        elif item[0] == Node.CONSTANT_DEFINITION:
            if not _is_identifier_free(item[1], depth):
                sem_errors.append("Identifier '{1}' is already taken. Depth: {0}".format(depth, item[1]))
                break
            if not _is_value_match_type(item[2], item[3]):
                sem_errors.append(
                    "Type of assigned value does not match ({1} to {2}). Depth: {0}".format(depth, item[3], item[2]))
                break
            sem_var_def[depth][item[1]] = (item[2], True)

        # Variable definition
        elif item[0] == Node.VARIABLE_DEFINITION:
            if not _is_identifier_free(item[1], depth):
                sem_errors.append("Identifier '{1}' is already taken. Depth: {0}".format(depth, item[1]))
                break
            # TODO: Validate Expression
            if not _is_value_match_type(item[2], item[3]):
                sem_errors.append(
                    "Type of assigned value does not match ({1} to {2}). Depth: {0}".format(depth, item[3], item[2]))
                break
            sem_var_def[depth][item[1]] = (item[2], False)

        # Variable declaration
        elif item[0] == Node.VARIABLE_DECLARATION:
            if not _is_identifier_free(item[1], depth):
                sem_errors.append("Identifier '{1}' is already taken. Depth: {0}".format(depth, item[1]))
                break
            sem_var_def[depth][item[1]] = (item[2], False)

        # Variable assign
        elif item[0] == Node.VARIABLE_ASSIGN:
            v = _get_var(item[1])
            if v is None:
                sem_errors.append("Assigning value to undefined variable '{1}'. Depth: {0}".format(depth, item[1]))
                break
            if v[1]:
                sem_errors.append("Cannot assign value to constant variable '{1}'. Depth: {0}".format(depth, item[1]))
                break
            # TODO: Validate Expression - in debug
            expr_type = _validate_expression(item[2])
            if expr_type is None:
                sem_errors.append("Expression is invalid: {0}. Depth: {0}".format(depth, item[2]))
                break
            if v[0] != expr_type:
                sem_errors.append("Type of assigned value does not match ({1} to {2}). Depth: {0}".format(depth, expr_type, v[0]))
                break

        # Function call
        elif item[0] == Node.FUNCTION_CALL:
            f = _get_func(item[1])
            if f is None:
                sem_errors.append("Calling undefined function '{1}'. Depth: {0}".format(depth, item[1]))
                break
            if not _is_func_parameters_match(item[2], f[0]):
                sem_errors.append("Calling undefined function '{1}' ({2}). Depth: {0}".format(depth, item[1], item[2]))
                break

        # Condition (IF)
        elif item[0] == Node.IF:
            # TODO: Validate Expression
            _analyze_layer(item[2], depth + 1, func_ins, loop_ins)
            if len(sem_errors) > 0:
                break

        # Condition (IF-ELSE)
        elif item[0] == Node.IF_ELSE:
            # TODO: Validate Expression
            _analyze_layer(item[2], depth + 1, func_ins, loop_ins)
            if len(sem_errors) > 0:
                break
            _analyze_layer(item[3], depth + 1, func_ins, loop_ins)
            if len(sem_errors) > 0:
                break

        # Loop (WHILE)
        elif item[0] == Node.WHILE:
            # TODO: Validate Expression
            _analyze_layer(item[2], depth + 1, func_ins, True)
            if len(sem_errors) > 0:
                break

        # Return keyword
        elif item[0] == Node.RETURN:
            # TODO: Return keyword
            pass

        # Break keyword
        elif item[0] == Node.BREAK:
            if not loop_ins:
                sem_errors.append("Break definition outside of loop. Depth: {0}".format(depth))
                break

        # Continue keyword
        elif item[0] == Node.CONTINUE:
            if not loop_ins:
                sem_errors.append("Continue definition outside of loop. Depth: {0}".format(depth))
                break


def _is_identifier_free(identifier, depth):
    """
    Check if input identifier is not already taken
    :param identifier: The identifier
    :param depth: Current depth
    :return: True = free, False otherwise
    """
    for depth_key in sem_var_def:
        if depth_key < depth:
            break
        if identifier in sem_var_def[depth_key]:
            return False
    if identifier in sem_func_def:
        return False
    return True


def _validate_expression(texpression):
    """
    TODO: not working yet
    Validate expression
    :param texpression: The expression
    :return: Type tuple or None on failure
    """
    if texpression[0] == Node.UPLUS \
            or texpression[0] == Node.UMINUS \
            or texpression[0] == Node.MUL \
            or texpression[0] == Node.DIV \
            or texpression[0] == Node.PLUS \
            or texpression[0] == Node.MINUS \
            or texpression[0] == Node.EQ \
            or texpression[0] == Node.NE \
            or texpression[0] == Node.LT \
            or texpression[0] == Node.GT \
            or texpression[0] == Node.LE \
            or texpression[0] == Node.GE:
        ret1 = _validate_expression(texpression[1])
        ret2 = _validate_expression(texpression[2])
        if ret1 == ret2 and ret1 != Node.TYPE_ARRAY and ret1 != Node.TYPE_BOOL:
            return (ret1,)
        else:
            return (None,)
    if texpression[0] == Node.NOT \
            or texpression[0] == Node.AND \
            or texpression[0] == Node.OR:
        ret1 = _validate_expression(texpression[1])
        ret2 = _validate_expression(texpression[2])
        if ret1 == ret2 and ret1 != Node.TYPE_ARRAY and ret1 == Node.TYPE_BOOL:
            return (ret1,)
        else:
            return (None,)
    else:
        return (_value_to_type(texpression[0]),)


def _value_to_type(value):
    """
    Convert value node to type node
    :param value: The value node
    :return: Type node or None on failure
    """
    if value == Node.VALUE_INT:
        return Node.TYPE_INT
    elif value == Node.VALUE_REAL:
        return Node.TYPE_REAL
    elif value == Node.VALUE_ARRAY:
        return Node.TYPE_ARRAY
    elif value == Node.VALUE_BOOL:
        return Node.TYPE_BOOL
    elif value == Node.VALUE_STR:
        return Node.TYPE_STR
    else:
        return None


def _is_value_match_type(ttype, tvalue):
    """
    Check if the AST tuple type matches with AST tuple value
    :param ttype: The AST tuple type
    :param tvalue: The AST tuple value
    :return: True = matches, False otherwise
    """
    if (ttype[0] == Node.TYPE_INT and tvalue[0] == Node.VALUE_INT) \
            or (ttype[0] == Node.TYPE_REAL and tvalue[0] == Node.VALUE_REAL) \
            or (ttype[0] == Node.TYPE_ARRAY and tvalue[0] == Node.VALUE_ARRAY) \
            or (ttype[0] == Node.TYPE_BOOL and tvalue[0] == Node.VALUE_BOOL) \
            or (ttype[0] == Node.TYPE_STR and tvalue[0] == Node.VALUE_STR):
        # Check if there is any more type to check in deep...
        if len(ttype) > 1 and type(tvalue[1]) == tuple:
            return _is_value_match_type(ttype[1], tvalue[1])
        # Or if we are sure there is no more types to check...
        elif len(ttype) == 1 and type(tvalue[1]) != tuple:
            return True
        # Otherwise, failure
        else:
            return False
    return False


def _is_func_parameters_match(lval, ldef):
    """
    Check if input parameters match with function declaration
    :param lval: Input value list
    :param ldef: Function parameter definition list
    :return: True = matches, False = otherwise
    """
    if len(lval) != len(ldef):
        return False
    i = 0
    for v in lval:
        if not _is_value_match_type(ldef[i][1], v):
            return False
        i += 1
    return True


def _get_var(identifier):
    """
    Finds and gets the var record if any exists
    :param identifier: Identifier of the searched var
    :return: The var record or None if no var found
    """
    for depth_key in sem_var_def:
        if identifier in sem_var_def[depth_key]:
            return sem_var_def[depth_key][identifier]
    return None


def _get_func(identifier):
    """
    Finds and gets the func record if any exists
    :param identifier: Identifier of the searched func
    :return: The func record or None if no func found
    """
    if identifier in sem_func_def:
        return sem_func_def[identifier]
    return None
