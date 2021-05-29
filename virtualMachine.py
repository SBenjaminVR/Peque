from memory import Memory

class VirtualMachine():
    directorio = {}
    cuadruplos = []
    def __init__(self, data):
        print('CREANDO LA VM')
        self.memory = Memory(data)

    def run(self):
        print('Estoy adentro de la vm')
        

    def procesarCuarteto(self, cuadruplo):
        op = cuadruplo.get('op')
        iz = self.traerValorNumerico(cuadruplo.get('iz'))
        de = self.traerValorNumerico(cuadruplo.get('de'))
        res = cuadruplo.get('res')
        if op == "/":
            val = iz / de
            self.guardarResultadoExpresion(res, val)
        elif op == "*":
            val = iz * de
            self.guardarResultadoExpresion(res, val)
        elif op == "+":
            val = iz + de
            self.guardarResultadoExpresion(res, val)
        elif op == "-":
            val = iz - de
            self.guardarResultadoExpresion(res, val)
        elif op == "Goto":
            return self.memory[self.ARR + address]
        elif op == "print":
            return self.procesarPrint(res)

    def guardarResultadoExpresion(self, res, val):
        if self.esUnTemporal(res):
            self.directorio['Temporales'][res] = val

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
    
        