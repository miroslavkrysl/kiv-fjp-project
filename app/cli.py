# PLY's documentation: http://www.dabeaz.com/ply/ply.html
import os
from pprint import pprint, pp

import sys
import ply.lex
import ply.yacc
import app.lex
import app.syntax
import app.sem.analyze
from app.gen.classfile import create_classfile
from app.gen.generator import generate


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

    if len(sys.argv) < 3:
        print("Parameters does not match the format!")
        print("<input_code_file> <output_class_file>")
        return 1

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print("Input file not accessible!")
        return 1

    data = open(input_file, 'r').read()
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        # print(tok)
        # print("{:<20} {:<30} {:<5} {:<5}".format(tok.type, tok.value, tok.lineno, tok.lexpos))

    parser = ply.yacc.yacc(module=app.syntax)
    ast = parser.parse(data, lexer=lexer, tracking=True)

    if app.sem.analyze(ast):
        # print_tree(ast)
        cls = generate("Main", ast)
        f = open(output_file, 'wb')
        create_classfile(cls, f)
        f.close()


if __name__ == '__main__':
    main()
