from direcciones import DireccionesMemoria
Dir = DireccionesMemoria()

def ConstantAlreadyExists(d, constant):
    return d.get(constant) != None

class TablaConstantes:
    Last = []
    def __init__(self):
        self.Last = [0]*4
        self.Tabla = {}
        self.IsInverted = False

    def GetMemoryAddress(self, constant, type):
        constant = str(constant)
        address = 0

        if self.IsInverted:
            self.InvertDictionary(self.Tabla)

        if ConstantAlreadyExists(self.Tabla, constant):
            return int(self.Tabla.get(constant)) 
        else:
            if type == 'int':
                address = Dir.INT_CONSTANTE + self.Last[0]
                self.Last[0] = self.Last[0] + 1
            elif type == 'float':
                address = Dir.FLOAT_CONSTANTE + self.Last[1]
                self.Last[1] = self.Last[1] + 1
            elif type == 'bool':
                address = Dir.BOOL_CONSTANTE + self.Last[2]
                self.Last[2] = self.Last[2] + 1
            elif type == 'string':
                address = Dir.STRING_CONSTANTE + self.Last[3]
                self.Last[3] = self.Last[3] + 1
        self.Tabla[constant] = str(address)
        return int(address)

    def GetConstant(self, address):
        address = str(address)
        if not self.IsInverted:
            self.InvertDictionary(self.Tabla)
        return int(self.Tabla.get(address))

    def InvertDictionary(self, d):
        self.IsInverted = not self.IsInverted
        self.Tabla = { value: key for key, value in d.items() }

    