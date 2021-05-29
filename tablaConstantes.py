def InvertDictionary(d):
    return {value: key for key, value in d.items()}

def ConstantAlreadyExists(d, constant):
    return d.get(constant) != None

class TablaConstantes:
    INT_CONSTANTE = 20000
    FLOAT_CONSTANTE = 21000
    CHAR_CONSTANTE =  22000
    BOOL_CONSTANTE = 23000

    Last = []
    def __init__(self):
        self.Last = [0]*4
        self.Tabla = {}
        self.IsInverted = False

    def GetMemoryAddress(self, constant, type):
        constant = str(constant)
        address = 0

        if self.IsInverted:
            self.Tabla = InvertDictionary(self.Tabla)
            self.IsInverted = False

        if ConstantAlreadyExists(self.Tabla, constant):
            return int(self.Tabla.get(constant)) 
        else:
            if type == 'int':
                address = self.INT_CONSTANTE + self.Last[0]
                self.Last[0] = self.Last[0] + 1
            elif type == 'float':
                address = self.FLOAT_CONSTANTE + self.Last[1]
                self.Last[1] = self.Last[1] + 1
            elif type == 'char':
                address = self.CHAR_CONSTANTE + self.Last[2]
                self.Last[2] = self.Last[2] + 1
            elif type == 'bool':
                address = self.BOOL_CONSTANTE + self.Last[3]
                self.Last[3] = self.Last[3] + 1
        self.Tabla[constant] = str(address)
        return int(address)

    def GetConstant(self, address):
        address = str(address)
        if not self.IsInverted:
            self.Tabla = InvertDictionary(self.Tabla)
            self.IsInverted = True
        return int(self.Tabla.get(address))

    