from memory import Memory

def GetQuadrupleValue(quadruple):
    iz = quadruple.get('iz')
    de = quadruple.get('de')
    res = quadruple.get('res')
    return iz, de, res

class VirtualMachine():
    def __init__(self, data):
        print('CREANDO LA VM')
        self.memory = Memory(data)

    def run(self):
        self.ProcessQuadruples()

    def ProcessQuadruples(self):
        current = 0
        quadruples = len(self.memory.quadruples)
        while current < quadruples:
            quadruple = self.memory.quadruples[current]
            operation = quadruple.get('op')
            iz, de, res = GetQuadrupleValue(quadruple)

            if operation == 1:
                self.ProcessPLUS(iz, de, res)
                current = current + 1
            elif operation == 2:
                self.ProcessMINUS(iz, de, res)
                current = current + 1
            elif operation == 3:
                self.ProcessTIMES(iz, de, res)
                current = current + 1
            elif operation == 4:
                self.ProcessDIVIDE(iz, de, res)
                current = current + 1
            else:
                current = current + 1
            '''
            elif operation == '5':
                # Do Something
            elif operation == '6':
                # Do Something
            elif operation == '7':
                # Do Something
            elif operation == '8':
                # Do Something
            elif operation == '9':
                # Do Something
            elif operation == '10':
                # Do Something
            elif operation == '11':
                # Do Something
            elif operation == '12':
                # Do Something
            elif operation == '13':
                # Do Something
            elif operation == '14':
                # Do Something
            elif operation == '15':
                # Do Something
            elif operation == '16':
                # Do Something
            elif operation == '17':
                # Do Something
            elif operation == '18':
                # Do Something
            elif operation == '19':
                # Do Something
            elif operation == '20':
                # Do Something
            elif operation == '21':
                # Do Something
            elif operation == '22':
                # Do Something
            elif operation == '23':
                # Do Something
            elif operation == '24':
                # Do Something
            '''

    def ProcessPLUS(self, left, right, result):
        iz = self.memory.GetValue(left)
        de = self.memory.GetValue(right)
        self.memory.SetValue(result, iz + de)
    
    def ProcessMINUS(self, left, right, result):
        iz = self.memory.GetValue(left)
        de = self.memory.GetValue(right)
        self.memory.SetValue(result, iz - de)

    def ProcessTIMES(self, left, right, result):
        iz = self.memory.GetValue(left)
        de = self.memory.GetValue(right)
        self.memory.SetValue(result, iz * de)

    def ProcessDIVIDE(self, left, right, result):
        iz = self.memory.GetValue(left)
        de = self.memory.GetValue(right)
        self.memory.SetValue(result, iz / de)

    def traerValorNumerico(self, var):
        if self.esIntOFloat(var):
            return var
        elif self.esUnDigito(var):
            return var
        elif self.esUnTemporal(var):
            return (self.directorio.get('Temporales').get(var))

    def esIntOFloat(self, var):
        return isinstance(var, int) or isinstance(var, float)

    def esUnDigito(self, var):
        return var.isdigit()

    def esUnTemporal(self, var):
        return var.startswith('_t')

    def procesarPrint(self, valores):
        Imprimir = []
        listaDeValores = valores.split(", ")
        for val in listaDeValores:
            Imprimir.append(self.traerValorNumerico(val))
        print(*Imprimir, sep = ", ")
    
        