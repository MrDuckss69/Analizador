import ply.yacc as yacc
from lexer import tokens, variables

# Definir la gramática
def p_programa(p):
    '''programa : PROGRAMA IDENTIFICADOR LPAR RPAR LCOR cuerpo END PUNTOCOMA RCOR'''
    p[0] = ('programa', p[2], p[6])

def p_cuerpo(p):
    '''cuerpo : declaraciones'''
    p[0] = ('cuerpo', p[1])

def p_declaraciones(p):
    '''declaraciones : declaraciones declaracion
                     | declaracion'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_declaracion(p):
    '''declaracion : tipo lista_identificadores PUNTOCOMA
                   | asignacion PUNTOCOMA
                   | lectura PUNTOCOMA
                   | escritura PUNTOCOMA
                   | expresion PUNTOCOMA'''  # Aceptar expresiones aritméticas
    p[0] = p[1]

def p_tipo(p):
    '''tipo : INT'''
    p[0] = ('int', p[1])

def p_lista_identificadores(p):
    '''lista_identificadores : VARIABLE
                             | lista_identificadores COMA VARIABLE'''
    if len(p) == 2:
        variables.add(p[1])
        p[0] = [p[1]]
    else:
        variables.add(p[3])
        p[0] = p[1] + [p[3]]

def p_asignacion(p):
    '''asignacion : VARIABLE ASIGNAR expresion'''
    p[0] = ('asignacion', p[1], p[3])

def p_lectura(p):
    '''lectura : READ VARIABLE'''
    p[0] = ('lectura', p[2])

def p_escritura(p):
    '''escritura : PRINTF LPAR IDENTIFICADOR RPAR
                 | PRINTF LPAR CADENA COMA expresion RPAR'''
    if len(p) == 5:
        # Caso con solo una cadena
        p[0] = ('escritura', p[3])
    elif len(p) == 7:
        # Caso con cadena y una expresión
        p[0] = ('escritura', p[3], p[5])

def p_expresion(p):
    '''expresion : expresion SUMA termino
                 | expresion RESTA termino
                 | termino'''
    if len(p) == 4:
        p[0] = ('expresion_binaria', p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_termino(p):
    '''termino : termino MULT factor
               | termino DIV factor
               | factor'''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
    else:
        p[0] = p[1]

def p_factor(p):
    '''factor : ENTERO
              | VARIABLE
              | LPAR expresion RPAR
              | CADENA'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

# Manejo de errores
def p_error(p):
    if p:
        print(f"Error de sintaxis en '{p.value}'")
        raise SyntaxError(f"Error de sintaxis en la línea {p.lineno}: '{p.value}'")
    else:
        print("Error de sintaxis en EOF")
        raise SyntaxError("Error de sintaxis en EOF")

# Construir el parser
parser = yacc.yacc()

# Función para probar el parser
def parse(data):
    try:
        result = parser.parse(data)
        return result, None
    except SyntaxError as e:
        return None, str(e)

# Función para contar tokens
def count_tokens(tokens):
    counts = {
        "total": len(tokens),
        "reserved_words": 0,
        "identifiers": 0,
        "variables": 0,
        "numbers": 0,
        "symbols": 0
    }
    
    reserved_words = {'PROGRAMA', 'INT', 'READ', 'PRINTF', 'END', 'SI', 'SINO', 'PARA', 'MIENTRAS'}
    symbols = {'SUMA', 'RESTA', 'MULT', 'DIV', 'ASIGNAR', 'AND', 'OR', 'NOT', 'MENORQUE', 'MAYORQUE', 'MENORIGUAL', 'MAYORIGUAL', 'IGUAL', 'DIFERENTE', 'NUMERAL', 'LPAR', 'RPAR', 'LCOR', 'RCOR', 'LLLA', 'RLLA', 'PUNTOCOMA', 'COMA', 'COMADOS', 'MAYORDER', 'MAYORIZQ'}
    
    for token in tokens:
        if token[1] in reserved_words:
            counts["reserved_words"] += 1
        elif token[1] == 'IDENTIFICADOR':
            counts["identifiers"] += 1
        elif token[1] == 'VARIABLE':
            counts["variables"] += 1
        elif token[1] == 'ENTERO':
            counts["numbers"] += 1
        elif token[1] in symbols:
            counts["symbols"] += 1
    
    return counts

# Función para analizar la sintaxis
def parse_syntax(data):
    result, error = parse(data)
    if error:
        return {"correct": False, "message": error}
    else:
        return {"correct": True, "message": "Análisis sintáctico correcto", "result": result}
