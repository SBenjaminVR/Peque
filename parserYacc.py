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
parametros = {}
sizeVar = 1
contVarLocal = [0]*9
LocationTemp = 'class'
Location = 'class'

paramChecktype = []
global lastVar
global DeclVar
global Funcion
global FuncionDeclarada
global cont
global claseDeclarada
global atributos

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
Tabla = Directory({}, {}, {}, {})

#--------- Memoria va asignando los espacios de memoria a las variables ----------#
from asignadorMemoria import AsignadorMemoria
memoria = AsignadorMemoria()

#--------- Constantes lleva el control de la tabla de constantes  ----------#
from tablaConstantes import TablaConstantes
Constantes = TablaConstantes()

from tablaOperaciones import TablaOperaciones
Operadores = TablaOperaciones()

#-------------- principal---------------

#program creates the end quadruple for the VM
def p_programa(p):
    '''
    programa : PROGRAMA ID SEMICOLON scopeClases declaracion_clases scopeFunction declaracion_funciones scopeMain principal
    | PROGRAMA ID SEMICOLON
    '''
    CrearCuadruplo('END','_','_','_')

    #addScope(p[2])
    p[0] = None
#neuralgic point to set the class scope and the location, also created the first quadruple to goto the main
def p_scopeClases(p):
    '''
    scopeClases : empty
    '''
    CrearCuadruplo('GOTO','_','_','_')
    Tabla.SetScope('class')
    Location = 'class'
    Scope[0] = 'LOCAL'
    p[0] = None
#neuralgic point to set the function scope
def p_scopeFunction(p):
    '''
    scopeFunction : empty
    '''
    Tabla.SetScope('function')
    Location = 'function'
    Scope[0] = 'LOCAL'
    p[0] = None
#neuralgic point to set the main scope
def p_scopeMain(p):
    '''
    scopeMain : empty
    '''
    Tabla.SetScope('main')
    Location = 'main'
    Scope[0] = 'GLOBAL'
    p[0] = None

#main sctructure of our language
def p_principal(p):
    '''
    principal : MAIN mainFin L_PARENTHESIS R_PARENTHESIS L_BRACKET cuerpo R_BRACKET 
    '''
    p[0] = None
#neuralgic point to fill the first GOTO with the jump quadruple address
def p_mainFin(p):
    '''
    mainFin : empty
    '''
    Fill(0,cont)
    p[0] = None
#cuerpo main estructure
def p_cuerpo(p) :
    '''
    cuerpo : cuerpo_aux cuerpo
    |
    '''
    p[0] = None
#cuerpo options, you can used any of this structure in the body of our language
def p_cuerpo_aux(p) :
    '''
    cuerpo_aux : estatutos_repeticion
    | estatutos_funciones
    | declaracion_var
    | instancear_objetos
    | regreso
    '''
    p[0] = None
#-------------- estatutos---------------

#All the options our language have to choose between function statements
def p_estatutos_funciones(p):
    '''
    estatutos_funciones : input
    | escribe
    | llamada
    | asignacion
    | condicion
    | listas
    '''
#listas declaraction main structure
def p_listas(p):
    '''
    listas : ID METOD ID L_PARENTHESIS expresion R_PARENTHESIS
    | ID METOD ID L_PARENTHESIS  R_PARENTHESIS


    '''
    #crete the address and type structure
    address = -1
    tipo = ''
    #Check if the list name exist in any other variable, if they exist add the type and address to their respective variables
    if  Tabla.CheckIfVariableExists(p[1],Location):
        address = Tabla.GetAttribute(p[1],'Address',Location)
        tipo = Tabla.GetAttribute(p[1],'Type',Location)
        
    else:
        #check if the list name exists in any other scope as a variable or atribute
        if Tabla.CheckIfFunctExistInAtribute(p[1],Location):
            address = Tabla.GetAttributeForParameters(p[1],'Address',Location)
            tipo = Tabla.GetAttribute(p[1],'Type',Location)
        else :
            raise ErrorMsg('No existe la variable ' + p[1])
    
    #------------------Append---------------------#
    #take the type from the temporal and add list_ to the type, so you can have it in the list format
    #that why you can check if they are of the same type
    if p[3] == 'append':
        if(len(p) <= 6):
            raise ErrorMsg(p[3] + 'debe tener un argumento')
        typeCheckTemp = tipos.pop() #check if the type of the list and the expression are the same
        typeCheckAns = 'list_' + typeCheckTemp
        if typeCheckAns != tipo :
            raise ErrorMsg(p[3] + ' el argumento debe ser un ' + tipo + ' se dio un tipo: ' + typeCheckAns)
        CrearCuadruplo('APPEND', values.pop(), '_', address) #created the quadruple
    #------------------POP---------------------#
    elif p[3] == 'pop':
        if(len(p) > 6):
            raise ErrorMsg(p[3] + ' no debe tener argumentos')
        CrearCuadruplo('POP',address,'_','_') #create the pop quadruple
    #------------------Sort---------------------#
    elif p[3] == 'sort':
        if(len(p) > 6):
            raise ErrorMsg(p[3] + ' no debe tener argumentos')
        CrearCuadruplo('SORT',address,'_','_') #create teh sort quadruple
   #------------------find---------------------#
   #take the type from the temporal and add list_ to the type, so you can have it in the list format
    #that why you can check if they are of the same type
    elif p[3] == 'find':
        if(len(p) <= 6):
            raise ErrorMsg(p[3] + 'debe tener un argumento')
        typeCheckTemp = tipos.pop()
        typeCheckAns = 'list_' + typeCheckTemp
        if typeCheckAns != tipo :
            raise ErrorMsg(p[3] + ' el argumento debe ser: ' + tipo + ' y se dio un tipo: ' + typeCheckAns)
        #set the type to the same type of the list
        val = values.pop()
        if(tipo == 'list_int'):
            tipo ='int'
        if(tipo == 'list_bool'):
            tipo ='bool'
        if(tipo == 'list_float'):
            tipo ='float'
        #created a temporal with the same type has the list type
        addressTemp = GenerarNuevoTemporal(tipo)
        values.push(addressTemp)
        CrearCuadruplo('FIND',address,val,addressTemp)#created the quadruple
    #------------------Head---------------------#
    elif p[3] == 'head':
        if(len(p) > 6):
            raise ErrorMsg(p[3] + ' no debe tener argumetos')
        #set the type to the same type of the list
        if(tipo == 'list_int'):
            tipo ='int'
        if(tipo == 'list_bool'):
            tipo ='bool'
        if(tipo == 'list_float'):
            tipo ='float'
        #created a temporal with the same type has the list type
        addressTemp = GenerarNuevoTemporal(tipo)
        values.push(addressTemp)
        CrearCuadruplo('HEAD',address,'_',addressTemp)
    #------------------Tail---------------------#
    elif p[3] == 'tail':
        if(len(p) > 6):
            raise ErrorMsg(p[3] + ' no debe tener argumetos')
        #set the type to the same type of the list
        if(tipo == 'list_int'):
            tipo ='int'
        if(tipo == 'list_bool'):
            tipo ='bool'
        if(tipo == 'list_float'):
            tipo ='float'
        #created a temporal with the same type has the list type
        addressTemp = GenerarNuevoTemporal(tipo)
        values.push(addressTemp)
        CrearCuadruplo('TAIL',address,'_',addressTemp) #created the quadruple
    #------------------Key---------------------#
    #
    elif p[3] == 'key':
        if(len(p) <= 6):
            raise ErrorMsg(p[3] + 'debe tener 1 argumento')
        typeCheckTemp = tipos.pop()
        typeCheckAns = typeCheckTemp
        if typeCheckAns != 'int' :
            raise ErrorMsg(p[3] + ' el argmunto debe ser un ' + 'int' + ' se dio un tipo: ' + typeCheckAns)
        #set the type to the same type of the list
        val = values.pop()
        if(tipo == 'list_int'):
            tipo ='int'
        if(tipo == 'list_bool'):
            tipo ='bool'
        if(tipo == 'list_float'):
            tipo ='float'
        #created a temporal with the same type has the list type
        addressTemp = GenerarNuevoTemporal(tipo)
        values.push(addressTemp)
        CrearCuadruplo('KEY',address,val,addressTemp)#created the key quadruple
    else:
        raise ErrorMsg('No existe el metodo para lista ' + p[3])

   
    p[0] = None
#estatutos repeticion
#loop-statements basic structure
def p_estatutos_repeticion(p):
    '''
    estatutos_repeticion : estatutos_repeticion_aux
    | 
    '''
    p[0]= None
#structure so the statement can be repeat
def p_estatutos_repeticion_aux(p):
    '''
    estatutos_repeticion_aux : estatutos_repeticion_aux2 estatutos_repeticion
    '''
    p[0]= None
    #structure to select between non conditional and condicional statements
def p_estatutos_repeticion_aux2(p):
    '''
    estatutos_repeticion_aux2 : repeticion_condicional
    | repeticion_no_condicional
    '''

    p[0]= None
#For non condiciontal loop statement
#basic structure for(exp to exp,exp){body}
def p_repeticion_no_condicional(p):
    '''
    repeticion_no_condicional : FOR L_PARENTHESIS for_inicio m_exp for_temp TO m_exp for_revision COMMA m_exp for_suma R_PARENTHESIS L_BRACKET cuerpo for_final R_BRACKET 
    '''

    p[0]= None
#neuralgic point to save the quadruple position before starting the for inside the quadruples
def p_for_inicio(p):
    '''
    for_inicio : empty
    '''
    Saltos.append(cont)
    p[0]= None
#NP to check the first expression and created a temporal local address for that expression
def p_for_temp(p):
    '''
    for_temp : empty
    '''
    
    iz = values.pop()
    
    GenerarNuevoTemporal(tipos.pop())
    values.push(Temporales[-1])
    if tipos.top() != 'int': #check if the expression is an int
        raise ErrorMsg('se esperaba un tipo int or float en la expresion del for')
    res = values.top()
    TemporalesFor.push(res)
    CrearCuadruplo('=', iz, '_', res) #assign the value of the expression to the temporal we created earlier
    
   

    p[0]= None
#NP to check the second expression
def p_for_revision(p):
    '''
    for_revision : empty
    '''
    
    if tipos.top() != 'int': # check if the expression is an int type result
        raise ErrorMsg('se esperaba un tipo int or float en la expresion del for')
    popper.push('<=')#push the operation
    GenerarCuadruploDeOperador(popper,values,tipos)#generate the condicional quadruple
    Saltos.append(cont)#append the jump before the expression, the one that has the result of expression, this is so the VM can now when to stop the for loop
    CrearCuadruplo('GOTOF',values.pop(),'_','_') #created the GOTOF with the address of the expression 
   

    p[0]= None


def p_for_suma (p):
    '''
    for_suma : empty
    '''
    #check if the third expression is of int type
    if tipos.top() != 'int':
        raise ErrorMsg('se esperaba un tipo int or float en la expresion del for')
    p[0]=None
#final NP that add the step to the temporal created
def p_for_final(p):
    '''
    for_final : empty
    '''    
    #pop out the temporal and its type
    variableFor = TemporalesFor.pop()
    tipo = tipos.pop()
    #created the sum between the temporal and the step
    CrearCuadruplo('+',values.pop(),variableFor,variableFor)
    
    global cont
    #save the false jump
    falseJump = Saltos[-1]
    Saltos.pop()#pop out the false jump
    Ret = Saltos[-1]#save the starting jump
    Saltos.pop()
    CrearCuadruplo('GOTO','_','_',Ret+1)#created the queadruple you need to return to the start of for
    Fill(falseJump,cont)#fill the quadruple of GOTOF with the position of the exiting quadrupl, so the VM can exit the for when teh condition is fake

    
    p[0] = None
#--------------------------While--------------------

#while loop statement
def p_repeticion_condicional(p):
    '''
    repeticion_condicional : WHILE startWhile L_PARENTHESIS expresion R_PARENTHESIS checkCond L_BRACKET cuerpo R_BRACKET finalWhile
    '''
    p[0]= None

    #np to save the starting point of the while
def p_startWhile(p):
    '''
    startWhile : empty
    '''
    Saltos.append(cont)
    
    p[0] = None
#NP to check the expression inside the while is a bool and save the jumping of the GOTOF and created the quadruple
def p_checkCond(p):
    '''
    checkCond : empty
    '''
    global cont

    cond = values.pop()
    tCond = tipos.top()
    if tCond != 'bool':
        raise ErrorMsg('Se esperaba un tipo bool en el while')
    Saltos.append(cont)
    CrearCuadruplo('GOTOF',cond,'_','_')        

    p[0] = None
#fill the gotof with the exiting number of the queadruple and created the GOTO, so the VM can return to the condiont and check it again
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
#input basic structure
def p_input(p):
    '''
    input : INPUT L_PARENTHESIS input_aux  R_PARENTHESIS
    '''
    
    p[0] = None
#structure so you can have multiple input values
def p_input_aux(p):
    '''
    input_aux : input_aux2 leeInput COMMA input_aux
    | input_aux2 leeInput
    '''
#NP to created the Input quadruple
def p_leeInput(p):
    '''
    leeInput : empty
    '''
    res = values.pop()
    tipo = tipos.pop()
    CrearCuadruplo('INPUT',res,tipo,'_')
    p[0] = None
#you can have variables, arrays and object atributes has a input 
def p_input_aux2(p):
    '''
    input_aux2 : variable
    | arreglo
    | atributo
    '''

    p[0] = None
#basic structure of a function call
def p_llamada(p):
    '''
    llamada : llamadaID startCall L_PARENTHESIS llamada_aux2 R_PARENTHESIS  endCall
    '''
    
    p[0]=None
#check the id of the call
def p_llamadaID(p):
    '''
    llamadaID : ID
    | ID PERIOD ID

    '''
    popper.push('(') #put a fake in the popper, so you separed teh call operations with the actual expression
    
    
    global paramChecktype
    paramChecktype = []
    memoria.ResetLocalMemory()#reset the variable local memory
    if(len(p) > 2):
        funct.push(p[3]) #push the id
        funct.push(p[2])#push the period
    funct.push(p[1])#push the actual id of the call
    p[0] = None
def p_startCall(p):
    '''
    startCall : empty
    '''
    #created the era based for the starting part of the function
    Funcion = funct.pop()
    if funct.top() == '.':
        funct.pop()
        objeto = funct.pop()
        temp = objeto
        objeto = Funcion
        Funcion = temp
        funct.push(objeto)
        funct.push('.')
        CrearCuadruplo('ERA',Funcion,'_', objeto)# push the actual object if the function is in a object class

    else:
        CrearCuadruplo('ERA',Funcion,'_', '_') #Created the era with the function ID
    
    funct.push(Funcion)
    
    p[0]=None
def p_endCall(p):
    '''
    endCall : empty
    '''
    global DeclVar
    Funcion = funct.pop()
    objeto = None
    popper.pop()

    #check if the function is part of a class
    if funct.top() == '.':
        funct.pop()
        objeto = funct.pop()
        
        tempScope = Tabla.Scope
        Tabla.SetScope('class')
        #search if the object exist
        if not Tabla.CheckIfObjectExists(objeto):
            raise ErrorMsg('no existe el objeto')
        
        clase = Tabla.GetObjectAtr(objeto,'Clase')
        Tabla.SetClass(clase)
        padre = Tabla.GetClassAtribute(clase,'Padre')
        #check if the object father class exist
        if not Tabla.CheckIfObjectExists(objeto):
            raise ErrorMsg('no existe el objeto')
        #check if the function exist inside the father
        if not Tabla.CheckIfFunctionExists(Funcion) :
            if padre == None:
                raise ErrorMsg('no existe la llamada')
            else:
                Tabla.SetClass(padre)
                if not Tabla.CheckIfFunctionExists(Funcion):
                    raise ErrorMsg('no existe la llamada')
        #save the parameters of the function
        parametrosFunct = Tabla.GetFunctionAttribute(Funcion, 'Parametros')
       #see if you have the same lenght of parameters
        if len(paramChecktype) != len(parametrosFunct):
            raise ErrorMsg('Incorrecto numero de parametros')
        #see if the parameters types match the ones with the call
        for k in parametrosFunct.values() :
            tipo = k.get('Type')
            for i in paramChecktype:
                if k.get('Type') != i:
                    raise ErrorMsg('parametros no son del mismo tipo que el instanceado en ' + Funcion + ' se dio un ' + i + ' se esperaba un ' + tipo)
        
        Type = Tabla.GetFunctionAttribute(Funcion, 'Type')
        start = Tabla.GetFunctionAttribute(Funcion, 'Start')
        CrearCuadruplo('GOSUB',Funcion,objeto,start)#created the quadruple
        #see if the function return something
        if Type != 'void':
            #if it does save the address of the funciton
            AddressA = Tabla.GetFunctionAttribute(Funcion, 'Address')
            #created a temporal to store the value of the call
            GenerarNuevoTemporal(Type)
            Resultado = Temporales[-1]
            values.push(Resultado)
            #save the address of the object
            AddressB = Tabla.GetObjectAtr(objeto,'Address')
            #make the address of the call be the address of the object . the address of the object ex 1000.1 where 1000 is teh object and 1 the function inside
            Address = str(AddressB) + '.'+ str(AddressA)
            #created the cuadruple with the address of the object and the new temporal we created
            CrearCuadruplo('=',Address,'_',Resultado)
            Tabla.SetScope(tempScope)
    else:
        parametrosFunct = Tabla.GetFunctionAttribute(Funcion, 'Parametros')
        #see if you have the same lenght of parameters
        if len(paramChecktype) != len(parametrosFunct):
            raise ErrorMsg('Incorrecto numero de parametros')
        listaTipos = []
        #see if the parameters types match the ones with the call
        for k in parametrosFunct.values() :
            tipo = k.get('Type')
            for i in paramChecktype:
                if k.get('Type') != i:
                    raise ErrorMsg('parametros no son del mismo tipo que el instanceado en ' + Funcion + ' se dio un ' + i + ' se esperaba un ' + tipo)
        
        #save the type of the function
        start = Tabla.GetFunctionAttribute(Funcion, 'Start')
        CrearCuadruplo('GOSUB',Funcion,'_',start)
        Type = Tabla.GetFunctionAttribute(Funcion, 'Type')
        if Type != 'void':
            #if the function has a return created a temporal to store the value
            #then created teh quadruple to assing the return value to rhe temporal
            Address = Tabla.GetFunctionAttribute(Funcion, 'Address')
            GenerarNuevoTemporal(Type)
            Resultado = Temporales[-1]
            values.push(Resultado)

            CrearCuadruplo('=', Address, '_' ,Resultado)

    p[0]= None

#structure to have multiples parameters
    
def p_llamada_aux2(p):
    '''
    llamada_aux2 :  parametros  llamada_aux3
    |
    '''
    p[0]=None
    #comma to separeted betweeb parameters
def p_llamada_aux3(p):
    '''
    llamada_aux3 : COMMA llamada_aux2
    |
    '''
    p[0]=None
#-------------- parametros---------------
#save the parameters in a local memory address and created the quadruple
def p_parametros(p):
    '''
    parametros : expresion
    '''
    global paramChecktype
    paramChecktype.append(tipos.top())
    address = memoria.AssignMemoryAddress(tipos.pop(),'LOCAL',Location)
    CrearCuadruplo('PARAMETRO', values.pop(),'_',address)
    
    p[0] = None

#PRINT BASIC STRUCTURE
def p_print(p):
    '''
    escribe : PRINT L_PARENTHESIS print_var R_PARENTHESIS
    '''
    
    p[0] = None
#structure to have multiple parameters in print
def p_print_var(p):
    '''
    print_var : print_var_aux2 finalVar COMMA print_var
    | print_var_aux2 finalVar
    '''
    p[0] = None
#NP to created the quadruple of print
def p_finalVar(p):
    '''
    finalVar : empty
    '''
    res = values.pop()
    tipos.pop()
    CrearCuadruplo('PRINT',res,'_','_')
    p[0] = None
#parameters print can have
def p_print_var_aux2(p):
    '''
    print_var_aux2 : llamada 
    | expresion
    | atributo
    | listas
    '''
    
    p[0] = None
#allocation basic structure
def p_asignacion(p):
    '''
    asignacion : igualdadVar  
    | igualdadArr
    | igualdadAtr
    '''

#allocation structure for atributes
#created teh quadruple and store it
    p[0] = None
def p_igualdadAtr(p):
    '''
    igualdadAtr : atributo EQUALS asignacion_aux
    '''
    iz = values.pop()
    res = values.pop()

    tipo1 = tipos.pop()
    tipo2 = tipos.pop()

    if tipo1 != tipo2:
        raise ErrorMsg('Error: No se pueden asignar '+ tipo1 + ' a un tipo ' + tipo2)
    
    CrearCuadruplo('=', iz, '_', res)
    p[0] = None

#atribute basic structure
def p_atributo(p):
    '''
    atributo : ID PERIOD ID 
    '''
    objeto = p[1]
    atributo = p[3]
    
    #check if the object exist
    if not Tabla.CheckIfObjectExists(objeto):
        raise ErrorMsg('El objeto ' + p[1] + ' no existe')
    else:
        #save the object address
        addressA = Tabla.GetObjectAtr(objeto,'Address')
        clase = Tabla.GetObjectAtr(objeto,'Clase')
        TempScope = Tabla.Scope
        Tabla.SetScope('class')
        Tabla.SetClass(clase)
        padre = Tabla.GetClassAtribute(clase,'Padre')
        #check if teh variable exist in the scope and save the  adress
        if Tabla.CheckIfVariableExists(atributo,'class'):

            addressB = Tabla.GetAttribute(atributo,'Address','class')
            addressFinal = str(addressA)+'.' + str(addressB)
            tipo = Tabla.GetAttribute(atributo,'Type','class')
            values.push(addressFinal)
            tipos.push(tipo)
        elif padre != None: #check if the object class has a father and search the atribute their
                Tabla.SetScope('class')
                Tabla.SetClass(padre)
                #check if the variable exist
                if Tabla.CheckIfVariableExists(atributo,'class'):
                    #push the value of the address to the values stack
                    addressB = Tabla.GetAttribute(atributo,'Address','class')
                    addressFinal = str(addressA)+'.' + str(addressB)
                    tipo = Tabla.GetAttribute(atributo,'Type','class')
                    values.push(addressFinal)
                    tipos.push(tipo)
                else:
                    raise ErrorMsg('El objeto ' + p[1] + ' no contiene '+p[3])
        else:
            raise ErrorMsg('El objeto ' + p[1] + ' no contiene '+p[3])
        Tabla.SetScope(TempScope)
    





        
        


    p[0] = None
    #pus the array address to the value adn his expression and created the quadruple
def p_igualdadArr(p):
    '''
    igualdadArr : arreglo EQUALS asignacion_aux
    '''

    iz = values.pop()
    res = values.pop()
    
    tipo1 = tipos.pop()
    tipo2 = tipos.pop()
    if tipo1 != tipo2:
        raise ErrorMsg('Error: No se pueden asignar '+ tipo1 + ' a un tipo ' + tipo2)

    CrearCuadruplo(p[2], iz, '_', res)
    p[0] = None
    #save th
def p_igualdadVar(p):
    '''
    igualdadVar : ID EQUALS asignacion_aux
    '''
    #check if the variable exist
    if Tabla.CheckIfVariableExists(p[1],Location) :
        iz = values.pop()
        tipo = tipos.pop()
        #see if the variable is the same type has the expression
        if tipo != Tabla.GetAttribute(p[1],'Type',Location):
            raise ErrorMsg('Error: No se pueden asignar a: ' + p[1] + ' el tipo ' + tipo + ' ya que es de tipo ' + Tabla.GetAttribute(p[1],'Type',Location) )
        address = Tabla.GetAttribute(p[1],'Address',Location)
        CrearCuadruplo(p[2], iz, '_',address ) #created the quadruple

    else:
        #see if the variable exist inside the atribute of a class
        if Tabla.CheckIfFunctExistInAtribute(p[1],Location):
            iz = values.pop()
            tipo = tipos.pop()
            #see if the variable is the same type has the expression
            if tipo != Tabla.GetAttributeForParameters(p[1],'Type',Location):
                raise ErrorMsg('Error: No se pueden asignar a ' + p[1] + ' el tipo ' + tipo + ' ya que es de tipo ' + Tabla.GetAttributeForParameters(p[1],'Type',Location) )
            address = Tabla.GetAttributeForParameters(p[1],'Address',Location)
            CrearCuadruplo(p[2], iz, '_',address )#created the quadruple
        else:
            raise ErrorMsg('La variable ' + p[1] + ' no existe')

    

    p[0]= None
#right side possible values of the assigment
def p_asignacion_aux(p):
    '''
    asignacion_aux : expresion
    | arreglo
    | estatutos_funciones
    | atributo
    '''
    p[0] = None
    #empty rule for the NP
def p_empty(p):
    'empty :'
    pass
#condition basci structure
def p_condicion(p):
    '''
    condicion : IF L_PARENTHESIS expresion R_PARENTHESIS rp_seen L_BRACKET cuerpo R_BRACKET condicion_aux else_after
    '''
    
    p[0] = None
#neuralgic point that save the expression and the positon of the GOTOF, also check if the expresion is bool
def p_rp_seen(p):
    '''
    rp_seen : empty
    '''
    
    result = Temporales[-1] #save teh temporal for the 
    
    if tipos.top() != 'bool':
        raise ErrorMsg('Se esperaba un tipo bool en el if')
    CrearCuadruplo('GOTOF',result,'_','_')#created the GOTOF
    Saltos.append(cont-1)

    p[0] = None
#fill the gotof with the end of the if body, so you can exit the if
def p_else_after(p):
    '''
    else_after : empty
    '''
    
    end = Saltos.pop()
    Fill(end,cont)
    

    p[0] = None
#else basic strcuture
def p_condicion_aux(p):
    '''
    condicion_aux : ELSE else_seen L_BRACKET cuerpo R_BRACKET
    |
    '''
    p[0] = None
#NP when you have a else
def p_else_seen(p):
    '''
    else_seen : empty
    '''
    CrearCuadruplo('GOTO','_','_','_')#created the jump so you can jump the if true part
    falseJ = Saltos.pop()#pop out the GOTOF location
    Saltos.append(cont-1)#append this new location
    Fill(falseJ,cont)#fill the gotof with the location after the GOTO 
    

    p[0] = None


#-------------- declaraciones---------------
#declaration basic structure
def p_declaracion_parametros(p):
    '''
    declaracion_parametros : startDParam declaracion_parametros_aux
	|
    '''
 
    p[0] = None
#NP that reset the parameter list
def p_startDParam(p):
    '''
    startDParam : empty
    '''
    global parametros
    parametros.clear()
    p[0]= None
#created the addres memory space for each parameter and append the parameter and his type to the paramater list
def p_declaracion_parametros_aux(p):
    '''
    declaracion_parametros_aux : tipo_retorno ID declaracion_parametros_aux2
    |
    '''
    if len(p ) > 1:
        tipo = AuxList[1]
        agregarContVarFunciones(tipo,'NORMAL')
        name = p[2]
        address = memoria.AssignMemoryAddress(tipo,Scope[0],'NORMAL')
        parametros[name] = { 'Type' :tipo,'Address':address}

    p[0] = None
#basic strucure to have multiple parameters
def p_declaracion_parametros_aux2(p):
    '''
    declaracion_parametros_aux2 : COMMA declaracion_parametros_aux
    |
    '''

    p[0] = None
#basic structure of a class
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

    p[0]= None
#save teh name of the class and check if there is another class with te same name
def p_guardar_nombre_clase(p):
    '''
    guardar_nombre_clase : ID
    '''
    global claseDeclarada
    claseDeclarada = p[1]
    global atributos
    atributos = 0
    
    if Tabla.CheckIfClassExists(claseDeclarada):
        raise ErrorMsg('La clase ' + claseDeclarada + ' ya habia sido declarada previamente')
    else:
        Tabla.AddClase(claseDeclarada) 
        Tabla.SetClass(claseDeclarada)

    p[0] = None
#set the basic structure and declaration of the class
def p_declaracion_clases_aux(p):
    '''
    declaracion_clases_aux :  L_BRACKET  declaracion_var declaracion_funciones R_BRACKET
    | herencia L_BRACKET  declaracion_var declaracion_funciones R_BRACKET
    '''

    p[0] = None
#Inheritance check if the class to inherance exsit, and save it in the class
def p_herencia(p):
    '''
    herencia : AGRANDA ID
    '''
    global atributos

    if claseDeclarada == p[2]:
        raise ErrorMsg('No puede haber herencia entre si mismo: ' + p[2])
    if Tabla.CheckIfClassExists(p[2]):
        Tabla.updateHerencia(claseDeclarada,p[2])
        size = Tabla.ClassAtribute(p[2],'Space')
        atributos = size
        
    else:
        raise ErrorMsg('La clase ' + p[2] + ' no existe')


    p[0] = None
#basic structure to declarated functions
def p_declaracion_funciones(p):
    '''
    declaracion_funciones :  declaracion_funciones_aux funciones_end  declaracion_funciones 
    |
    '''

    p[0] = None
#save the location has inside of a fucntion
def p_startF(p):
    '''
    startF : empty
    '''
    global Location
    Location = 'function'
    
#NP for the end of the function
def p_funciones_end(p):
    '''
    funciones_end : empty
    '''
    #Guarda contador de variables
    if Tabla.Scope == 'class':
        Tabla.updateClassAtribute(claseDeclarada,'Space',atributos)#update the space of the function to match the atributes in the class
    CrearCuadruplo('END PROC','_','_','_')#created the end procedure quadruple
    global Location
    Location = Tabla.Scope
    #save the scope table scope in location
    p[0]= None
#basic function structure
def p_declaracion_funciones_aux(p):
    '''
    declaracion_funciones_aux : startF MINI declaracion_funciones_aux2 guardar_nombre_funcion L_PARENTHESIS declaracion_parametros R_PARENTHESIS L_BRACKET cuerpo  R_BRACKET save_variables
    |
    '''
    global Location
    global LocationTemp
    LocationTemp = Location #save the location before entering the function
    
    Location = 'function' #put the location to funciton
    p[0] = None
def p_save_variables(p):
    '''
    save_variables : empty
    '''

    global FuncionDeclarada #see which function is and update the parameters with the parameters and the local address
    Tabla.updateFunctionAttribute(FuncionDeclarada,'Space',contVarLocal.copy())
    Tabla.updateFunctionAttribute(FuncionDeclarada,'Parametros',parametros.copy())
    p[0]= None
def p_guardar_nombre_funcion(p):
    '''
    guardar_nombre_funcion : ID
    '''
    #reset the local variables adn the temporals
    global contVarLocal
    resetConVarFunciones()
    memoria.ResetLocalMemory()
    
    global FuncionDeclarada
    FuncionDeclarada = p[1]
    #save the nameof the function
    CrearCuadruplo('START PROC','_','_',FuncionDeclarada)
    #created the quadruple of the function

   #see if there is a function of the same name
    if Tabla.CheckIfFunctionExists(FuncionDeclarada):
        raise ErrorMsg('La funcion ' + FuncionDeclarada + ' ya habia sido declarada previamente')
    else:
        #
        #if the scope is inside a class add the function to the class
        if Tabla.Scope == 'class':
            global atributos
            atributos = atributos + 1
            Tabla.AddFunction(FuncionDeclarada, AuxList[1], atributos,parametros,cont-1)
            Tabla.SetCurrentFunction(FuncionDeclarada)
        #else added it to the main function scope
        else:
            address = memoria.AssignMemoryAddress(AuxList[1], 'GLOBAL', 'NORMAL')
            Tabla.AddFunction(FuncionDeclarada, AuxList[1], address,parametros,cont-1)
            Tabla.SetCurrentFunction(FuncionDeclarada)

def p_declaracion_funciones_aux2(p):
    '''
    declaracion_funciones_aux2 : VOID
    | tipo_retorno
    '''
    #save the type of the funciton
    if p[1] == 'void' :
        AuxList[1] = p[1]
    p[0] = None
#return basic structure
def p_regreso(p):
    '''
    regreso : RETURN expresion
    |
    '''
    global FuncionDeclarada
    tipo = Tabla.GetFunctionAttribute(FuncionDeclarada, 'Type')#save the type of the function

    if len(p) > 1:
        if tipo == 'void': # if the class it is void, they cant have return
            raise ErrorMsg('Las funciones void (' + FuncionDeclarada + ') no deben tener un return')
        else:
            CrearCuadruplo('RETURN', '_', '_', values.pop()) #created the quadruple
    else:
        if tipo != 'void': #if the type is not void, they should always have a return
            raise ErrorMsg('Las funciones de tipo ' + tipo + '(' + FuncionDeclarada + ') deben tener un return')
        
    p[0] = None
#function declaration basic structure
def p_declaracion_var(p):
    '''
    declaracion_var : declaracion_var_aux
    '''
    #if the declaration is inside the class, match the space to the atributes and update it in the class
    if Tabla.Scope == 'class':
        Tabla.updateClassAtribute(claseDeclarada,'Space',atributos)
    p[0] = None
#var aux so you can ahve multiple declarations
def p_declaracion_var_aux(p):
    '''
    declaracion_var_aux : PETITE declaracion_var_aux2 assignAddress declaracion_var 
    |
    '''
    p[0] = None
#assing I address to the variable
def p_assignAddress(p):
    # Funcion que asigna los espacios de memoria faltantes en caso de ser un array o matriz
    '''
    assignAddress : empty
    '''
    global sizeVar
    
    # Se ignora el primer espacio ya que fue asignado al momento de guardar la variable por primera vez
    if Tabla.Scope != 'class':
        for i in range(1, sizeVar):
            agregarContVarFunciones(AuxList[1],'NORMAL')
            address = memoria.AssignMemoryAddress(AuxList[1], Scope[0], 'NORMAL')
        
    p[0] = None
#multiple posible variable strcuture declaration
def p_declaracion_var_aux2(p):
    '''
    declaracion_var_aux2 : tipo_retorno idChecker declaracion_var_aux3
    | tipo_retorno idChecker declaracion_var_aux5
    | tipo_especial idChecker
    '''
    p[0] = None
#check the id of the variable
def p_idChecker(p):
    '''
    idChecker : ID
    '''
    global DeclVar
    global sizeVar
    global atributos

    sizeVar = 1
    #check if the id exist in teh main scope
    if Tabla.CheckIfVariableExists(p[1],Location):
        raise ErrorMsg('La variable ' + p[1] + ' ya habia sido declarada previamente')
    else:
        #check if the varible it is inside a class
        if Tabla.Scope == 'class':
            #see if the variable is a list_type
            if(AuxList[1] == 'list_int' or AuxList[1] == 'list_bool' or AuxList[1] == 'list_float'):
                DeclVar = p[1]
                #save the variable of the list and added it to the directory
                address = memoria.AssignMemoryAddress(AuxList[1], Scope[0], 'NORMAL')
                agregarContVarFunciones(AuxList[1],'NORMAL',sizeVar)
                Tabla.AddVariable(DeclVar, AuxList[1], address, sizeVar,Location)

            
            else:#if it is not a list save it as a sum of the atribute + 1 in the class address memory
                #this way they can be access has object dir . var dir Object.var or atribute
                DeclVar = p[1]
                atributos = atributos + 1
                address = atributos
                Tabla.AddVariable(DeclVar, AuxList[1], address, sizeVar,Location)
        else:
            #if the variable is not in class scope save it as a non temporal memory
            DeclVar = p[1]
            address = memoria.AssignMemoryAddress(AuxList[1], Scope[0], 'NORMAL')
            agregarContVarFunciones(AuxList[1],'NORMAL',sizeVar)
            Tabla.AddVariable(DeclVar, AuxList[1], address, sizeVar,Location)    
    p[0] = None
#basic structure to have multiple declarations
def p_declaracion_var_aux3(p):
    '''
    declaracion_var_aux3 : COMMA idChecker declaracion_var_aux3
    |
    '''
    p[0] = None
#basic array declaration structure
def p_declaracion_var_aux5(p):
    '''
    declaracion_var_aux5 : L_CORCHETE save_size R_CORCHETE declaracion_var_aux7
    |
    '''
   #you cant have arrays in a object
    if Tabla.Scope == 'class' and Location == 'class':
        raise ErrorMsg('no se pueden declarar arreglos como atributos de objetos')
    p[0] = None

def p_save_size(p):
    '''
    save_size : CTEI
    '''
    #make the user to just have positive integers has array and update hte size of teh variable
    if p[1] > 0:
        global sizeVar
        sizeVar *= p[1]
        Tabla.UpdateSize(DeclVar,sizeVar,Location)
        Tabla.UpdateArrayLimit(DeclVar, p[1] - 1,Location)
    else: 
        raise ErrorMsg('No se puede declarar el tamaño de un array como menor que 1')
    
    p[0] = None
#matrix basic structure declaration
def p_declaracion_var_aux7(p):
    '''
    declaracion_var_aux7 : L_CORCHETE last_size R_CORCHETE
    |
    '''
    p[0] = None
#see if the int inside the array is not negative
def p_last_size(p):
    '''
    last_size : CTEI
    '''
    if p[1] > 0:
        global sizeVar
        
        tipo = Tabla.GetAttribute(DeclVar,'Type',Location)
        currentSize = sizeVar
        sizeVar *= p[1] #multiple the size fo the array to match the real space
        Tabla.UpdateSize(DeclVar, sizeVar,Location) #update the size
    else: 
        raise ErrorMsg('No se puede declarar el tamaño de una matriz como menor que 1')

    p[0] = None
#basic object declarations
def p_instancear_objetos(p):
    '''
    instancear_objetos :  ID EQUALS NEW ID

    '''
    #you cant have object inside a class
    if Tabla.Scope == 'class':
        raise ErrorMsg('No se puede declarar objetos dentro de funciones en clases')
    #you cant have a object with the same name has a the class
    if p[1] == p[4]:
        raise ErrorMsg('El objeto no puede tener el mismo nombre que una clase')

    clase = p[4]
    objeto = p[1]
    #check if the class exist
    if not Tabla.CheckIfClassExists(clase):
        raise ErrorMsg('La clase ' + clase + ' no existe')
    else:
        #check if there is another object with the same name
        if Tabla.CheckIfObjectExists(objeto):
            raise ErrorMsg('El Objeto ' + objeto + ' ya existe')
        else:
            #assign memory and add it to teh directory of objects
            address = memoria.AssignMemoryAddressObject()
            size = Tabla.ClassAtribute(clase,'Space')
            Tabla.AddObject(objeto,clase,size,address)
    p[0] = None
#-------------- Variables---------------
#basic a variable call structure
def p_variable(p):
    '''
    variable : variable_aux2 variable_aux
    '''
    p[0] = None
#NP to call a variable
def p_variable_aux2(p):
    '''
    variable_aux2 : ID empty
    '''
    #check if the variable exist in the main scope and push the address to the value stack
    if  Tabla.CheckIfVariableExists(p[1],Location):
        address = Tabla.GetAttribute(p[1],'Address',Location)
        values.push(address)
        tipos.push(Tabla.GetAttribute(p[1], 'Type',Location))
    else:
        #check if the variable is a parameters of a function or a atribute of a class and push the address to the value stack
        if Tabla.CheckIfFunctExistInAtribute(p[1],Location):
            address = Tabla.GetAttributeForParameters(p[1],'Address',Location)
            values.push(address)
            tipos.push(Tabla.GetAttributeForParameters(p[1], 'Type',Location))
        #see if the atribute is not inside the father atributes and push the address to the value stack
        elif not Tabla.CheckIfAtributeExistsInFather(p[1],Location):
            clasePadre = Tabla.GetClassAtribute(Tabla.CurrentClass,'Padre')
            tempClass = Tabla.CurrentClass
            Tabla.SetClass(clasePadre)
            address = Tabla.GetAttributeFromFather(p[1],'Address',Location)
            values.push(address)
            tipos.push(Tabla.GetAttributeFromFather(p[1], 'Type',Location))
            Tabla.SetClass(tempClass)
        else :
            raise ErrorMsg('No existe la variable ' + p[1])
    p[0] = None
def p_variable_aux(p):
    '''
    variable_aux : PERIOD ID
    |
    '''
    p[0] = None
#-------------- Tipos---------------
#types of the list or special types, push the type to the type stack
def p_tipo_especial(p):
    '''
    tipo_especial : LIST INT
    | LIST FLOAT
    | LIST BOOL
    '''
    if(p[2] == 'int'):
        AuxList[1] = 'list_int'
    elif(p[2] == 'float'):
        AuxList[1] = 'list_float'
    else:
        AuxList[1] = 'list_bool'

    p[0] = None
#return types,push the type to the type stack
def p_tipo_retorno(p):
    '''
    tipo_retorno : INT
    | FLOAT
    | BOOL
    '''
    AuxList[1] = p[1]
    p[0] = None



#-------------- arreglo---------------
#array basic call
def p_arreglo(p):
    '''
    arreglo : startArray L_CORCHETE expresion R_CORCHETE checkLimits arreglo2
    '''

    
    #save the base adress
    dirBase = Tabla.GetAttribute( lastVar, 'Address', Location)
    popper.push('+')
    
    address = Constantes.GetMemoryAddress(dirBase,'int')
    values.push(address)
    tipos.push('int')
    #add the base adress to the limit
    GenerarCuadruploDeOperador(popper,values,tipos)
    fix = values.pop()
    #see if the variable exist
    if  Tabla.CheckIfVariableExists(lastVar,Location):
        tipos.push(Tabla.GetAttribute(lastVar, 'Type',Location))
    else:
       raise ErrorMsg ('No existe la variable: ' + lastVar)
    values.push('('+str(fix)+')')

    
    p[0] = None
def p_startArray(p):
    '''
    startArray : ID
    '''
    global lastVar
    lastVar = p[1]
    #fake symbol in popper, to separete the arrays operation from the expresions or actual program
    popper.push('(')
    p[0]= None
#created the quadruples to check the limits and get teh address
def p_checkLimits(p):
    '''
    checkLimits : empty
    '''
    limit = Tabla.GetAttribute( lastVar,'Limit', Location)
    size =  Tabla.GetAttribute( lastVar,'Size', Location)
    tipo = Tabla.GetAttribute( lastVar,'Type', Location)
    #created the limit check quadruple
    CrearCuadruplo('VER',values.top(),0,limit)
    popper.push('*')
    row = int(math.ceil(size/(limit+1)))
    address = Constantes.GetMemoryAddress(row,'int')
    values.push(address)
    tipos.push('int')
    tipos.push('int')
    #multiple the address with the size / limit and pushes the answer to the values stack
    GenerarCuadruploDeOperador(popper,values,tipos)
    p[0] = None
def p_arreglo2(p):
    '''
    arreglo2 : L_CORCHETE expresion p_checkLimits2 R_CORCHETE
    |
    '''
    #takes the fake symbol out of the popper stack
    if(popper.top() == '('):
        popper.pop()
    p[0] = None
#operaions to get the address
def p_checkLimits2(p):
    '''
    p_checkLimits2 : empty
    '''
    
    arrSize = Tabla.GetAttribute(lastVar,'Size', Location)
    limit = Tabla.GetAttribute(lastVar,'Limit', Location)
    columnSize = int(arrSize / (limit + 1))
    #created the quadrupl to check the limits
    CrearCuadruplo('VER',values.top(),0, columnSize - 1)
    popper.push('+') 
    #sum the limit with the dirbase
    GenerarCuadruploDeOperador(popper,values,tipos)
    #sum the val of the past address and this one
    popper.push('+')
    address = Constantes.GetMemoryAddress(1,'int')
    #sum 1
    values.push(address)
    tipos.push('int')
    tipos.push('int')
    #generated the operation
    GenerarCuadruploDeOperador(popper,values,tipos)


    p[0]= None

#-------------- expresiones---------------

#expresion structure
def p_expresion(p):
    '''
    expresion : t_exp expresion_aux2
    | t_exp expresion_aux2 expresion_aux expresion
    '''
    p[0] = None
#push the or to the popper
def p_expresion_aux(p):
    '''
    expresion_aux : OR
    '''
    if (len(p) > 1):
        popper.push(p[1])
    p[0] = None
#generated the quadruple of the operation
def p_expresion_aux2(p):
    '''
    expresion_aux2 : empty
    '''
    if popper.top() == '||':
        GenerarCuadruploDeOperador(popper, values, tipos)
    p[0] = None
#texp basic structure
def p_t_exp(p):
    '''
    t_exp : g_exp t_exp_aux2
    | g_exp t_exp_aux2 t_exp_aux t_exp
    '''
    p[0] = None
#if the expression has an and push it to the popper
def p_t_exp_aux(p):
    '''
    t_exp_aux : AND
    '''
    if (len(p) > 1):
        popper.push(p[1])
    p[0] = None
#created the cuadruple of the expression
def p_t_exp_aux2(p):
    '''
    t_exp_aux2 : empty
    '''
    if popper.top() == '&&':
        GenerarCuadruploDeOperador(popper, values, tipos)
    p[0] = None
#basic sctructure of comparison symbols
def p_g_exp(p):
    '''
    g_exp : m_exp g_exp_aux2
    | m_exp g_exp_aux2 g_exp_aux g_exp
    '''
    p[0] = None
#push the symbol to the popper
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
#created the quadruple
def p_g_exp_aux2(p):
    '''
    g_exp_aux2 : empty
    '''
    operadores = ['>', '<', '>=', '<=', '==', '<>']
    if popper.top() in operadores:
        GenerarCuadruploDeOperador(popper, values, tipos)
    p[0] = None
#term basic expression
def p_m_exp(p):
    '''
    m_exp : termino m_exp_aux2
    | termino m_exp_aux2 m_exp_aux m_exp
    '''
    p[0] = None
#if the operation has a + or - add it to the popper
def p_m_exp_aux(p):
    '''
    m_exp_aux : PLUS
    | MINUS
    '''
    if (len(p) > 1):
        popper.push(p[1])
    p[0] = None
#created the quadruple
def p_m_exp_aux2(p):
    '''
    m_exp_aux2 : empty
    '''
    if popper.top() == '+' or popper.top() == '-':
        GenerarCuadruploDeOperador(popper, values, tipos)
    p[0] = None
#term basic structure
def p_termino(p):
    '''
    termino : factor termino_aux2 termino_aux termino
    | factor termino_aux2
    '''
    p[0] = None
#if the expression has a  * or / add it to the popper
def p_termino_aux(p):
    '''
    termino_aux : TIMES
    | DIVIDE
    '''
    if (len(p) > 1):
        popper.push(p[1])
    p[0] = None
#generated the quadruple
def p_termino_aux2(p):
    '''
    termino_aux2 : empty
    '''
    if popper.top() == '*' or popper.top() == '/':
        GenerarCuadruploDeOperador(popper, values, tipos)
    p[0] = None
#factor basic possible values
def p_factor(p):
    '''
    factor : L_PARENTHESIS factor_aux expresion R_PARENTHESIS factor_aux2
    | variable
    | llamada
    | arreglo
    | CTEI
    | CTEF
    | CTES
    | TRUE
    | FALSE
    '''
    #push the address of the expression if there is not a fake symbol
    if p[1] != '(':
        if isinstance(p[1],int):
            tipos.push('int')
            address = Constantes.GetMemoryAddress(int(p[1]), 'int')
            values.push(address)
        elif isinstance(p[1],float):
            tipos.push('float')
            address = Constantes.GetMemoryAddress(float(p[1]), 'float')
            values.push(address)
        elif isinstance(p[1],str):
            tipos.push('string')
            string = p[1][1:-1]
            address = Constantes.GetMemoryAddress(str(string), 'string')
            values.push(address)
    p[0] = None
#NP to elimated the fake symbol
def p_factor_aux(p):
    '''
    factor_aux : empty
    '''
    popper.push('(')
    p[0] = None
#NP to take out the popper
def p_factor_aux2(p):
    '''
    factor_aux2 : empty
    '''
    popper.pop()
    p[0] = None

#-------------- error---------------
#ERROR MESSAGE CLASS
class ErrorMsg(Exception):
    def __init__(self, message):
        self.message = message
#structure to return the error token, value and line
def p_error(p):
   if p:
      print("Syntax error at token", p.type)
      print("Syntax error at '%s'" % p.value)
      print("line : '%s'" % p.lineno)
      print("column: '%s'" % p.lexpos)
   else:
      print("Syntax error at EOF")
#--------------------------------------- Error---------------------------------------
#rule to print
def imprimirP(p):
    for i in range(len(p)):
        if (i != 0):
            print(p[i], end=" ")
    print()
#function to generate quadruples that pop out the values adn type and generated the quadruple and temporals
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

#created a quadaruple adn add it 1 to the cont of the quadruple
def CrearCuadruplo(op, iz, der, res):
    global cont
    cont += 1
    Cuartetos.append({'op': Operadores.GetNumber(op), 'iz': iz, 'de': der, 'res':res})
#generated a new temporal and assign a memory address to it
def GenerarNuevoTemporal(tipo):
    agregarContVarFunciones(tipo,'TEMPORAL')
    addressTemporal = memoria.AssignMemoryAddress(tipo,Scope[0],'TEMPORAL')
    Temporales.append(addressTemporal)
    tipos.push(tipo)
    return addressTemporal
#fill update a quadruple res part
def Fill(cuarteto, llenado):
    global Cuartetos
    Cuartetos[cuarteto]['res'] = llenado
#function to add 1 to the counter of a address
def agregarContVarFunciones(type,location,size=1):
    global contVarLocal
    if location == 'NORMAL':
        if(type == 'int'):
            contVarLocal[0]  = contVarLocal[0] + size
        elif(type == 'float'):
            contVarLocal[1]  = contVarLocal[1] + size
        elif(type == 'bool'):
            contVarLocal[2]  = contVarLocal[2] + size
        elif(type == 'list_int'):
            contVarLocal[3]  = contVarLocal[3] + size
        elif(type == 'list_float'):
            contVarLocal[4]  = contVarLocal[4] + size
        elif(type == 'list_bool'):
            contVarLocal[5]  = contVarLocal[5] + size
    else:
        if(type == 'int'):
            contVarLocal[6]  = contVarLocal[6] + size 
        elif(type == 'float'):
            contVarLocal[7]  = contVarLocal[7] + size 
        elif(type == 'bool'):
             contVarLocal[8]  = contVarLocal[8] + size
        
#function to reset the temporal
def resetConVarFunciones():
    global contVarLocal
    global Temporales
    contVarLocal.clear()
    contVarLocal = [0]*9


# crear el parser
parser = yacc.yacc()