import ply.lex as lex

resultadoLex = []

# Palabras reservadas
reservadas = {
    'programa': 'PROGRAMA',
    'int': 'INT',
    'read': 'READ',
    'printf': 'PRINTF',
    'println': 'PRINTLN',
    'end': 'END',
    'if': 'SI',
    'else': 'SINO',
    'for': 'PARA',
    'while': 'MIENTRAS'
}

tokens = [
    'IDENTIFICADOR', 
    'VARIABLE',  # Nuevo token para variables
    'ENTERO', 
    'ASIGNAR',  # = 
    # Operaciones
    'SUMA',  # +
    'RESTA',  # -
    'MULT',  # *
    'DIV',  # /
    # Lógica
    'AND',
    'OR',
    'NOT',
    'MENORQUE',  # <
    'MENORIGUAL',  # <=
    'MAYORQUE',  # >
    'MAYORIGUAL',  # >=
    'IGUAL',  # ==
    'DIFERENTE',  # !=
    'NUMERAL',  # #
    'LPAR',  # (
    'RPAR',  # )
    'LCOR',  # {
    'RCOR',  # }
    'LLLA',  # [
    'RLLA',  # ]
    # Otros
    'PUNTOCOMA',  # ;
    'COMA',  # ,
    'COMADOS',  # ""
    'MAYORDER',  # <<
    'MAYORIZQ',  # >>  
] + list(reservadas.values())  # Incluimos las palabras reservadas como tokens

# Reglas de Tokens mediante Expresiones Regulares
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_ASIGNAR = r'='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_MENORQUE = r'<'
t_MAYORQUE = r'>'
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_PUNTOCOMA = r';'
t_COMA = r','
t_LPAR = r'\('
t_RPAR = r'\)'
t_LLLA = r'\['
t_RLLA = r'\]'
t_LCOR = r'\{'
t_RCOR = r'\}'
t_COMADOS = r'\"'
t_NUMERAL = r'\#'
t_MAYORDER = r'<<'
t_MAYORIZQ = r'>>'

# Bandera para indicar que estamos dentro de una declaración de variables
variable_flag = False


def t_INT(t):
    r'int'
    global variable_flag
    t.type = 'INT'
    variable_flag = True  # Activamos la bandera cuando encontramos un 'int'
    return t

# Reglas para identificadores y enteros
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    global variable_flag
    # Si la bandera está activa, es una variable
    if variable_flag:
        t.type = 'VARIABLE'
        # Si el siguiente token no es una coma o un punto y coma, apagamos la bandera
        siguiente_token = t.lexer.lexdata[t.lexer.lexpos:t.lexer.lexpos+1]
        if siguiente_token not in [',', ';']:
            variable_flag = False
    else:
        t.type = reservadas.get(t.value, 'IDENTIFICADOR')  # Si es una palabra reservada, cambiar tipo
    return t



def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de comentarios de una línea
def t_COMENTARIO_SIMPLE(t):
    r'//.*'
    pass  # Ignoramos los comentarios

# Manejo de comentarios de múltiples líneas
def t_COMENTARIO_MULTILINEA(t):
    r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/'
    t.lexer.lineno += t.value.count('\n')

# Manejo de errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()

def prueba(data):
    analizador = lex.lex()
    analizador.input(data)
    tokens = []
    while True:
        tok = analizador.token()
        if not tok:
            break
        tokens.append((tok.lineno, tok.type, tok.value))
    return tokens
