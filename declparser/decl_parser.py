from sly import Parser
from .decl_lexer import DeclLexer

class DeclParser(Parser):
    # get the token list from the Lexer (required)
    tokens = DeclLexer.tokens

    #
    # Gramar rules and actions
    #

    # decltypedefs          : decls
    #                       | typedefs

    @_('decls',
       'typedefs')
    def decltypedefs(self, p):
        return p[0]

    # decls                 : decls SEMI decl
    #                       | decl

    @_('decls SEMI decl')
    def decls(self, p):
        return p.decls + [ p.decl ]

    @_('decl')
    def decls(self, p):
        return [ p.decl ]

    # typedefs              : typedefs SEMI typedef
    #                       | typedef

    @_('typedefs SEMI typedef')
    def typedefs(self, p):
        return p.typedefs + [ p.typedef ]

    @_('typedef')
    def typedefs(self, p):
        return [ p.typedef ]

    # decl                  : typedef varname

    @_('typedef varname')
    def decl(self, p):
        return ('decl', p.typedef, p.varname)

    # varname               : ID

    @_('ID')
    def varname(self, p):
        return p.ID

    # typedef               : defoptderefarr
    #                       | STRUCT LBRACK typedefs RBRACK
    #                       | UNION LBRACK typedefs RBRACK

    @_('defoptderefarr')
    def typedef(self, p):
        return ('typedef', p.defoptderefarr)

    @_('STRUCT LBRACK typedefs RBRACK')
    def typedef(self, p):
        return ('struct', p.typedefs)

    @_('UNION LBRACK typedefs RBRACK')
    def typedef(self, p):
        return ('union', p.typedefs)

    # defoptderefarr        : defoptderefarr LBRACE size RBRACE
    #                       | defoptderef

    @_('defoptderefarr LBRACE size RBRACE')
    def defoptderefarr(self, p):
        return ('array', p.defoptderefarr, p.size)

    @_('defoptderef')
    def defoptderefarr(self, p):
        return p.defoptderef

    # defoptderef           : DEREF defoptderef
    #                       | defnonopt

    @_('DEREF defoptderef')
    def defoptderef(self, p):
        return ('pointer', p.defoptderef)

    @_('defnonopt')
    def defoptderef(self, p):
        return p.defnonopt

    # size                  : NUMBER

    @_('NUMBER')
    def size(self, p):
        return int(p.NUMBER)

    # defnonopt             : LPAREN typedef RPAREN
    #                       | typename

    @_('LPAREN typedef RPAREN')
    def defnonopt(self, p):
        return p.typedef

    @_('typename')
    def defnonopt(self, p):
        return p.typename

    # typename              : ID
    @_('ID')
    def typename(self, p):
        return p.ID

if __name__ == '__main__':
    lexer = DeclLexer()
    parser = DeclParser()

    while True:
        try:
            text = input('parser > ')
            if text == "quit":
                break
            result = parser.parse(lexer.tokenize(text))
            print(result)
        except EOFError:
            break
