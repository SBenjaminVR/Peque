
import ply.lex as lex           # Scanner
import ply.yacc as yacc  

#--------------------------------------- palabras reservadas---------------------------------------
#tokens reservados o palabras reservadas
reserved = {
    'programa': 'PROGRAMA',
    'print': 'PRINT',
    'fila' : 'FILA',
    'petite': 'PETITE',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'void' : 'VOID',
    'bool': 'BOOL',
    'if': 'IF',
    'else': 'ELSE',
    'mini' : 'MINI',
    'agranda': 'AGRANDA',
    'peque': 'PEQUE',
    'return':'RETURN',
    'input' : 'INPUT',
    'for':'FOR',
    'while' : 'WHILE',
    'to' : 'TO',
    'main': 'MAIN'
}
#--------------------------------------- Tokens---------------------------------------

tokens = [
    'ID',
    'CTEI', 'CTEF', 'CTEC',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'DOTS', 'EQUALS', 'SEMICOLON', 'PERIOD', 'COMMA',
    'LESS', 'BIGGER', 'DIFFERENT','EQUAL','BIGGER_EQUAL', 'LESS_EQUAL',
    'L_PARENTHESIS', 'R_PARENTHESIS', 'L_BRACKET', 'R_BRACKET', 'L_CORCHETE', 'R_CORCHETE',
    'OR', 'AND',
    'COMMENT',
] + list(reserved.values())
#--------------------------------------- Simple regular expresion---------------------------------------

# Expresiones regulares para tokens simples
t_L_CORCHETE = r'\['
t_R_CORCHETE = r'\]'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_DOTS = r'\:'
t_EQUALS = r'\='
t_SEMICOLON = r'\;'
t_PERIOD = r'\.'
t_COMMA = r'\,'
t_LESS = r'\<'
t_BIGGER = r'\>'
t_DIFFERENT = r'\<\>'
t_EQUAL = r'\=\='
t_BIGGER_EQUAL = r'\>\='
t_LESS_EQUAL = r'\<\='
t_L_PARENTHESIS = r'\('
t_R_PARENTHESIS = r'\)'
t_L_BRACKET = r'\{'
t_R_BRACKET = r'\}'
t_OR = r'\|\|'
t_AND = r'\&\&'

# Caracteres ignorados (Espacios y tabs)
t_ignore = ' \t'
#ignore newlines
def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
#id regular expresion
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    #Directory[t.value] = []
    return t
 #error 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
#float
def t_CTEF(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
#Int
def t_CTEI(t):
    r'\d+'
    t.value = int(t.value)
    return t
def t_CTEC(t):
    r'[a-z]'
    t.value = str(t.value)
    return t
def t_COMMENT(t):
     r'\#.*'
     pass

#construimos el lexico
lexer = lex.lex()
#precedencia de operadores
precedence = (
    ( 'left', 'PLUS', 'MINUS' ),
    ( 'left', 'TIMES', 'DIVIDE' ),
)
# er para el programa
#falta declaracion de variable