from localMemory import LocalMemory
from stack import Stack
from direcciones import DireccionesMemoria

Dir = DireccionesMemoria()

# Checks if the given address is the range of the local addresses
def IsInLocalRange(address):
    return address >= Dir.INT_LOCAL and address <= Dir.BOOL_LOCAL_TEMPORAL

# Returns the data type of the constant given an address  
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
    # It mounts the memory, the directory and the quadruples. It also stores the value of the constants
    def __init__(self, data):
        self.memory = [None]*35000
        self.memoryStack = Stack()
        self.quadruples = data.get('Cuadruplos')
        self.directory = data.get('Directorio')

        self.AssignConstants(data.get('Constantes'))
        self.AssignObjects()

    # Gets the value of a given address, it also takes into account if you have to access an object
    def GetValue(self, address, object):
        # Checks if we are trying to access an atributte of an object OUTSIDE the object
        if isinstance(address, list):
            objeto = int(address[0])
            parametro = str(address[1])
            return self.memory[objeto][parametro]
        else: 
            if (IsInLocalRange(address)):
                # Stores the value in the top local memory
                return self.memoryStack.top().GetValue(address)
            else:
                # Checks if we are inside of a function
                if object != None and address < Dir.INT_CONSTANTE:
                    objectAddress = object.get('Object')
                    # Checks if we are inside of an object
                    if objectAddress == '_':
                        return self.memory[address]
                    else:
                        return self.memory[objectAddress][str(address)]
                else:    
                    return self.memory[address]
    
    def SetValue(self, address, value, funcion):
        #  Checks if we are trying to access an atributte of an object OUTSIDE the object
        if isinstance(address, list):
            objeto = int(address[0])
            parametro = str(address[1])
            self.memory[objeto][str(parametro)] = value
        else: 
            # Stores the value in the top local memory
            if (IsInLocalRange(address)):
                self.memoryStack.top().SetValue(address, value)
            else:
                # Checks if we are inside of an function
                if funcion != None and address < Dir.INT_CONSTANTE:
                    objectAddress = funcion.get('Object')
                    # Checks if we are inside of an object
                    if objectAddress == '_':
                        self.memory[address] = value
                    else:
                        self.memory[objectAddress][str(address)] = value
                else:
                    self.memory[address] = value

    # Stores the constants in the memory
    def AssignConstants(self, constantes):
        # The constants table gets inverted to get the Constants
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

    # Assigns the initial value of {} to the objects 
    def AssignObjects(self):
        numObjetos = len(self.directory.Objetos)
        for i in range(Dir.OBJETOS, Dir.OBJETOS + numObjetos):
            self.memory[i] = {}

    # Creates a new local memory of the given space
    def CreateNewLocalMemory(self, space):
        memory = LocalMemory(space)
        return memory
        
    # Pushes the a local memory in the memory stack
    def MountNewLocalMemory(self, memory):
        self.memoryStack.push(memory)

    # Removes the last local memory from the stack
    def UnloadLastLocalMemory(self):
        self.memoryStack.pop()

        
