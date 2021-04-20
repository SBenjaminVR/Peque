#--------------------------------------- Autores---------------------------------------
# Benjamín Valdez Rodríguez A00822027
#Juan Carlos Garza Lopez A00822601

#ITESM
#--------------------------------------- Autores---------------------------------------

import ply.lex as lex           # Scanner
import ply.yacc as yacc         # Parser
from pathlib import Path        # Read files
import sys

Directory = {
    'Clases': {},
    'Funciones': {},
    'Variables': {}
}
Glovalvar = {}
AuxList = ['temp', 'tempo']

#--------------------------------------- palabras reservadas---------------------------------------
#tokens reservados o palabras reservadas
reserved = {
    'programa': 'PROGRAMA',
    'escribe': 'ESCRIBE',
    'fila' : 'FILA',
    'variable': 'VARIABLE',
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
    'regreso':'REGRESO',
    'lee' : 'LEE',
    'for':'FOR',
    'while' : 'WHILE',
    'to' : 'TO'
}
#--------------------------------------- Tokens---------------------------------------

tokens = [
    'ID',
    'CTEI', 'CTEF', 'CTEC',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'DOTS', 'EQUALS', 'SEMICOLON', 'PERIOD', 'COMMA',
    'LESS', 'BIGGER', 'DIFFERENT','EQUAL','BIGGER_EQUAL', 'LESS_EQUAL',
    'L_PARENTHESIS', 'R_PARENTHESIS', 'L_BRACKET', 'R_BRACKET',
    'OR', 'AND',
    'L_CORCHETE', 'R_CORCHETE',
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
#construimos el lexico
lexer = lex.lex()
#precedencia de operadores
precedence = (
    ( 'left', 'PLUS', 'MINUS' ),
    ( 'left', 'TIMES', 'DIVIDE' ),
)
# er para el programa
#falta declaracion de variable

#--------------------------------------- RE par el lexer---------------------------------------


#--------------function dir symb table ---------
def addVariable(name, type):
    if Directory.get('Variables').get(name) == None:
        Directory['Variables'][name] = {
            'Id': name, 
            'DataType': type
        }

def addFuncion(name, type):
    print('addFuncion name: ' + name + ' type: ' + type)
    if Directory.get('Funciones').get(name) == None:
        Directory['Funciones'][name] = {
            'Id': name, 
            'DataType': type,
            'Variables': {},
            'Parametros': {}
        }

def addScope(name):
    if Directory.get(name) == None:
        Directory[name] = [name,"retorno",{}]
    
def addType(name,type):
    if Directory.get(name) != None:
        Directory[name] = [name,type,{}]
    
def addToScopeVar(name,var):
    if Directory.get(name) != None :
        directoryScope = Directory.get(name)
        if directoryScope[2].get(var) == None :
            directoryScope[2][var] = []
stack = []
#-------------- principal---------------

def p_programa(p):
    '''
    programa : PROGRAMA ID SEMICOLON declaracion_clases declaracion_funciones declaracion_var principal
    | PROGRAMA ID SEMICOLON
    '''
    #addScope(p[2])
    p[0] = None
def p_principal(p):
    '''
    principal : L_BRACKET cuerpo R_BRACKET
    '''
    p[0] = None
#falta agregar estatutos repeticion
def p_cuerpo(p) :
    '''
    cuerpo : cuerpo_aux cuerpo
    |
    '''
    p[0] = None
def p_cuerpo_aux(p) :
    '''
    cuerpo_aux : estatutos_repeticion
    | estatutos_funciones
    '''
    p[0] = None
#-------------- estatutos---------------
#estatutos general
def p_estatutos_funciones(p):
    '''
    estatutos_funciones : lee
    | escribe
    | llamada
    | asignacion
    | condicion
    '''
    p[0] = None
#estatutos repeticion
def p_estatutos_repeticion(p):
    '''
    estatutos_repeticion : estatutos_repeticion_aux
    | 
    '''
    p[0]= None
def p_estatutos_repeticion_aux(p):
    '''
    estatutos_repeticion_aux : estatutos_repeticion_aux2 estatutos_repeticion
    '''
    p[0]= None
def p_estatutos_repeticion_aux2(p):
    '''
    estatutos_repeticion_aux2 : repeticion_condicional
    | repeticion_no_condicional
    '''
    p[0]= None
#repeticion_no_condicional
def p_repeticion_no_condicional(p):
    '''
    repeticion_no_condicional : FOR L_PARENTHESIS m_exp TO m_exp R_PARENTHESIS L_BRACKET cuerpo R_BRACKET
    '''
    p[0]= None
def p_repeticion_condicional(p):
    '''
    repeticion_condicional : WHILE L_PARENTHESIS expresion R_PARENTHESIS L_BRACKET cuerpo R_BRACKET
    '''
    p[0]= None

#estatutos funcionales
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
def p_regreso(p):
    '''
    regreso : REGRESO expresion
    '''
    p[0] = None
def p_llamada(p):
    '''
    llamada : ID llamada_aux L_PARENTHESIS llamada_aux2 R_PARENTHESIS
    '''
    p[0]=None
def p_llamada_aux(p):
    '''
    llamada_aux : PERIOD ID
    |
    '''
    p[0]=None
def p_llamada_aux2(p):
    '''
    llamada_aux2 : parametros llamada_aux3
    |
    '''
    p[0]=None
def p_llamada_aux3(p):
    '''
    llamada_aux3 : COMMA llamada_aux2
    |
    '''
    p[0]=None
def p_escribe(p):
    '''
    escribe : ESCRIBE L_PARENTHESIS escribe_var R_PARENTHESIS
    '''
    p[0] = None
def p_escribe_var(p):
    '''
    escribe_var : escribe_var_aux
    '''
    p[0] = None
def p_escribe_var_aux(p):
    '''
    escribe_var_aux : escribe_var_aux2 COMMA
    | escribe_var_aux2
    '''
    p[0] = None
def p_escribe_var_aux2(p):
    '''
    escribe_var_aux2 : llamada 
    | expresion
    '''
    p[0] = None
def p_asignacion(p):
    '''
    asignacion : VARIABLE ID EQUALS asignacion_aux
    '''
    #addScope(p[2])
    p[0] = None
def p_asignacion_aux(p):
    '''
    asignacion_aux : expresion
    | arreglo
    | estatutos_funciones
    | ID PERIOD ID
    '''
    p[0] = None
def p_condicion(p):
    '''
    condicion : IF L_PARENTHESIS expresion R_PARENTHESIS L_BRACKET cuerpo R_BRACKET condicion_aux
    '''
    p[0] = None
def p_condicion_aux(p):
    '''
    condicion_aux : ELSE L_BRACKET cuerpo R_BRACKET
    |
    '''
    p[0] = None
#-------------- declaraciones---------------

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
def p_declaracion_funciones(p):
    '''
    declaracion_funciones : declaracion_funciones_aux declaracion_funciones
    |
    '''

    p[0] = None

def p_declaracion_funciones_aux(p):
    '''
    declaracion_funciones_aux : MINI declaracion_funciones_aux2 ID L_PARENTHESIS declaracion_parametros R_PARENTHESIS L_BRACKET cuerpo declaracion_funciones_aux3 R_BRACKET
    |
    '''
    AuxList[0] = 'Funcion'
    print('p_delcaracion_funciones_aux ' + AuxList[1])
    addFuncion(p[3], AuxList[1])
    #addScope(p[3])
    p[0] = None
def p_declaracion_funciones_aux2(p):
    '''
    declaracion_funciones_aux2 : VOID
    | tipo_retorno
    '''
    AuxList[1] = p[1]
    print('p_delcaracion_funciones_aux2 ' + AuxList[1])
    p[0] = None
def p_declaracion_funciones_aux3(p):
    '''
    declaracion_funciones_aux3 : regreso
    | 
    '''
    p[0] = None
def p_declaracion_var(p):
    '''
    declaracion_var : declaracion_var_aux
    '''
    p[0] = None
def p_declaracion_var_aux(p):
    '''
    declaracion_var_aux : VARIABLE declaracion_var_aux2 declaracion_var
    |
    '''

    p[0] = None
def p_declaracion_var_aux2(p):
    '''
    declaracion_var_aux2 : tipo_especial ID declaracion_var_aux3
    | tipo_retorno ID declaracion_var_aux5
    '''
    #addScope(p[2])
    addVariable(p[2], AuxList[1])
    p[0] = None
def p_declaracion_var_aux3(p):
    '''
    declaracion_var_aux3 : COMMA ID declaracion_var_aux3
    |
    '''
    #addScope(p[2])
    p[0] = None
def p_declaracion_var_aux5(p):
    '''
    declaracion_var_aux5 : declaracion_var_aux6 
    |
    '''
    p[0] = None
def p_declaracion_var_aux6(p):
    '''
    declaracion_var_aux6 : L_CORCHETE CTEI R_CORCHETE declaracion_var_aux7
    |
    '''
    p[0] = None
def p_declaracion_var_aux7(p):
    '''
    declaracion_var_aux7 : L_CORCHETE CTEI R_CORCHETE
    |
    '''
    p[0] = None

#-------------- Variables---------------

def p_variable(p):
    '''
    variable : ID variable_aux
    '''
    p[0] = None
def p_variable_aux(p):
    '''
    variable_aux : COMMA ID variable_aux
    |
    '''
    p[0] = None
#-------------- Tipos---------------

def p_tipo_especial(p):
    '''
    tipo_especial : FILA
    '''
    p[0] = None
def p_tipo_retorno(p):
    '''
    tipo_retorno : INT
    | FLOAT
    | CHAR
    | BOOL
    '''
    AuxList[1] = p[1]
    p[0] = None
#-------------- parametros---------------

def p_parametros(p):
    '''
    parametros : ID parametros_aux
    | expresion
    |
    '''
    p[0] = None
def p_parametros_aux(p):
    '''
    parametros_aux : PERIOD ID
    |
    '''
    p[0] = None


#-------------- arreglo---------------

def p_arreglo(p):
    '''
    arreglo : ID L_CORCHETE expresion R_CORCHETE arreglo2
    '''
    p[0] = None
def p_arreglo2(p):
    '''
    arreglo2 : L_CORCHETE expresion R_CORCHETE
    |
    '''
    p[0] = None


#-------------- expresiones---------------

def p_expresion(p):
    '''
    expresion : t_exp expresion_aux
    '''
    p[0] = None
def p_expresion_aux(p):
    '''
    expresion_aux : OR expresion
    | 
    '''
    p[0] = None
def p_t_exp(p):
    '''
    t_exp : g_exp t_exp_aux
    '''
    p[0] = None
def p_t_exp_aux(p):
    '''
    t_exp_aux : AND t_exp
    |
    '''
    p[0] = None

def p_g_exp(p):
    '''
    g_exp : m_exp
    | m_exp BIGGER m_exp
    | m_exp LESS m_exp
    | m_exp BIGGER_EQUAL m_exp
    | m_exp LESS_EQUAL m_exp
    | m_exp EQUAL m_exp
    | m_exp DIFFERENT m_exp
    '''
    p[0]=None
def p_m_exp(p):
    '''
    m_exp : termino m_exp_aux
    '''
    p[0] = None
def p_m_exp_aux(p):
    '''
    m_exp_aux : PLUS termino
    | MINUS termino
    |
    '''
    p[0]=None
def p_termino(p):
    '''
    termino : factor termino_aux
    '''
    p[0] = None
def p_termino_aux(p):
    '''
    termino_aux : TIMES factor
    | DIVIDE factor
    |
    '''
    p[0]=None
def p_factor(p):
    '''
    factor : L_BRACKET expresion R_BRACKET
    | CTEI
    | CTEF
    | CTEC
    | variable
    | llamada
    '''
    p[0] = None
#-------------- error---------------

def p_error(p):
   if p:
      print("Syntax error at token", p.type)
      print("Syntax error at '%s'" % p.value)
      print("line : '%s'" % p.lineno)
      print("column: '%s'" % p.lexpos)
   else:
      print("Syntax error at EOF")
#--------------------------------------- Error---------------------------------------

# crear el parser
parser = yacc.yacc()

#--------------------------------------- funciones de prueba---------------------------------------

def prueba(data):
  result = parser.parse(data)
  print(result)


# lectura de archivo
from pathlib import Path

aceptado = Path('prueba.txt').read_text()
aceptado = aceptado
prueba(aceptado)
print(Directory)
