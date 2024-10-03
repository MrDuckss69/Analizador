import ply.yacc as yacc
from lexer_parser.lexer import tokens

# Reglas de gramática

def p_programa(p):
    '''programa : PROGRAMA IDENTIFICADOR LPAR RPAR LCOR declaraciones RCOR'''
    p[0] = 'Estructura válida'

def p_declaraciones(p):
    '''declaraciones : declaraciones declaracion
                     | declaracion'''
    p[0] = p[1]

def p_declaracion(p):
    '''declaracion : INT lista_variables PUNTOCOMA
                   | READ VARIABLE PUNTOCOMA
                   | PRINTF LPAR COMADOS VARIABLE COMADOS RPAR PUNTOCOMA
                   | VARIABLE ASIGNAR VARIABLE SUMA VARIABLE PUNTOCOMA
                   | END PUNTOCOMA'''
    p[0] = p[1]

def p_lista_variables(p):
    '''lista_variables : VARIABLE COMA lista_variables
                       | VARIABLE'''
    p[0] = p[1]

# Manejo de errores sintácticos
def p_error(p):
    if p:
        print(f"Error sintáctico en el token: {p.value}")
        raise SyntaxError(f"Error sintáctico en el token: {p.value}")
    else:
        print("Error sintáctico en EOF")
        raise SyntaxError("Error sintáctico en EOF")

# Construir el parser
parser = yacc.yacc()

def parse_syntax(data):
    try:
        result = parser.parse(data)
        return result
    except SyntaxError as e:
        return str(e)
