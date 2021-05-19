#--------------------------------------- RE par el lexer---------------------------------------

import ply.lex as lex           # Scanner
import ply.yacc as yacc  
import lexico

AuxList = ['temp', 'tempo']
Cuartetos = []
Temporales = []
Memoria = []
#--------------------------------------- importar cuboSemantico---------------------------------------
from cuboSemantico import cuboSemantico
#cuboSemantico tiene todas las consideraciones semanticas

#-Generacion de codigo de expresiones aritmeticas
from stack import Stack
popper = Stack()
values = Stack()
tipos = Stack()

#--------------------------------------- Variables ncesarias para usar yacc, lista de tokens y lexer---------------------------------------

tokens = lexico.tokens
lexer = lexico.lexer

#--------------function dir symb table ---------
import symbTableFunctions as symb

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
    popper.push('inicio')
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
    symb.addFuncion(p[3], AuxList[1])
    #addScope(p[3])
    p[0] = None
def p_declaracion_funciones_aux2(p):
    '''
    declaracion_funciones_aux2 : VOID
    | tipo_retorno
    '''
    AuxList[1] = p[1]
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
    symb.addVariable(p[2], AuxList[1], len(Memoria))
    Memoria.append(0)
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
    if len(p) > 2:
        realizarCuartetosBinarios(p,popper,values,tipos)
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
    if len(p) > 1:
        realizarCuartetos(p,popper,values,tipos)



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
    if len(p) > 1:
        realizarCuartetos(p,popper,values,tipos)
    
    p[0]=None
def p_factor(p):
    '''
    factor : L_PARENTHESIS expresion R_PARENTHESIS
    | CTEI
    | CTEF
    | CTEC
    | variable
    | llamada
    '''
    if p[1] != '(':
        if isinstance(p[1],int) :
            tipos.push('int')
            values.push(int(p[1]))
        elif isinstance(p[1],float) :
            tipos.push('float')
            values.push(float(p[1]))
        elif isinstance(p[1],str) and len(p[1]) == 3 :
            tipos.push('char')
            values.push(p[1][1])
        
        #values.printStack()
    #else :
       # values.push('FF')
    
    #algoritmo de quartos
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

def imprimirP(p):
    for i in range(len(p)):
        if (i != 0):
            print(p[i], end=" ")
    print()

def operacionesSemantica(operador,valorA,valorB,tipoA,tipoB):
    tipo = cuboSemantico[tipoA][tipoB][operador]
    result = None
    """
    if operador == '*':
        result = valorB * valorA
    elif operador == '/':
        result = valorB / valorA
    elif operador == '+':
        result = valorB + valorA
    elif operador == '-':
        result = valorB - valorA
    elif operador == '>=':
        result = True if valorB >= valorA else False
    elif operador == '==':
        result = True if valorB == valorA else False
    elif operador == '<=':
        result = True if valorB <= valorA else False
    elif operador == '<':
        result = True if valorB < valorA else False
    elif operador == '>':
        result = True if valorB > valorA else False
    elif operador == '!=':
        result = True if valorB != valorA else False
    else:
        result = 'err'
    """
    result = 't' + str(len(Temporales))
    agregarCuarteto(operador, valorA, valorB, result)
    return result,tipo

def realizarCuartetosBinarios(p,popper,values,tipos):
    TIPO = 2
    HacerOperacionSemanticaYCuartetos(p, popper, values, tipos, TIPO)


def realizarCuartetos(p,popper,values,tipos):
    TIPO = 1
    HacerOperacionSemanticaYCuartetos(p, popper, values, tipos, TIPO)

def HacerOperacionSemanticaYCuartetos(p, popper, values, tipos, TIPO):
    popper.push(p[1])
    if values.length() >= 2:
        lastVal = values.top()
        lastType = tipos.top()
        values.pop()
        tipos.pop()
        resultVal, resultType= operacionesSemantica(p[TIPO],lastVal,values.top(),lastType,tipos.top())
        values.pop()
        tipos.pop()
        Temporales.append(resultVal)
        values.push(resultVal)
        tipos.push(resultType)

def agregarCuarteto(op, iz, der, res):
    Cuartetos.append({'op': op, 'iz': iz, 'de': der, 'res':res})

# crear el parser
parser = yacc.yacc()