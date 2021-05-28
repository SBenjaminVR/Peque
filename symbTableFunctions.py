
Directory = {
    'Clases': {},
    'Funciones': {},
    'Variables': {}
}
Glovalvar = {}

def addVariable(name, type, memoria,size):
    if Directory.get('Variables').get(name) == None:
        Directory['Variables'][name] = {
            'Id': name, 
            'DataType': type,
            'EspacioMemoria': memoria,
            'Size' : size
        }
def addLimiteSuperior(name,LS,option):
    if option == 1:
        if Directory.get('Variables').get(name) != None:
            Directory['Variables'][name].update({'LS1': LS})
    else :
        if Directory.get('Variables').get(name) != None:
            Directory['Variables'][name].update({'LS2': LS})

        
def addSizeArray(name,size):
    Directory['Variables'][name].update({'Size': size})
    

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
    if Directory.get(name) != None:
        directoryScope = Directory.get(name)
        if directoryScope[2].get(var) == None:
            directoryScope[2][var] = []

def CheckIfVariableExists(scope, clase, funcion, name):
    if scope == 'main':
        if Directory.get('Variables').get(name) != None:
            return True
    elif scope == 'function':
        functionObj = Directory.get('Funciones').get(funcion)
        if functionObj.get('Variables').get(name) != None:
            return True
    elif scope == 'class':
        classObj = Directory.get('Clases').get(clase)
        functionObj = classObj.get('Funciones').get(funcion)
        if functionObj.get('Variables').get(name) != None:
            return True
    return False

def CheckIfFunctionExists(scope, clase, funcion):     
    if scope == 'class':
        classObj = Directory.get('Clases').get(clase)
        if classObj.get('Funciones').get(funcion) != None:
            return True
    else:
        if Directory.get('Funciones').get(funcion) != None:
            return True
    return False

def CheckIfClassExists(clase):
    if Directory.get('Clases').get(clase) != None:
            return True
    return False
    
def GetType(scope, clase, funcion, name):
    if scope == 'main':
        return Directory.get('Variables').get(name).get('DataType')
    elif scope == 'function':
        functionObj = Directory.get('Funciones').get(funcion)
        return functionObj.get('Variables').get(name).get('DataType')
    elif scope == 'class':
        classObj = Directory.get('Clases').get(clase)
        functionObj = classObj.get('Funciones').get(funcion)
        return functionObj.get('Variables').get(name).get('DataType')
def GetSize(scope, clase, funcion, name):
    if scope == 'main':
        return Directory.get('Variables').get(name).get('Size')
    elif scope == 'function':
        functionObj = Directory.get('Funciones').get(funcion)
        return functionObj.get('Variables').get(name).get('Size')
    elif scope == 'class':
        classObj = Directory.get('Clases').get(clase)
        functionObj = classObj.get('Funciones').get(funcion)
        return functionObj.get('Variables').get(name).get('Size')

def GetLS(scope, clase, funcion, name,option):
    if scope == 'main':
        if option == 1 :
            return Directory.get('Variables').get(name).get('LS1')
        else :
            return Directory.get('Variables').get(name).get('LS2')
    elif scope == 'function':
        functionObj = Directory.get('Funciones').get(funcion)
        if option == 1 :
            return functionObj.get('Variables').get(name).get('LS1')
        else :
            return functionObj.get('Variables').get(name).get('LS2')
    elif scope == 'class':
        classObj = Directory.get('Clases').get(clase)
        functionObj = classObj.get('Funciones').get(funcion)
        if option == 1 :
            return functionObj.get('Variables').get(name).get('LS1')
        else :
            return functionObj.get('Variables').get(name).get('LS2')
        
           