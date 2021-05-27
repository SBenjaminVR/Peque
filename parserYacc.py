#--------------------------------------- RE par el lexer---------------------------------------

import re
import ply.lex as lex           # Scanner
import ply.yacc as yacc  
import lexico

AuxList = ['temp', 'tempo']
Cuartetos = []
Temporales = []
Saltos = []
Scope = ['main', '_', '_']
parametros = 1

global cont
cont = 0

Memoria = []
#--------------------------------------- importar cuboSemantico---------------------------------------
from cuboSemantico import cuboSemantico
#cuboSemantico tiene todas las consideraciones semanticas

#-Generacion de codigo de expresiones aritmeticas
from stack import Stack
popper = Stack()
values = Stack()
tipos = Stack()
funct = Stack()
TemporalesFor = Stack()
#--------------------------------------- Variables ncesarias para usar yacc, lista de tokens y lexer---------------------------------------

tokens = lexico.tokens
lexer = lexico.lexer

#--------------function dir symb table ---------
import symbTableFunctions as symb

#-------------- principal---------------

def p_programa(p):
    '''
    programa : PROGRAMA  ID SEMICOLON mainInicio declaracion_clases declaracion_funciones principal
    | PROGRAMA ID SEMICOLON mainInicio
    '''
    CrearCuadruplo('END','_','_','_')

    #addScope(p[2])
    p[0] = None
def p_principal(p):
    '''
    principal : MAIN mainFin L_PARENTHESIS R_PARENTHESIS L_BRACKET  principal_aux cuerpo R_BRACKET 
    '''
    p[0] = None
def p_mainInicio(p):
    '''
    mainInicio : empty
    '''
    CrearCuadruplo('Goto','_','_','_')

    p[0] = None
def p_mainFin(p):
    '''
    mainFin : empty
    '''

    fill(0,cont)


    p[0] = None
def p_principal_aux(p):
    '''
    principal_aux : empty
    '''
    Scope[0] = 'main'
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
    | declaracion_var
    '''
    popper.push('inicio')
    p[0] = None
#-------------- estatutos---------------
#estatutos general
def p_estatutos_funciones(p):
    '''
    estatutos_funciones : input
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
    repeticion_no_condicional : FOR L_PARENTHESIS for_inicio m_exp for_temp TO m_exp for_revision COMMA m_exp for_suma R_PARENTHESIS L_BRACKET cuerpo for_final R_BRACKET 
    '''

    p[0]= None
def p_for_inicio(p):
    '''
    for_inicio : empty
    '''
    
    Saltos.append(cont)
    p[0]= None
def p_for_temp(p):
    '''
    for_temp : empty
    '''
    TemporalesFor.push(values.pop())
    
    
    p[0]= None
def p_for_revision(p):
    '''
    for_revision : empty
    '''
    GenerarNuevoTemporal()
    #chechar por las variables y expresiones
    popper.push('>=')
    GenerarCuadruploDeOperador(popper,values,tipos)
    Saltos.append(cont)
    CrearCuadruplo('GotoF',Temporales[-1],'_','_')

    p[0]= None

def p_for_suma (p):
    '''
    for_suma : empty
    '''
    popper.push('+')
    values.push(TemporalesFor.pop())
    #PENDIENTE REVISION DE TIPOS
    GenerarCuadruploDeOperador(popper,values,tipos)
    p[0]=None
def p_for_final(p):
    '''
    for_final : empty
    '''
    global cont
    falseJump = Saltos[-1]
    Saltos.pop()
    Ret = Saltos[-1]
    Saltos.pop()
    CrearCuadruplo('Goto','_','_',Ret)
    fill(falseJump,cont)
    p[0] = None
#--------------------------While--------------------
def p_repeticion_condicional(p):
    '''
    repeticion_condicional : WHILE startWhile L_PARENTHESIS expresion R_PARENTHESIS checkCond L_BRACKET cuerpo R_BRACKET finalWhile
    '''
    p[0]= None
def p_startWhile(p):
    '''
    startWhile : empty
    '''
    Saltos.append(cont)
    
    p[0] = None
def p_checkCond(p):
    '''
    checkCond : empty
    '''
    global cont

    cond = values.pop()
    tCond = tipos.top()
    print(tCond)

    #if tCond != 'bool' :
     #   print('Error')
    #else :
        #Saltos.append(cont)
        #CrearCuadruplo('GotoF',cond,'_','_')
    Saltos.append(cont)
    CrearCuadruplo('GotoF',cond,'_','_')
    
        

    p[0] = None
def p_finalWhile(p):
    '''
    finalWhile : empty
    '''
    global cont
    falseJump = Saltos[-1]
    Saltos.pop()
    Ret = Saltos[-1]
    Saltos.pop()
    CrearCuadruplo('Goto','_','_',Ret)
    print(falseJump)
    print(cont)
    fill(falseJump,cont)
    
    p[0] = None
#estatutos funcionales
def p_input(p):
    '''
    input : INPUT L_PARENTHESIS variable input_aux
    '''
    print(p[3])
    p[0] = None
def p_lee_aux(p):
    '''
    input_aux : R_PARENTHESIS
    | COMMA  variable input_aux
    '''

    p[0] = None
def p_regreso(p):
    '''
    regreso : REGRESO expresion
    '''
    p[0] = None
def p_llamada(p):
    '''
    llamada : llamadaID startCall llamada_aux L_PARENTHESIS llamada_aux2 R_PARENTHESIS endCall
    '''
    
    p[0]=None
def p_llamadaID(p):
    '''
    llamadaID : ID
    '''
    funct.push(p[1])    
    p[0] = None
def p_startCall(p):
    '''
    startCall : empty
    '''
    global parametros
    parametros = 1
    CrearCuadruplo('ERA',funct.top(),'_','_')
    
    p[0]=None
def p_endCall(p):
    '''
    endCall : empty
    '''
    CrearCuadruplo('GOSUB',funct.top(),'_','_')
    funct.pop()
    p[0]= None
def p_llamada_aux(p):
    '''
    llamada_aux : PERIOD ID
    |
    '''
    p[0]=None
def p_llamada_aux2(p):
    '''
    llamada_aux2 :  parametros endParam  llamada_aux3
    |
    '''
    
    p[0]=None
def p_llamada_aux3(p):
    '''
    llamada_aux3 : COMMA llamada_aux2
    |
    '''
    p[0]=None
#-------------- parametros---------------

def p_parametros(p):
    '''
    parametros : ID parametros_aux 
    | expresion 
    |
    '''
    
    p[0] = None
def p_endParam(p):
    '''
    endParam : empty

    '''
    global parametros
    CrearCuadruplo('Parametro', values.pop(),'_','Param' + str(parametros))
    parametros += 1
    p[0] = None

def p_parametros_aux(p):
    '''
    parametros_aux : PERIOD ID
    |
    '''
    p[0] = None

def p_print(p):
    '''
    escribe : PRINT L_PARENTHESIS print_var R_PARENTHESIS
    '''
    
    p[0] = None

def p_print_var(p):
    '''
    print_var : print_var_aux2 finalVar COMMA print_var
    | print_var_aux2 finalVar
    '''
    p[0] = None
def p_finalVar(p):
    '''
    finalVar : empty
    '''
    res = values.pop()
    CrearCuadruplo('print',res,'_','_')
    p[0] = None

def p_print_var_aux2(p):
    '''
    print_var_aux2 : llamada 
    | expresion
    '''
    
    p[0] = None

def p_asignacion(p):
    '''
    asignacion : ID EQUALS asignacion_aux
    '''
    iz = values.pop()
    CrearCuadruplo(p[2], iz, '_', p[1])
    p[0] = None
def p_asignacion_aux(p):
    '''
    asignacion_aux : expresion
    | arreglo
    | estatutos_funciones
    | ID PERIOD ID
    '''
    p[0] = None
def p_empty(p):
    'empty :'
    pass

def p_condicion(p):
    '''
    condicion : IF L_PARENTHESIS expresion R_PARENTHESIS rp_seen L_BRACKET cuerpo R_BRACKET condicion_aux else_after
    '''
    
    p[0] = None

def p_else_after(p):
    '''
    else_after : empty
    '''

    end = Saltos[-1]
    Saltos.pop()
    fill(end,cont)
    

    p[0] = None
def p_rp_seen(p):
    '''
    rp_seen : empty
    '''
    global cont
    result = Temporales[-1]
    salto = cont
    Saltos.append(salto)
    CrearCuadruplo('GotoF',result,'_','_')
    
    
    p[0] = None
def p_condicion_aux(p):
    '''
    condicion_aux : ELSE else_seen L_BRACKET cuerpo R_BRACKET elseEnd
    |
    '''
    #end = Saltos[-1]
    #Cuartetos[end][res] = end
    p[0] = None
def p_else_seen(p):
    '''
    else_seen : empty
    '''
    global cont

    result = Saltos[-1]
    Saltos.pop()
    Cuartetos.append({'op': 'Goto', 'iz': '_', 'de': '_', 'res':'_'})
    Saltos.append(cont)
    cont += 1
    fill(result,cont)
    # se fillea lo que este en result con el cont actual

    p[0] = None
def p_elseEnd(p):
    '''
    elseEnd : empty
    '''
    Saltos.pop()
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
    declaracion_funciones : declaracion_funciones_aux funciones_end declaracion_funciones 
    |
    '''

    p[0] = None
def p_funciones_end(p):
    '''
    funciones_end : empty
    '''
    CrearCuadruplo('END PROC','_','_','_')
    p[0]= None
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
    declaracion_var_aux2 : tipo_retorno ID declaracion_var_aux3
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
    if (len(p) > 1):
        symb.addVariable(p[2], AuxList[1], len(Memoria))
        Memoria.append(0)
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
    variable : variable_aux2 variable_aux
    '''
    p[0] = None
def p_variable_aux2(p):
    '''
    variable_aux2 : ID empty
    '''
    if symb.CheckIfVariableExists(Scope[0], Scope[1], Scope[2], p[1]):
        print('Simon, existe carnal')
    else:
        raise ErrorMsg('No existe la variable ' + p[1])
    values.push(p[1])
    p[0] = None
def p_variable_aux(p):
    '''
    variable_aux : PERIOD ID
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
    expresion : t_exp expresion_aux2
    | t_exp expresion_aux2 expresion_aux expresion
    '''
    p[0] = None
def p_expresion_aux(p):
    '''
    expresion_aux : OR
    '''
    if (len(p) > 1):
        popper.push(p[1])
    p[0] = None
def p_expresion_aux2(p):
    '''
    expresion_aux2 : empty
    '''
    if popper.top() == '||':
        GenerarCuadruploDeOperador(popper, values, tipos)
    p[0] = None
def p_t_exp(p):
    '''
    t_exp : g_exp t_exp_aux2
    | g_exp t_exp_aux2 t_exp_aux t_exp
    '''
    p[0] = None
def p_t_exp_aux(p):
    '''
    t_exp_aux : AND
    '''
    if (len(p) > 1):
        popper.push(p[1])
    p[0] = None
def p_t_exp_aux2(p):
    '''
    t_exp_aux2 : empty
    '''
    if popper.top() == '&&':
        GenerarCuadruploDeOperador(popper, values, tipos)
    p[0] = None
def p_g_exp(p):
    '''
    g_exp : m_exp g_exp_aux2
    | m_exp g_exp_aux2 g_exp_aux g_exp
    '''
    p[0] = None
def p_g_exp_aux(p):
    '''
    g_exp_aux : BIGGER
    | LESS
    | BIGGER_EQUAL
    | LESS_EQUAL
    | EQUAL
    | DIFFERENT
    '''
    if (len(p) > 1):
        popper.push(p[1])
    p[0] = None
def p_g_exp_aux2(p):
    '''
    g_exp_aux2 : empty
    '''
    operadores = ['>', '<', '>=', '<=', '==', '<>']
    if popper.top() in operadores:
        GenerarCuadruploDeOperador(popper, values, tipos)
    p[0] = None
def p_m_exp(p):
    '''
    m_exp : termino m_exp_aux2
    | termino m_exp_aux2 m_exp_aux m_exp
    '''
    p[0] = None
def p_m_exp_aux(p):
    '''
    m_exp_aux : PLUS
    | MINUS
    '''
    if (len(p) > 1):
        popper.push(p[1])
    p[0] = None
def p_m_exp_aux2(p):
    '''
    m_exp_aux2 : empty
    '''
    if popper.top() == '+' or popper.top() == '-':
        GenerarCuadruploDeOperador(popper, values, tipos)
    p[0] = None
def p_termino(p):
    '''
    termino : factor termino_aux2 termino_aux termino
    | factor termino_aux2
    '''
    p[0] = None
def p_termino_aux(p):
    '''
    termino_aux : TIMES
    | DIVIDE
    '''
    if (len(p) > 1):
        popper.push(p[1])
    p[0] = None
def p_termino_aux2(p):
    '''
    termino_aux2 : empty
    '''
    if popper.top() == '*' or popper.top() == '/':
        GenerarCuadruploDeOperador(popper, values, tipos)
    p[0] = None
def p_factor(p):
    '''
    factor : L_PARENTHESIS factor_aux expresion R_PARENTHESIS factor_aux2
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
    p[0] = None
def p_factor_aux(p):
    '''
    factor_aux : empty
    '''
    popper.push('(')
    p[0] = None
def p_factor_aux2(p):
    '''
    factor_aux2 : empty
    '''
    popper.pop()
    p[0] = None

#-------------- error---------------
class ErrorMsg(Exception):
    def __init__(self, message):
        self.message = message

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
    GenerarNuevoTemporal()
    result = Temporales[-1]
    CrearCuadruplo(operador, valorA, valorB, result)
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

        resultVal, resultType = operacionesSemantica(p[TIPO], lastVal, values.top(), lastType, tipos.top())

        values.pop()
        tipos.pop()

        values.push(resultVal)
        tipos.push(resultType)

def GenerarCuadruploDeOperador(operandos, valores, tipos):
    der = valores.pop()
    iz = valores.pop()
    op = operandos.pop()

    GenerarNuevoTemporal()
    result = Temporales[-1]
    
    CrearCuadruplo(op, iz, der, result)
    valores.push(result)


def CrearCuadruplo(op, iz, der, res):
    global cont
    cont += 1
    Cuartetos.append({'op': op, 'iz': iz, 'de': der, 'res':res})

def GenerarNuevoTemporal():
    Temporales.append('t' + str(len(Temporales)))

def fill(cuarteto, llenado):
    global Cuartetos
    Cuartetos[cuarteto]['res'] = llenado

# crear el parser
parser = yacc.yacc()