from sly import Lexer

class DeclLexer(Lexer):
    # Set of token names.
    tokens = { ID, NUMBER, STRUCT, UNION,
              LBRACE, RBRACE, LBRACK, RBRACK, LPAREN, RPAREN,
              SEMI, DEREF,
              }

    # String containing ignored characters between tokens
    ignore = ' \t\n'

    # Regular expression rules for tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['struct'] = STRUCT
    ID['union'] = UNION

    LBRACK = r'\['
    RBRACK = r'\]'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LPAREN = r'\('
    RPAREN = r'\)'
    DEREF = r'\*'
    SEMI = r';'
    NUMBER = r'\d+'

    # Error handling rule
    def error(self, t):
        print("[ERROR] Illegal character '%s'" % t.value[0])
        self.index += 1


if __name__ == '__main__':
    data = """struct a { int ; long; float; };
    *char[23];
    union b { int; byte; }
    *(*int)[20];
    """
    lexer = DeclLexer()
    for tok in lexer.tokenize(data):
        print('type=%r, value=%r' % (tok.type, tok.value))
