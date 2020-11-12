# PLY's documentation: http://www.dabeaz.com/ply/ply.html
import ply.lex as ply_scanner
import ply.yacc as ply_parser
from app.analyzers import *


def main():
    # Build the lexical_analyzer
    lexer = ply_scanner.lex()

    # Test it out
    # data = '''
    # 3 + 4 * 10
    #   + -20 *2
    # '''
    data = open('../input_test.txt', 'r').read()

    # Give the lexical_analyzer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        # print(tok)
        print("{:<20} {:<30} {:<5} {:<5}".format(tok.type, tok.value, tok.lineno, tok.lexpos))

    # ----------
    # # Build the parser
    # parser = ply_parser.yacc()
    # # Parsing loop
    # while True:
    #     try:
    #         s = input('calc > ')
    #     except EOFError:
    #         break
    #     if not s: continue
    #     result = parser.parse(s)
    #     print(result)


if __name__ == '__main__':
    main()
