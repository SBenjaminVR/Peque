from localMemory import LocalMemory
from stack import Stack
from direcciones import DireccionesMemoria

Dir = DireccionesMemoria()

def IsInLocalRange(address):
    return address >= Dir.INT_LOCAL and address <= Dir.BOOL_LOCAL_TEMPORAL
        
def GetTypeOfValueGivenTheAddress(address):
    if address < Dir.INT_GLOBAL_TEMPORAL:
        return GetTypeGivenTheBase(address, 0)
    elif address < Dir.INT_LOCAL:
        return GetTypeGivenTheBase(address, 4000)
    elif address < Dir.INT_LOCAL_TEMPORAL:
        return GetTypeGivenTheBase(address, 8000)
    elif address < Dir.INT_CONSTANTE:
        return GetTypeGivenTheBase(address, 12000)

def GetTypeOfConstantGivenTheAddress(address):
    if address < Dir.FLOAT_CONSTANTE:
        return 'int'
    elif address < Dir.BOOL_CONSTANTE:
        return 'float'
    elif address < Dir.STRING_CONSTANTE:
        return 'bool'
    elif address < Dir.OBJETOS:
        return 'string'

class Memory:
    def __init__(self, data):
        self.memory = [None]*35000
        self.memoryStack = Stack()
        self.quadruples = data.get('Cuadruplos')
        self.directory = data.get('Directorio')

        self.AssignConstants(data.get('Constantes'))
        self.AssignObjects()

    def GetValue(self, address, object):
        # Checa si estamos obteniendo un atributo de un objeto AFUERA de un objeto
        if isinstance(address, list):
            objeto = int(address[0])
            parametro = str(address[1])
            return self.memory[objeto][parametro]
        else: 
            # Checa si esta en el rango de memoria local para saber si tiene que ir a buscar ahi
            if (IsInLocalRange(address)):
                return self.memoryStack.top().GetValue(address)
            else:
                # Checa si estamos adentro de una funcion y no llamando a constantes
                if object != None and address < Dir.INT_CONSTANTE:
                    objectAddress = object.get('Object')
                    # Checa si estamos dentro de un objeto para obtener un valor
                    if objectAddress == '_':
                        return self.memory[address]
                    else:
                        return self.memory[objectAddress][str(address)]
                else:    
                    return self.memory[address]
    
    def SetValue(self, address, value, funcion):
        # Checa si estamos asigando un atributo de un objeto AFUERA de un objeto
        if isinstance(address, list):
            objeto = int(address[0])
            parametro = str(address[1])
            self.memory[objeto][str(parametro)] = value
        else: 
            # Checa si esta en el rango de memoria local para saber si tiene que ir a buscar ahi
            if (IsInLocalRange(address)):
                self.memoryStack.top().SetValue(address, value)
            else:
                # Checa si estamos adentro de una funcion y no llamando a constantes
                if funcion != None and address < Dir.INT_CONSTANTE:
                    objectAddress = funcion.get('Object')
                    # Checa si estamos dentro de un objeto para asignar un atributo
                    if objectAddress == '_':
                        self.memory[address] = value
                    else:
                        self.memory[objectAddress][str(address)] = value
                else:
                    self.memory[address] = value

    def AssignConstants(self, constantes):
        # Se invierte la tabla de constantes para poder tener las direcciones
        constantes.InvertDictionary(constantes.Tabla)
        for constant in constantes.Tabla:
            type = GetTypeOfConstantGivenTheAddress(int(constant))
            value = constantes.GetConstant(str(constant))
            if type == 'int':
                value = int(value)
            elif type == 'float':
                value = float(value)
            if type == 'string':
                value = str(value)
            self.memory[int(constant)] = value
        
    def AssignObjects(self):
        numObjetos = len(self.directory.Objetos)
        for i in range(Dir.OBJETOS, Dir.OBJETOS + numObjetos):
            self.memory[i] = {}

    def CreateNewLocalMemory(self, space):
        memory = LocalMemory(space)
        return memory
        
    def MountNewLocalMemory(self, memory):
        self.memoryStack.push(memory)

    def UnloadLastLocalMemory(self):
        self.memoryStack.pop()

        
