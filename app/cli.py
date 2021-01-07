# PLY's documentation: http://www.dabeaz.com/ply/ply.html
from pprint import pprint, pp

import ply.lex
import ply.yacc
import app.lex
import app.syntax


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

    pp(result, width=1)


if __name__ == '__main__':
    main()
