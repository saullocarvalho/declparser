from sly import Parser
from decl_lexer import DeclLexer

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
        return ('decl', p.varname, p.typedef)

    # varname               : ID

    @_('ID')
    def varname(self, p):
        return p.ID

    # typedef               : type_opt_deref_arr
    #                       | STRUCT LBRACE typedefs RBRACE
    #                       | UNION LBRACE typedefs RBRACE

    @_('type_opt_deref_arr')
    def typedef(self, p):
        return p.type_opt_deref_arr

    @_('STRUCT LBRACE typedefs RBRACE')
    def typedef(self, p):
        return ('struct', p.typedefs)

    @_('UNION LBRACE typedefs RBRACE')
    def typedef(self, p):
        return ('union', p.typedefs)

    # type_opt_deref_arr    : type_opt_deref_arr LBRACK size RBRACK
    #                       | type_opt_deref

    @_('type_opt_deref_arr LBRACK size RBRACK')
    def type_opt_deref_arr(self, p):
        return ('array', p.type_opt_deref_arr, p.size)

    @_('type_opt_deref')
    def type_opt_deref_arr(self, p):
        return p.type_opt_deref

    # type_opt_deref        : DEREF type_opt_deref
    #                       | type_non_opt

    @_('DEREF type_opt_deref')
    def type_opt_deref(self, p):
        return ('pointer', p.type_opt_deref)

    @_('type_non_opt')
    def type_opt_deref(self, p):
        return p.type_non_opt

    # size                  : NUMBER

    @_('NUMBER')
    def size(self, p):
        return int(p.NUMBER)

    # type_non_opt          : LPAREN type_opt_deref_arr RPAREN
    #                       | typename

    @_('LPAREN type_opt_deref_arr RPAREN')
    def type_non_opt(self, p):
        return p.type_opt_deref_arr

    @_('typename')
    def type_non_opt(self, p):
        return p.typename

    # typename              : ID
    @_('ID')
    def typename(self, p):
        return ('id_type', p.ID)

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
