import ply.yacc as yacc
from lexer import tokens, variables  # Importar los tokens y el conjunto de variables desde el lexer

# Definir la gramática
def p_programa(p):
    '''programa : PROGRAMA IDENTIFICADOR LPAR RPAR LCOR cuerpo RCOR END PUNTOCOMA'''
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
                   | escritura PUNTOCOMA'''
    p[0] = p[1]

def p_tipo(p):
    '''tipo : INT'''
    p[0] = p[1]

def p_lista_identificadores(p):
    '''lista_identificadores : IDENTIFICADOR
                             | lista_identificadores COMA IDENTIFICADOR'''
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
    '''escritura : PRINTF LPAR CADENA RPAR
                 | PRINTF LPAR CADENA COMA VARIABLE RPAR'''
    if len(p) == 5:
        p[0] = ('escritura', p[3])
    else:
        p[0] = ('escritura', p[3], p[5])

def p_expresion(p):
    '''expresion : expresion SUMA termino
                 | expresion RESTA termino
                 | termino'''
    if len(p) == 4:
        p[0] = (p[2], p[1], p[3])
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
        raise SyntaxError(f"Error de sintaxis en '{p.value}' en la línea {p.lineno}")
    else:
        raise SyntaxError("Error de sintaxis en EOF")

# Construir el parser
parser = yacc.yacc()

# Función para probar el parser
def parse(data):
    result = parser.parse(data)
    return result

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
    
    reserved_words = {'PROGRAMA', 'INT', 'READ', 'PRINTF', 'PRINTLN', 'END', 'SI', 'SINO', 'PARA', 'MIENTRAS'}
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
    try:
        result = parse(data)
        return {"correct": True, "message": "Análisis sintáctico correcto", "result": result}
    except SyntaxError as e:
        return {"correct": False, "message": str(e)}