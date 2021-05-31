class Directory():
    def __init__(self, clases, funciones, variables,Objetos):
        self.Clases = clases
        self.Funciones = funciones
        self.Variables = variables
        self.Scope = ''
        self.CurrentFunction = ''
        self.CurrentClass = ''
        self.Objetos = Objetos
        self.currentObject = ''

    def SetScope(self, scope):
        self.Scope = scope
    
    def SetCurrentFunction(self, function):
        self.CurrentFunction = function

    def SetClass(self, clase):
        self.CurrentClass = clase
    
    def CheckIfVariableExists(self, name,location):
        
        if self.Scope == 'main':
            return self.Variables.get(name) != None
        elif self.Scope == 'function':
            current = self.Funciones.get(self.CurrentFunction)
            return current.get('Variables').get(name) != None
        elif self.Scope == 'class':
            if location == 'function':
                classObj = self.Clases.get(self.CurrentClass)
                current = classObj.get('Funciones').get(self.CurrentFunction)
                return current.get('Variables').get(name) != None
            elif location == 'class':
                current = self.Clases.get(self.CurrentClass)
                return current.get('Variables').get(name) != None
        

    def CheckIfFunctionExists(self, funcion):     
        if self.Scope == 'class':
            current = self.Clases.get(self.CurrentClass)
            return current.get('Funciones').get(funcion) != None
        else:
            return self.Funciones.get(funcion)

    def CheckIfClassExists(self, clase):
        return self.Clases.get(clase) != None

    def CheckIfObjectExists(self, object):
        return self.Objetos.get(object) != None
 

    def GetAttribute(self, name, val,Location):
        if self.Scope == 'main':
            return self.Variables.get(name).get(val)
        elif self.Scope == 'function':
            
            current = self.Funciones.get(self.CurrentFunction)
        elif self.Scope == 'class':
            if Location == 'function' :
                classObj = self.Clases.get(self.CurrentClass)
                current = classObj.get('Funciones').get(self.CurrentFunction)
            else:
                classObj = self.Clases.get(self.CurrentClass)
                current = classObj
        return current.get('Variables').get(name).get(val)
    
    

    def GetObjectAtr(self, name,val):  
        return self.Objetos.get(name).get(val)
        
    def GetFunctionAttribute(self, name, val):
        if self.Scope == 'class':
            classObj = self.Clases.get(self.CurrentClass)
            current = classObj.get('Funciones').get(name)
        else:
            current = self.Funciones.get(name)
            
        return current.get(val)
#adds---------------------------------------------------------------
    def AddVariable(self, name, type, address, size, Location):
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
            if Location == 'function':
                self.Clases[self.CurrentClass]['Funciones'][self.CurrentFunction]['Variables'][name] = newVar
            elif Location == 'class':
                self.Clases[self.CurrentClass]['Variables'][name] = newVar


    def AddFunction(self, name, type, address,param,start):
        newFunction = {
            'Type': type,
            'Address': address,
            'Start' : start,
            'Space': 0,
            'Variables': {},
            'Parametros': param
        }
        if self.Scope == 'function':
            self.Funciones[name] = newFunction
        else:
            self.Clases[self.CurrentClass]['Funciones'][name] = newFunction

    def AddClase(self, name,padre = None):
        newClase = {
            'Space': 0,
            'Padre' : padre,
            'Variables': {},
            'Funciones' : {}
            
        }
        self.Clases[name] = newClase
    def AddObject(self, name,clase,space,address):
        newObj = {
            'Clase' : clase,
            'Space' : space,
            'Address' : address

            
        }
        self.Objetos[name] = newObj


#updates------------------------------
    def UpdateArrayLimit(self, name, limit,Location):
        newLimit = {'Limit': limit}
        if self.Scope == 'main':
            self.Variables[name].update(newLimit)
        elif self.Scope == 'function':
            self.Funciones[self.CurrentFunction]['Variables'][name].update(newLimit)
        elif self.Scope == 'class':
            if Location == 'function' :
                self.Clases[self.CurrentClass]['Funciones'][self.CurrentFunction]['Variables'][name].update(newLimit)
            else :
                self.Clases[self.CurrentClass]['Variables'][name].update(newLimit)

    def UpdateSize(self, name, size,Location):
        newSize = {'Size': size}
        if self.Scope == 'main':
            self.Variables[name].update(newSize)
        elif self.Scope == 'function':
            self.Funciones[self.CurrentFunction]['Variables'][name].update(newSize)
        elif self.Scope == 'class':
            if Location == 'function':
                self.Clases[self.CurrentClass]['Funciones'][self.CurrentFunction]['Variables'][name].update(newSize)
            else:
                self.Clases[self.CurrentClass]['Variables'][name].update(newSize)

    def updateFunctionAttribute(self,name,nameOfChange,change):
        newVal = {nameOfChange: change}
        if self.Scope == 'class':
            self.Clases[self.CurrentClass]['Funciones'][name].update(newVal)
        else:
            self.Funciones[name].update(newVal)
    def updateHerencia(self,clase,padre):
        referencia = {'Padre' : padre}
        self.Clases.get(clase).update(referencia)

    def updateClassAtribute(self,clase,name,val):
        referencia = {name : val}
        self.Clases[clase].update(referencia)

    def ClassAtribute(self,clase,name):
        return self.Clases[clase].get(name)
