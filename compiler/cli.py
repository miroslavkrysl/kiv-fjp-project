# PLY's documentation: http://www.dabeaz.com/ply/ply.html
import os
import re

import sys
import ply.lex
import ply.yacc
import compiler.lex
import compiler.syntax
import compiler.sem.analyze
from compiler.gen.classfile import create_classfile
from compiler.gen.generator import generate
from compiler.lex import LexerError
from compiler.syntax import SyntaxerError

CLASS_NAME_REGEX = r'^([^\.;\[/]+\.)*[^\.;\[/]+$'


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
    lexer = ply.lex.lex(module=compiler.lex)

    if len(sys.argv) < 3:
        print("Parameters does not match the format!")
        print("<input_code_file> <output_class_name>")
        return 1

    input_file = sys.argv[1]
    output_class_name = sys.argv[2]

    if not os.path.isfile(input_file):
        print("Input file not accessible!")
        return 1

    if not re.match(CLASS_NAME_REGEX, output_class_name):
        print("Output class name is invalid!")
        return 1

    data = open(input_file, 'r').read()
    lexer.input(data)

    # Tokenize
    # while True:
    #     tok = lexer.token()
    #     if not tok:
    #         break  # No more input
    #     print(tok)
    #     print("{:<20} {:<30} {:<5} {:<5}".format(tok.type, tok.value, tok.lineno, tok.lexpos))

    try:
        parser = ply.yacc.yacc(module=compiler.syntax, debug=False)
        ast = parser.parse(data, lexer=lexer, tracking=True, debug=False)

        if compiler.sem.analyze(ast):
            # print_tree(ast)
            cls = generate(output_class_name, ast)
            output_file = open(output_class_name + '.class', 'wb')
            create_classfile(cls, output_file)
            output_file.close()
    except SyntaxerError:
        pass
    except LexerError:
        pass
