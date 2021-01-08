# Here goes AST analyze process
from app.syntax import Node

sem_var_def = {}  # Key = depth, Value => Key = identifier, Value = tuple (AST definition type tuple, AST literal type)
sem_func_def = {}  # Key = identifier, Value = tuple (AST parameter list of type tuples, AST return type tuple)
sem_errors = []


def analyze(ast):
    print("ANALYZING THE INPUT...")
    _analyze_layer(ast, 0)

    # Print errors
    if len(sem_errors) > 0:
        print(sem_errors)


def _analyze_layer(items, depth):
    sem_var_def[depth] = {}

    # Go through all the items and register all the functions first in the root (depth-0)
    if depth == 0:
        for item in items:
            if item[0] == Node.FUNCTION_DEFINITION:
                if not _is_identifier_free(item[1]):
                    sem_errors.append("Identifier '{1}' is already taken. Depth: {0}".format(depth, item[1]))
                    break
                sem_func_def[item[1]] = (item[2], item[3])

    # Go through the all items in the current depth
    for item in items:
        # TODO: This print is just for debugging
        if depth > 0:
            print("{0}: {1}".format(depth, item))

        # Function definition
        if item[0] == Node.FUNCTION_DEFINITION:
            _analyze_layer(item[4], depth + 1)
            if len(sem_errors) > 0:
                break

        # Constant definition
        elif item[0] == Node.CONSTANT_DEFINITION:
            if not _is_identifier_free(item[1]):
                sem_errors.append("Identifier '{1}' is already taken. Depth: {0}".format(depth, item[1]))
                break
            if not _is_value_match_type(item[2], item[3]):
                sem_errors.append("Type of assigned value does not match ({1} to {2}). Depth: {0}".format(depth, item[3], item[2]))
                break
            sem_var_def[depth][item[1]] = (item[2], item[3])

        # Variable definition
        elif item[0] == Node.VARIABLE_DEFINITION:
            pass

        # Variable declaration
        elif item[0] == Node.VARIABLE_DECLARATION:
            pass

        # Variable assign
        elif item[0] == Node.VARIABLE_ASSIGN:
            v = _get_var(item[1])
            if v is None:
                sem_errors.append("Assigning value to undefined variable '{1}'. Depth: {0}".format(depth, item[1]))
                break
            if not _is_value_match_type(v[0], item[2]):
                sem_errors.append("Type of assigned value does not match ({1} to {2}). Depth: {0}".format(depth, item[2], v[0]))
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
            pass

        # Condition (IF-ELSE)
        elif item[0] == Node.IF_ELSE:
            pass

        # Loop (WHILE)
        elif item[0] == Node.WHILE:
            pass

        # Return keyword
        elif item[0] == Node.RETURN:
            pass

        # Break keyword
        elif item[0] == Node.BREAK:
            pass

        # Continue keyword
        elif item[0] == Node.CONTINUE:
            pass


def _is_identifier_free(identifier):
    """
    Check if input identifier is not already taken
    :param identifier: The identifier
    :return: True = free, False otherwise
    """
    for depth_key in sem_var_def:
        if identifier in sem_var_def[depth_key]:
            return False
    if identifier in sem_func_def:
        return False
    return True


def _is_value_match_type(ttype, tvalue):
    """
    Check if the AST tuple type matches with AST tuple value
    :param ttype: The AST tuple type
    :param tvalue: The AST tuple value
    :return: True = matches, False otherwise
    """
    if (ttype[0] == Node.TYPE_INT and tvalue[0] == Node.VALUE_INT)\
            or (ttype[0] == Node.TYPE_REAL and tvalue[0] == Node.VALUE_REAL)\
            or (ttype[0] == Node.TYPE_ARRAY and tvalue[0] == Node.VALUE_ARRAY)\
            or (ttype[0] == Node.TYPE_BOOL and tvalue[0] == Node.VALUE_BOOL)\
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
    for items in sem_var_def:
        if identifier in items:
            return items[identifier]
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
