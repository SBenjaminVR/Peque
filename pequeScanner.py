import ply.lex as lex           # Scanner
import ply.yacc as yacc         # Parser
from pathlib import Path        # Read files
import sys

#tokens reservados o palabras reservadas
reserved = {
    'programa': 'PROGRAMA',
    'escribe': 'ESCRIBE',
    'variable': 'VARIABLE',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'void' : 'VOID',
    'if': 'IF',
    'else': 'ELSE',
    'mini' : 'MINI',
    'agranda': 'AGRANDA',
    'peque': 'PEQUE',
    'regreso':'REGRESO',
    'lee' : 'LEE',
    'for':'FOR',
    'while' : 'WHILE'
}

tokens = [
    'ID',
    'CTEI', 'CTEF', 'CTEC',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'DOTS', 'EQUALS', 'SEMICOLON', 'PERIOD', 'COMMA',
    'LESS', 'BIGGER', 'DIFFERENT','EQUAL','BIGGER_EQUAL', 'LESS_EQUAL',
    'L_PARENTHESIS', 'R_PARENTHESIS', 'L_BRACKET', 'R_BRACKET',
    'OR', 'AND'
] + list(reserved.values())

# Expresiones regulares para tokens simples
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
    return t
 #error 
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
#escribe
def t_ESCRIBE(t):
    r'\[escribe]'
    t.type = 'ESCRIBE'
    return t
#float
def t_CTEFLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t
#Int
def t_CTEINT(t):
    r'\d+'
    t.value = int(t.value)
    return t
#construimos el lexico
lexer = lex.lex()
#precedencia de operadores
precedence = (
    ( 'left', 'PLUS', 'MINUS' ),
    ( 'left', 'TIMES', 'DIVIDE' ),
)
# er para el programa
#falta declaracion de variable
def p_programa(p):
    '''
    programa : PROGRAMA ID SEMICOLON declaracion_clases declaracion_funciones principal
    | PROGRAMA ID SEMICOLON
    '''
    p[0] = None
def p_principal(p):
    '''
    principal : L_BRACKET cuerpo R_BRACKET
    '''
    p[0] = None
#falta agregar estatutos repeticion
def p_cuerpo(p) :
    '''
    cuerpo : estatutos_funciones cuerpo
    |
    '''
    p[0] = None
#falta agregar funciones
def p_estatutos_funciones(p):
    '''
    estatutos_funciones : lee
    |
    '''
    p[0] = None
def p_declaracion_parametros(p):
    '''
    declaracion_parametros : tipo_retorno ID declaracion_parametros_aux
	|
    '''
    p[0] = None
def p_declaracion_parametros_aux(p):
    '''
    declaracion_parametros_aux : COMMA declaracion_parametros
    |
    '''
    p[0] = None

def p_lee(p):
    '''
    lee : LEE L_PARENTHESIS variable lee_aux
    '''
    p[0] = None
def p_lee_aux(p):
    '''
    lee_aux : R_PARENTHESIS
    | COMMA  variable lee_aux
    '''
    p[0] = None
def p_variable(p):
    '''
    variable : ID variable_aux
    '''
    p[0] = None
def p_variable_aux(p):
    '''
    variable_aux : PERIOD ID variable_aux
    |
    '''
    p[0] = None
def p_declaracion_clases(p):
    '''
    declaracion_clases : PEQUE ID declaracion_clases_aux declaracion_clases
    |

    '''
    p[0] = None
def p_declaracion_clases_aux(p):
    '''
    declaracion_clases_aux :  L_BRACKET  declaracion_var declaracion_funciones R_BRACKET
    | AGRANDA ID L_BRACKET  declaracion_var declaracion_funciones R_BRACKET
    '''
    p[0] = None
def p_declaracion_var(p):
    '''
    declaracion_var : VARIABLE tipo_retorno ID declaracion_var
    |
    '''
def p_expresion(p):
    '''
    expresion : 
    '''
    p[0] = None


def p_declaracion_funciones(p):
    '''
    declaracion_funciones : declaracion_funciones_aux
    |
    '''
    p[0] = None

def p_declaracion_funciones_aux(p):
    '''
    declaracion_funciones_aux : MINI declaracion_funciones_aux2 ID L_PARENTHESIS declaracion_parametros R_PARENTHESIS L_BRACKET cuerpo declaracion_funciones_aux3 R_BRACKET
    |
    '''
    p[0] = None
def p_declaracion_funciones_aux2(p):
    '''
    declaracion_funciones_aux2 : VOID
    | tipo_retorno
    '''
    p[0] = None
def p_declaracion_funciones_aux3(p):
    '''
    declaracion_funciones_aux3 : regreso
    | 
    '''
    p[0] = None
def p_regreso(p):
    '''
    regreso : REGRESO ID
    '''
    p[0] = None
def p_tipo_retorno(p):
    '''
    tipo_retorno : INT
    | FLOAT
    | CHAR
    '''
    p[0] = None

def p_factor(p):
    '''
    factor : L_BRACKET expresion R_BRACKET
    | CTEI
    | CTEF
    | CTEC
    | variable
    '''
    p[0] = None


def p_error(p):
   if p:
      print("Syntax error at token", p.type)
      print("Syntax error at '%s'" % p.value)
      print("line : '%s'" % p.lineno)
      print("column: '%s'" % p.lexpos)
   else:
      print("Syntax error at EOF")
parser = yacc.yacc()
def prueba(data):
  result = parser.parse(data)
  print(result)

from pathlib import Path

aceptado = Path('prueba.txt').read_text()
aceptado = aceptado
prueba(aceptado)
