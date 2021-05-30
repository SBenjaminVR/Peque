from localMemory import LocalMemory
from stack import Stack

def IsInLocalRange(address):
    return address >= 8000 and address <= 15000
        
class Memory:
    def __init__(self, data):
        self.memory = [None]*30000
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
        self.memoryStack.push(memory)

    def UnloadLastLocalMemory(self):
        self.memoryStack.pop()

        
