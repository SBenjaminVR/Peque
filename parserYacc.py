#--------------------------------------- RE par el lexer---------------------------------------

import re
import ply.lex as lex           # Scanner
import ply.yacc as yacc  
import math as math
import lexico

AuxList = ['temp', 'tempo']
Cuartetos = []
Temporales = []
Saltos = []
Scope = ['GLOBAL']
parametros = 1
sizeVar = 1
contVarLocal = [0]*10

global lastVar
global DeclVar
global FuncionDeclarada
global cont
global claseDeclarada

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

#-------------- Directorio de Clases y Funciones, Tablas de Variables  ---------
from directory import Directory
Tabla = Directory({}, {}, {})

#--------- Memoria va asignando los espacios de memoria a las variables ----------#
from asignadorMemoria import AsignadorMemoria
memoria = AsignadorMemoria()

#--------- Constantes lleva el control de la tabla de constantes  ----------#
from tablaConstantes import TablaConstantes
Constantes = TablaConstantes()

from tablaOperaciones import TablaOperaciones
Operadores = TablaOperaciones()

#-------------- principal---------------

def p_programa(p):
    '''
    programa : PROGRAMA ID SEMICOLON mainInicio scopeClases declaracion_clases scopeFunction declaracion_funciones scopeMain principal
    | PROGRAMA ID SEMICOLON
    '''
    CrearCuadruplo('END','_','_','_')

    #addScope(p[2])
    p[0] = None

def p_scopeClases(p):
    '''
    scopeClases : empty
    '''
    Tabla.SetScope('class')
    Scope[0] = 'LOCAL'
    p[0] = None

def p_scopeFunction(p):
    '''
    scopeFunction : empty
    '''
    Tabla.SetScope('function')
    Scope[0] = 'LOCAL'
    p[0] = None

def p_scopeMain(p):
    '''
    scopeMain : empty
    '''
    Tabla.SetScope('main')
    Scope[0] = 'GLOBAL'
    p[0] = None

def p_principal(p):
    '''
    principal : MAIN mainFin L_PARENTHESIS R_PARENTHESIS L_BRACKET cuerpo R_BRACKET 
    '''
    p[0] = None
def p_mainInicio(p):
    '''
    mainInicio : empty
    '''
    CrearCuadruplo('GOTO','_','_','_')

    p[0] = None
def p_mainFin(p):
    '''
    mainFin : empty
    '''
    Fill(0,cont)
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
    iz = values.pop()
    GenerarNuevoTemporal('int')
    values.push(Temporales[-1])
    res = values.top()
    TemporalesFor.push(res)
    CrearCuadruplo('=', iz, '_', res)
    
   

    p[0]= None
def p_for_revision(p):
    '''
    for_revision : empty
    '''
    
    #chechar por las variables y expresiones
    popper.push('>=')
    GenerarCuadruploDeOperador(popper,values,tipos)
    Saltos.append(cont)
    CrearCuadruplo('GOTOF',values.pop(),'_','_')
   

    p[0]= None

def p_for_suma (p):
    '''
    for_suma : empty
    '''
   
    p[0]=None
def p_for_final(p):
    '''
    for_final : empty
    '''    
    
    variableFor = TemporalesFor.pop()
    tipo = tipos.pop()
    #falta comprobar tipos del for
    CrearCuadruplo('+',values.pop(),variableFor,variableFor)
    
    global cont
    falseJump = Saltos[-1]
    Saltos.pop()
    Ret = Saltos[-1]
    Saltos.pop()
    CrearCuadruplo('GOTO','_','_',Ret)
    Fill(falseJump,cont)

    
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

    Saltos.append(cont)
    CrearCuadruplo('GOTOF',cond,'_','_')        

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
    CrearCuadruplo('GOTO','_','_',Ret)
    Fill(falseJump,cont)
    
    p[0] = None
#estatutos funcionales
def p_input(p):
    '''
    input : INPUT L_PARENTHESIS input_aux  R_PARENTHESIS
    '''
    
    p[0] = None
def p_input_aux(p):
    '''
    input_aux : input_aux2 leeInput COMMA input_aux
    | input_aux2 leeInput
    '''
def p_leeInput(p):
    '''
    leeInput : empty
    '''
    res = values.pop()
    CrearCuadruplo('INPUT',res,'_','_')
    p[0] = None
def p_input_aux2(p):
    '''
    input_aux2 : variable
    | arreglo
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
    Funcion = funct.pop()
    CrearCuadruplo('GOSUB',Funcion,'_','_')

    Type = Tabla.GetFunctionAttribute(Funcion, 'Type')
    if Type != 'void':
        Address = Tabla.GetFunctionAttribute(Funcion, 'Address')
        GenerarNuevoTemporal(Type)
        Resultado = Temporales[-1]
        values.push(Resultado)
        CrearCuadruplo('=',Address,'_',Resultado)

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
    parametros :  expresion 
    | 
    '''
    
    p[0] = None
def p_endParam(p):
    '''
    endParam : empty

    '''
    global parametros

    CrearCuadruplo('PARAMETRO', values.pop(),'_','Param' + str(parametros))
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
    CrearCuadruplo('PRINT',res,'_','_')
    p[0] = None

def p_print_var_aux2(p):
    '''
    print_var_aux2 : llamada 
    | expresion
    '''
    
    p[0] = None

def p_asignacion(p):
    '''
    asignacion : igualdadVar  
    | igualdadArr
    '''

    p[0] = None
def p_igualdadArr(p):
    '''
    igualdadArr : arreglo EQUALS asignacion_aux
    '''
    iz = values.pop()
    res = values.pop()
    
    CrearCuadruplo(p[2], iz, '_', res)
    p[0] = None
def p_igualdadVar(p):
    '''
    igualdadVar : ID EQUALS asignacion_aux
    '''
    iz = values.pop()
    if not Tabla.CheckIfVariableExists :
        raise ErrorMsg('La variable ' + p[1] + ' no existe')
    else:
        address = Tabla.GetAttribute(p[1],'Address')
        CrearCuadruplo(p[2], iz, '_',address )


    

    p[0]= None
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
def p_rp_seen(p):
    '''
    rp_seen : empty
    '''
    #guardamos direccion del primer salto
    result = Temporales[-1]
    CrearCuadruplo('GOTOF',result,'_','_')
    Saltos.append(cont-1)

    p[0] = None
def p_else_after(p):
    '''
    else_after : empty
    '''
    
    end = Saltos.pop()
    Fill(end,cont)
    

    p[0] = None

def p_condicion_aux(p):
    '''
    condicion_aux : ELSE else_seen L_BRACKET cuerpo R_BRACKET
    |
    '''
    p[0] = None

def p_else_seen(p):
    '''
    else_seen : empty
    '''
    CrearCuadruplo('GOTO','_','_','_')
    falseJ = Saltos.pop()
    Saltos.append(cont-1)
    Fill(falseJ,cont)
    
    # se Fillea lo que este en result con el cont actual

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
    declaracion_clases : PEQUE guardar_nombre_clase declaracion_clases_aux end_class declaracion_clases
    |

    '''


    p[0] = None
def p_end_class(p):
    '''
    end_class : empty
    '''
    CrearCuadruplo('END CLASS','_','_','_')
    p[0]= None

def p_guardar_nombre_clase(p):
    '''
    guardar_nombre_clase : ID
    '''
    global claseDeclarada
    claseDeclarada = p[1]
    if Tabla.CheckIfClassExists(claseDeclarada):
        raise ErrorMsg('La clase ' + claseDeclarada + ' ya habia sido declarada previamente')
    else:
        Tabla.AddClase(claseDeclarada) 
        Tabla.SetClass(claseDeclarada)

    p[0] = None
def p_declaracion_clases_aux(p):
    '''
    declaracion_clases_aux :  L_BRACKET  declaracion_var declaracion_funciones R_BRACKET
    | AGRANDA ID L_BRACKET  declaracion_var declaracion_funciones R_BRACKET
    '''
    p[0] = None
def p_declaracion_funciones(p):
    '''
    declaracion_funciones : declaracion_funciones_aux funciones_end  declaracion_funciones 
    |
    '''
    p[0] = None
def p_funciones_end(p):
    '''
    funciones_end : empty
    '''
    #Guarda contador de variables
    
    
    CrearCuadruplo('END PROC','_','_','_')
    p[0]= None
def p_declaracion_funciones_aux(p):
    '''
    declaracion_funciones_aux : MINI declaracion_funciones_aux2 guardar_nombre_funcion L_PARENTHESIS declaracion_parametros R_PARENTHESIS L_BRACKET cuerpo regreso R_BRACKET save_variables
    |
    '''
    
    p[0] = None
def p_save_variables(p):
    '''
    save_variables : empty
    '''
    copiaDeLista = contVarLocal.copy()
    Tabla.updateFunctionAttribute(FuncionDeclarada,'Space',copiaDeLista)
    p[0]= None
def p_guardar_nombre_funcion(p):
    '''
    guardar_nombre_funcion : ID
    '''
    #se resetea el contador de variables para funciones
    global contVarLocal
    resetConVarFunciones()
    global FuncionDeclarada
    FuncionDeclarada = p[1]
    print(FuncionDeclarada)
    if Tabla.CheckIfFunctionExists(FuncionDeclarada):
        raise ErrorMsg('La funcion ' + FuncionDeclarada + ' ya habia sido declarada previamente')
    else:
        AuxList[0] = 'Funcion'
        address = memoria.AssignMemoryAddress(AuxList[1], 'GLOBAL', 'NORMAL')
        Tabla.AddFunction(FuncionDeclarada, AuxList[1], address)
        Tabla.SetCurrentFunction(FuncionDeclarada)
def p_declaracion_funciones_aux2(p):
    '''
    declaracion_funciones_aux2 : VOID
    | tipo_retorno
    '''
    if p[1] == 'void' :
        AuxList[1] = p[1]
    p[0] = None
def p_regreso(p):
    '''
    regreso : RETURN expresion
    |
    '''
    global FuncionDeclarada
    tipo = Tabla.GetFunctionAttribute(FuncionDeclarada, 'Type')
    if len(p) > 1:
        if tipo == 'void':
            raise ErrorMsg('Las funciones void (' + FuncionDeclarada + ') no deben tener un return')
        else:
            CrearCuadruplo('RETURN', '_', '_', values.pop())
    else:
        if tipo != 'void':
            raise ErrorMsg('Las funciones de tipo ' + tipo + '(' + FuncionDeclarada + ') deben tener un return')
        
    p[0] = None

def p_declaracion_var(p):
    '''
    declaracion_var : declaracion_var_aux
    '''
    p[0] = None
def p_declaracion_var_aux(p):
    '''
    declaracion_var_aux : PETITE declaracion_var_aux2 assignAddress declaracion_var
    |
    '''

def p_assignAddress(p):
    # Funcion que asigna los espacios de memoria faltantes en caso de ser un array o matriz
    '''
    assignAddress : empty
    '''
    global sizeVar
    # Se ignora el primer espacio ya que fue asignado al momento de guardar la variable por primera vez
    for i in range(1, sizeVar):
        agregarContVarFunciones(AuxList[1],'NORMAL')
        memoria.AssignMemoryAddress(AuxList[1], Scope[0], 'NORMAL')

    p[0] = None
def p_declaracion_var_aux2(p):
    '''
    declaracion_var_aux2 : tipo_retorno idChecker declaracion_var_aux3
    | tipo_retorno idChecker declaracion_var_aux5
    | tipo_especial idChecker
    '''
    p[0] = None
def p_idChecker(p):
    '''
    idChecker : ID
    '''
    global sizeVar
    sizeVar = 1
    if Tabla.CheckIfVariableExists(p[1]):
        raise ErrorMsg('La variable ' + p[1] + ' ya habia sido declarada previamente')
    else:
        global DeclVar
        DeclVar = p[1]
        address = memoria.AssignMemoryAddress(AuxList[1], Scope[0], 'NORMAL')
        agregarContVarFunciones(AuxList[1],'NORMAL',sizeVar)
        Tabla.AddVariable(DeclVar, AuxList[1], address, sizeVar)
        Memoria.append(0)

    p[0] = None
def p_declaracion_var_aux3(p):
    '''
    declaracion_var_aux3 : COMMA idChecker declaracion_var_aux3
    |
    '''
    p[0] = None
def p_declaracion_var_aux5(p):
    '''
    declaracion_var_aux5 : L_CORCHETE save_size R_CORCHETE declaracion_var_aux7
    |
    '''
    p[0] = None

def p_save_size(p):
    '''
    save_size : CTEI
    '''
    if p[1] > 0:
        global sizeVar
        sizeVar *= p[1]
        Tabla.UpdateSize(DeclVar,sizeVar)
        Tabla.UpdateArrayLimit(DeclVar, p[1] - 1)
    else: 
        raise ErrorMsg('No se puede declarar el tamaño de un array como menor que 1')
    
    p[0] = None
def p_declaracion_var_aux7(p):
    '''
    declaracion_var_aux7 : L_CORCHETE last_size R_CORCHETE
    |
    '''
    p[0] = None
def p_last_size(p):
    '''
    last_size : CTEI
    '''
    if p[1] > 0:
        global sizeVar
        
        tipo = Tabla.GetAttribute(DeclVar,'Type')
        currentSize = sizeVar
        sizeVar *= p[1]
        Tabla.UpdateSize(DeclVar, sizeVar)
    else: 
        raise ErrorMsg('No se puede declarar el tamaño de una matriz como menor que 1')

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
    if Tabla.CheckIfVariableExists(p[1]):
        address = Tabla.GetAttribute(p[1],'Address')
        values.push(address)
        tipos.push(Tabla.GetAttribute(p[1], 'Type'))
    else:
        raise ErrorMsg('No existe la variable ' + p[1])
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
    AuxList[1] = p[1]
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
    arreglo : startArray L_CORCHETE expresion R_CORCHETE checkLimits arreglo2
    '''
    dirBase = Tabla.GetAttribute( lastVar,'Address')
    popper.push('+')
    values.push(dirBase)
    tipos.push('int')
    GenerarCuadruploDeOperador(popper,values,tipos)

    
    p[0] = None
def p_startArray(p):
    '''
    startArray : ID
    '''
    global lastVar
    lastVar = p[1]
    popper.push('(')
    p[0]= None
def p_checkLimits(p):
    '''
    checkLimits : empty
    '''
    limit = Tabla.GetAttribute( lastVar,'Limit')
    size =  Tabla.GetAttribute( lastVar,'Size')
    tipo = Tabla.GetAttribute( lastVar,'Type')

    CrearCuadruplo('VER',values.top(),0,limit)
    popper.push('*')
    address = Constantes.GetMemoryAddress(math.ceil(size/(limit+1)),'int')
    values.push(address)
    tipos.push('int')
    tipos.push('int')
    GenerarCuadruploDeOperador(popper,values,tipos)
    p[0] = None
def p_arreglo2(p):
    '''
    arreglo2 : L_CORCHETE expresion p_checkLimits2 R_CORCHETE
    |
    '''
    if(popper.top() == '('):
        popper.pop()
    p[0] = None

def p_checkLimits2(p):
    '''
    p_checkLimits2 : empty
    '''
    arrSize = Tabla.GetAttribute(lastVar,'Size')
    limit = Tabla.GetAttribute(lastVar,'Limit')
    columnSize = arrSize / (limit + 1)
    CrearCuadruplo('VER',values.top(),0, columnSize - 1)
    popper.push('+')  
    GenerarCuadruploDeOperador(popper,values,tipos)
    popper.push('+')
    address = Constantes.GetMemoryAddress(1,'int')
    values.push(address)
    tipos.push('int')
    tipos.push('int')
    GenerarCuadruploDeOperador(popper,values,tipos)


    p[0]= None

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
    | variable
    | llamada
    | arreglo
    | CTEI
    | CTEF
    | CTEC
    '''
    if p[1] != '(':
        if isinstance(p[1],int) :
            tipos.push('int')
            address = Constantes.GetMemoryAddress(int(p[1]), 'int')
            values.push(address)
        elif isinstance(p[1],float) :
            tipos.push('float')
            address = Constantes.GetMemoryAddress(float(p[1]), 'float')
            values.push(address)

        elif isinstance(p[1],str) and len(p[1]) == 3 :
            tipos.push('char')
            address = Constantes.GetMemoryAddress(str(p[1]), 'char')
            values.push(address)
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

def GenerarCuadruploDeOperador(operandos, valores, tipos):
    der = valores.pop()
    iz = valores.pop()
    op = operandos.pop()
    tipoDer = tipos.pop()
    tipoIzq = tipos.pop()

    tipoResultado = cuboSemantico[tipoIzq][tipoDer][op]

    if (tipoResultado != 'err'):
        GenerarNuevoTemporal(tipoResultado)
        result = Temporales[-1]
        
        CrearCuadruplo(op, iz, der, result)
        valores.push(result)
    else:
        raise ErrorMsg('Error en los tipos de la operacion: ' 
        + iz + ' (' + tipoIzq + ') '
        + op + ' ' 
        + der + ' (' + tipoDer + ') ')


def CrearCuadruplo(op, iz, der, res):
    global cont
    cont += 1
    Cuartetos.append({'op': Operadores.GetNumber(op), 'iz': iz, 'de': der, 'res':res})

def GenerarNuevoTemporal(tipo):
    agregarContVarFunciones(tipo,'TEMPORAL')
    addressTemporal = memoria.AssignMemoryAddress(tipo,Scope[0],'TEMPORAL')
    Temporales.append(addressTemporal)
    tipos.push(tipo)

def Fill(cuarteto, llenado):
    global Cuartetos
    Cuartetos[cuarteto]['res'] = llenado
def agregarContVarFunciones(type,location,size=1):
    global contVarLocal
    if location == 'NORMAL':
        if(type == 'int'):
            contVarLocal[0]  = contVarLocal[0] + size
        elif(type == 'float'):
            contVarLocal[1]  = contVarLocal[1] + size
        elif(type == 'char'):
            contVarLocal[2]  = contVarLocal[2] + size
        elif(type == 'bool'):
            contVarLocal[3]  = contVarLocal[3] + size
        else:
            contVarLocal[4]  = contVarLocal[4] + size
    else:
        if(type == 'int'):
            contVarLocal[5]  = contVarLocal[5] + size 
        elif(type == 'float'):
            contVarLocal[6]  = contVarLocal[6] + size 
        elif(type == 'char'):
            contVarLocal[7]  = contVarLocal[7] + size
        elif(type == 'bool'):
             contVarLocal[8]  = contVarLocal[8] + size
        else:
            contVarLocal[9]  = contVarLocal[9] + size
    
def resetConVarFunciones():
    global contVarLocal
    contVarLocal.clear()
    contVarLocal = [0]*10
    
def getContVarFunciones(type,location):
    if location == 'NORMAL':
        if(type == 'int'):
            return contVarLocal[0] 
        elif(type == 'float'):
            return contVarLocal[1] 
        elif(type == 'char'):
            return contVarLocal[2]
        elif(type == 'bool'):
            return contVarLocal[3]
        else:
            return contVarLocal[4]
    else:
        if(type == 'int'):
            return contVarLocal[5] 
        elif(type == 'float'):
            return contVarLocal[6] 
        elif(type == 'char'):
            return contVarLocal[7]
        elif(type == 'bool'):
            return contVarLocal[8]
        else:
            return contVarLocal[9]


# crear el parser
parser = yacc.yacc()