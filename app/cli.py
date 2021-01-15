# PLY's documentation: http://www.dabeaz.com/ply/ply.html
from pprint import pprint, pp

import ply.lex
import ply.yacc
import app.lex
import app.syntax
import app.sem.analyze
from app.gen.generator import generate
from app.syntax import Node


def print_tree(x, level=0):
    if isinstance(x, dict):
        print(('    ' * level) + str(x['node']))
        for (k, v) in x.items():
            if k != 'node':
                print(('    ' * (level+1)) + k + ':')
                print_tree(v, level+2)
    elif isinstance(x, list):
        if x:
            print('    ' * level + '[')
            for i in x:
                print_tree(i, level + 1)
            print('    ' * level + ']')
        else:
            print('    ' * level + str(x))
    else:
        print(('    ' * level) + str(x))


def main():
    # Build the lexical_analyzer
    lexer = ply.lex.lex(module=app.lex)

    data = open('../inputs/input_test.txt', 'r').read()
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        # print(tok)
        print("{:<20} {:<30} {:<5} {:<5}".format(tok.type, tok.value, tok.lineno, tok.lexpos))

    parser = ply.yacc.yacc(module=app.syntax)
    result = parser.parse(data, lexer=lexer, tracking=True)

    print_tree(result)
    app.sem.analyze(result)
    # cls = generate("Main", result)


if __name__ == '__main__':
    main()
