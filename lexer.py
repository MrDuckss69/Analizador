import ply.lex as lex

resultadoLex = []

# Palabras reservadas
reservadas = {
    'programa': 'PROGRAMA',
    'int': 'INT',
    'read': 'READ',
    'printf': 'PRINTF',
    'end': 'END',
    'if': 'SI',
    'else': 'SINO',
    'for': 'PARA',
    'while': 'MIENTRAS'
}

tokens = [
    'IDENTIFICADOR', 
    'ENTERO', 
    'ASIGNAR',  # = 
    'CADENA',  # Cadenas de texto
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
    'MAYORIZQ',  # >>,
    'VARIABLE'  # Añadimos VARIABLE a la lista de tokens
] + list(reservadas.values())  # Incluimos las palabras reservadas como tokens

# Conjunto para almacenar variables declaradas
variables = set()

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

# Reglas para identificadores y enteros
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reservadas:
        t.type = reservadas[t.value]  # Si es una palabra reservada, cambiar tipo
    elif t.value in variables:
        t.type = 'VARIABLE'  # Si es una variable declarada, cambiar tipo
    return t

def t_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.type = 'IDENTIFICADOR'  # Cambiar el tipo a IDENTIFICADOR
    t.value = t.value.strip('"')  # Eliminar las comillas
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
        if tok.type == 'INT':  # Detectar declaración de variables
            while True:
                siguiente_tok = analizador.token()
                if not siguiente_tok:
                    break
                if siguiente_tok.type == 'IDENTIFICADOR':
                    variables.add(siguiente_tok.value)
                    tokens.append((siguiente_tok.lineno, 'VARIABLE', siguiente_tok.value))
                elif siguiente_tok.type == 'COMA':
                    continue
                elif siguiente_tok.type == 'PUNTOCOMA':
                    break
                else:
                    tokens.append((siguiente_tok.lineno, siguiente_tok.type, siguiente_tok.value))
                    break
        else:
            tokens.append((tok.lineno, tok.type, tok.value))
    return tokens