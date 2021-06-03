class Directory():
    
    def __init__(self, clases, funciones, variables,Objetos):
        self.Clases = clases #Directory of clases
        self.Funciones = funciones #Directory of variables
        self.Variables = variables #directory of the variables
        self.Scope = '' #Direcotry of the scope
        self.CurrentFunction = '' #Curent functions
        self.CurrentClass = '' #Curretn class
        self.Objetos = Objetos # Directory of objects
        self.currentObject = '' #Current Object

    #Set a new scope
    def SetScope(self, scope):
        self.Scope = scope
    #function to select a new current function
    def SetCurrentFunction(self, function):
        self.CurrentFunction = function
    #function to replace the current class
    def SetClass(self, clase):
        self.CurrentClass = clase
    #function that check if a variable inside a function
    #is in his parameter or if it is a class search for them in the variables
    def CheckIfFunctExistInAtribute(self,name,location):
        if self.Scope == 'class':
            current = self.Clases.get(self.CurrentClass).get('Funciones').get(self.CurrentFunction)
            parametros = current.get('Parametros').get(name) != None
            atributos = self.Clases.get(self.CurrentClass).get('Variables').get(name) != None
            return parametros or atributos
        elif self.Scope == 'function':

            current = self.Funciones.get(self.CurrentFunction)
            
            parametros = current.get('Parametros').get(name) != None
            return parametros
           


        
    def CheckIfVariableExists(self, name,location):
        #check if a varibale exist in any scope
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
        
    #check if a function exist
    def CheckIfFunctionExists(self, funcion):     
        if self.Scope == 'class':
            current = self.Clases.get(self.CurrentClass)
            return current.get('Funciones').get(funcion) != None
        else:
            return self.Funciones.get(funcion)
    #check if a class exist
    def CheckIfClassExists(self, clase):
        return self.Clases.get(clase) != None
    #check if a object exist
    def CheckIfObjectExists(self, object):
        return self.Objetos.get(object) != None
 
    #check if a atribute exist in father atributes
    def CheckIfAtributeExistsInFather(self, name,location):
        clasePadre = self.Clases[self.CurrentClass].get('Father')
        if clasePadre == None:
            return False
        else:
            find = self.Clases[clasePadre].get('Variable')
            return find.get(name) != None
            


    #check if a atribute exist in the current scope
    def CheckIAributeExists(self, name,location):
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
   #get a variable value from the current scope you are in
    def GetAttribute(self, name, val, Location):
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
    #get an attribute from a father
    def GetAttributeFromFather(self, name, val, Location):
        if self.Scope == 'class':
                classObj = self.Clases.get(self.CurrentClass)
                current = classObj
        return current.get('Variables').get(name).get(val)
    #get any atribute from the variables in any scope
    def GetAttributeForParameters(self, name, val, Location):
        if self.Scope == 'function':
            current = self.Funciones.get(self.CurrentFunction)
            return current.get('Parametros').get(name).get(val)
        elif self.Scope == 'class':
            current = self.Clases.get(self.CurrentClass).get('Funciones').get(self.CurrentFunction)
            state = current.get('Parametros').get(name) != None
            if state :
                current = current.get('Parametros').get(name).get(val)
                return current
            else:
                return  self.Clases.get(self.CurrentClass).get('Variables').get(name).get(val)

    
    #get any object atribute
    def GetObjectAtr(self, name,val):  
        return self.Objetos.get(name).get(val)
    #get any function attribute
    def GetFunctionAttribute(self, name, val):
        if self.Scope == 'class':
            classObj = self.Clases.get(self.CurrentClass)
            current = classObj.get('Funciones').get(name)
        else:
            current = self.Funciones.get(name)
  
        return current.get(val)
#adds---------------------------------------------------------------
    #add a variable to the variable directory if it is in the main scope, or to a function if it is in a function scope
    #or in a class if it is in a class scope
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

    #add the function to the function directory if it is in the function directory or to a class if it is in class scope
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
    #add a class tot he class directory
    def AddClase(self, name,padre = None):
        newClase = {
            'Space': 0,
            'Padre' : padre,
            'Variables': {},
            'Funciones' : {}
            
        }
        self.Clases[name] = newClase
    #add a object to the object directory
    def AddObject(self, name,clase,space,address):
        newObj = {
            'Clase' : clase,
            'Space' : space,
            'Address' : address

            
        }
        self.Objetos[name] = newObj


#updates------------------------------
#update the array limit of a varible which it is a array
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
#update the size of a varible in any scope
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
#update any value of the function in any scope
    def updateFunctionAttribute(self,name,nameOfChange,change):
        newVal = {nameOfChange: change}
        if self.Scope == 'class':
            self.Clases[self.CurrentClass]['Funciones'][name].update(newVal)
        else:
            self.Funciones[name].update(newVal)
        #update the father of a class    
    def updateHerencia(self,clase,padre):
        referencia = {'Padre' : padre}
        self.Clases.get(clase).update(referencia)
    #update any atribute of a class
    def updateClassAtribute(self,clase,name,val):
        referencia = {name : val}
        self.Clases[clase].update(referencia)
    #update a class atribute
    def ClassAtribute(self,clase,name):
        return self.Clases[clase].get(name)
    #get the object address
    def GetObjectAddress(self, function, objeto):
        if objeto != '_':
            return self.GetAttributeOfFunctionInObject(function, objeto, 'Address')
        else:
            return self.Funciones[function].get('Address')
    #get the function address
    def GetFunctionAddress(self, name):
        return self.Funciones.get(name).get('Address')
    #get the function space value
    def GetFunctionSpace(self, function, objeto):
        if objeto != '_':
            return self.GetAttributeOfFunctionInObject(function, objeto, 'Space')
        else:
            return self.Funciones[function].get('Space')
    #get the atribute of a function in a object
    def GetAttributeOfFunctionInObject(self, function, objeto, attribute):
        currentClass = self.Objetos.get(objeto).get('Clase')
        foundFunction = False
        while not foundFunction:
            if self.Clases[currentClass]['Funciones'].get(function) != None:
                foundFunction = True
            else:
                currentClass = self.Clases[currentClass].get('Padre')
        return self.Clases[currentClass]['Funciones'][function].get(attribute)
    #get the function address
    def GetFunctionAddress(self, name):
        return self.Funciones.get(name).get('Address')
    #get the class atribute
    def GetClassAtribute(self, name,atr):
        return self.Clases.get(name).get(atr)
