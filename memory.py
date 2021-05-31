from localMemory import LocalMemory
from stack import Stack
from direcciones import DireccionesMemoria

Dir = DireccionesMemoria()

def IsInLocalRange(address):
    return address >= Dir.INT_LOCAL and address <= Dir.LIST_BOOL_LOCAL_TEMPORAL
        
def GetTypeOfValueGivenTheAddress(address):
    if address < Dir.INT_GLOBAL_TEMPORAL:
        return GetTypeGivenTheBase(address, 0)
    elif address < Dir.INT_LOCAL:
        return GetTypeGivenTheBase(address, 4000)
    elif address < Dir.INT_LOCAL_TEMPORAL:
        return GetTypeGivenTheBase(address, 8000)
    elif address < Dir.INT_CONSTANTE:
        return GetTypeGivenTheBase(address, 12000)

class Memory:
    def __init__(self, data):
        self.memory = [None]*35000
        self.memoryStack = Stack()
        self.quadruples = data.get('Cuadruplos')
        self.directory = data.get('Directorio')

        self.AssignConstants(data.get('Constantes'))

    def GetValue(self, address):
        if (IsInLocalRange(address)):
            return self.memoryStack.top().GetValue(address)
        else:
            return self.memory[address]
    
    def SetValue(self, address, value):
        if (IsInLocalRange(address)):
            self.memoryStack.top().SetValue(address, value)
        else:
            self.memory[address] = value

    def AssignConstants(self, constantes):
        # Se invierte la tabla de constantes para poder tener las direcciones
        constantes.InvertDictionary(constantes.Tabla)
        for constant in constantes.Tabla:
            self.memory[int(constant)] = constantes.GetConstant(constant) 

    def CreateNewLocalMemory(self, space):
        memory = LocalMemory(space)
        return memory
        
    def MountNewLocalMemory(self, memory):
        self.memoryStack.push(memory)

    def UnloadLastLocalMemory(self):
        self.memoryStack.pop()

        
