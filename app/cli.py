# PLY's documentation: http://www.dabeaz.com/ply/ply.html
from pprint import pprint, pp

import ply.lex
import ply.yacc
import app.lex
import app.syntax
import app.sem.analyze


def print_tree(x, level=0):
    p = []
    r = []
    for i in x:
        if isinstance(i, tuple):
            r.append(i)
        else:
            p.append(i)

    print(('    ' * (level + 1)) + ', '.join(map(str, p)))

    for i in r:
        print_tree(i, level + 1)


def main():
    # Build the lexical_analyzer
    lexer = ply.lex.lex(module=app.lex)

    data = open('../input_test.txt', 'r').read()
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
    # app.sem.analyze.analyze(result)


if __name__ == '__main__':
    main()
