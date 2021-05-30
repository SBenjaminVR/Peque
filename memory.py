class Memory:
    def __init__(self, data):
        self.memory = [None]*30000
        self.memoryStack = []
        self.isGlobal = True
        self.quadruples = data.get('Cuadruplos')
        self.directory = data.get('Directorio')

        self.AssignConstants(data.get('Constantes'))

    def GetValue(self, address):
        if self.isGlobal == True:
            return self.memory[address]
        else:
            print('FALTA IMPLIMENTAR STACKS')
    
    def SetValue(self, address, value):
        if self.isGlobal == True:
            self.memory[address] = value
        else:
            print('FALTA IMPLIMENTAR STACKS')

    def AssignConstants(self, constantes):
        # Se invierte la tabla de constantes para poder tener las direcciones
        constantes.InvertDictionary(constantes.Tabla)
        for constant in constantes.Tabla:
            self.memory[int(constant)] = constantes.GetConstant(constant) 


        
