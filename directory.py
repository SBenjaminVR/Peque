class Directory():
    def __init__(self, clases, funciones, variables):
        self.Clases = clases
        self.Funciones = funciones
        self.Variables = variables
        self.Scope = ''
        self.CurrentFunction = ''
        self.CurrentClass = ''

    def SetScope(self, scope):
        self.Scope = scope
    
    def SetCurrentFunction(self, function):
        self.CurrentFunction = function

    def SetClass(self, clase):
        self.CurrentClass = clase

    def CheckIfVariableExists(self, name):
        if self.Scope == 'main':
            return self.Variables.get(name) != None
        elif self.Scope == 'function':
            current = self.Funciones.get(self.CurrentFunction)
        elif self.Scope == 'class':
            classObj = self.Clases.get(self.CurrentClass)
            current = classObj.get('Funciones').get(self.CurrentFunction)

        return current.get('Variables').get(name) != None

    def CheckIfFunctionExists(self, funcion):     
        if self.Scope == 'class':
            current = self.Clases.get(self.CurrentClass).get('Funciones')
            return current.get('Funciones').get(funcion) != None
        else:
            return self.Funciones.get(funcion)

    def CheckIfClassExists(self, clase):
        return self.Clases.get(self.CurrentClass) != None
    
    def GetAttribute(self, name, val):
        if self.Scope == 'main':
            return self.Variables.get(name).get(val)
        elif self.Scope == 'function':
            current = self.Funciones.get(self.CurrentFunction)
        elif self.Scope == 'class':
            classObj = self.Clases.get(self.CurrentClass)
            current = classObj.get('Funciones').get(self.CurrentFunction)
        return current.get('Variables').get(name).get(val)

    def GetFunctionAttribute(self, name, val):
        if self.Scope == 'class':
            classObj = self.Clases.get(self.CurrentClass)
            current = classObj.get('Funciones').get(name)
        else:
            current = self.Funciones.get(name)
            
        return current.get(val)

    def AddVariable(self, name, type, address, size):
        newVar = {
            'Type': type,
            'Address': address,
            'Size': size
        }
        if self.Scope == 'main':
            self.Variables[name] = newVar
        elif self.Scope == 'function':
            self.Funciones[self.CurrentFunction]['Variables'][name] = newVar
        elif self.Scope == 'class':
            self.Clases[self.CurrentClass]['Funciones'][self.CurrentFunction]['Variables'][name] = newVar

    def AddFunction(self, name, type, address):
        newFunction = {
            'Type': type,
            'Address': address,
            'Space': 0,
            'Variables': {},
            'Parametros': {}
        }
        if self.Scope == 'function':
            self.Funciones[name] = newFunction
        else:
            self.Clases[self.CurrentClass]['Funciones'][name] = newFunction

    def AddClase(self, name,padre = None):
        newClase = {
            'Space': 0,
            'Variables': {},
            'Funciones' : {},
            'Padre' : padre
        }
        self.Clases[name] = newClase

    def UpdateArrayLimit(self, name, limit):
        newLimit = {'Limit': limit}
        if self.Scope == 'main':
            self.Variables[name].update(newLimit)
        elif self.Scope == 'function':
            self.Funciones[self.CurrentFunction]['Variables'][name].update(newLimit)
        elif self.Scope == 'class':
            self.Clases[self.CurrentClass]['Funciones'][self.CurrentFunction]['Variables'][name].update(newLimit)
    def UpdateSize(self, name, size):
        newSize = {'Size': size}
        if self.Scope == 'main':
            self.Variables[name].update(newSize)
        elif self.Scope == 'function':
            self.Funciones[self.CurrentFunction]['Variables'][name].update(newSize)
        elif self.Scope == 'class':
            self.Clases[self.CurrentClass]['Funciones'][self.CurrentFunction]['Variables'][name].update(newSize)

    def updateFunctionAttribute(self,name,nameOfChange,change):
        newVal = {nameOfChange: change}
        if self.Scope == 'class':
            self.Clases[self.CurrentClass]['Funciones'][name].update(newVal)
        else:
            self.Funciones[name].update(newVal)
