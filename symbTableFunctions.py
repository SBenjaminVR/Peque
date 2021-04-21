
Directory = {
    'Clases': {},
    'Funciones': {},
    'Variables': {}
}
Glovalvar = {}

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