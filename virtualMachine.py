from memory import Memory

memoriaGlobal = Memory()
cuartetosTest = [{'op': '*', 'iz': 3, 'de': 2, 'res': '_t0'}, {'op': '+', 'iz': '_t0', 'de': 2, 'res': '_t1'}]
directorioTest = {
    'Clases': {}, 
    'Funciones': {}, 
    'Variables': {'hola': {'Id': 'hola', 'DataType': 'int', 'EspacioMemoria': 0}, 'hello': {'Id': 'hello', 'DataType': 'int', 'EspacioMemoria': 1}}, 
    'Temporales': {'_t0': 10}
}

class VirtualMachine():
    directorio = {}
    cuartetos = []
    def __init__(self, data):
        print('CREANDO LA VM')
        #self.cuartetos = data.cuartetos
        #self.directorio = data.directorio
    def run(self):
        print('Estoy adentro de la vm')
        memoriaGlobal.addValueToMemory(5, 'Int', 0)
        print(memoriaGlobal.getValue('Int', 0))

        for item in cuartetosTest:
            self.procesarCuarteto(item)

    def procesarCuarteto(self, cuarteto):
        op = cuarteto.get('op')
        iz = self.traerValorNumerico(cuarteto.get('iz'))
        de = self.traerValorNumerico(cuarteto.get('de'))
        res = cuarteto.get('res')
        if op == "/":
            print(iz / de)
        elif op == "*":
            print(iz * de)
        elif op == "+":
            print(iz + de)
        elif op == "-":
            print(iz - de)
        elif op == "Goto":
            return self.memory[self.ARR + address]

    def traerValorNumerico(self, var):
        if self.esIntOFloat(var):
            return var
        elif self.esUnTemporal(var):
            return (directorioTest.get('Temporales').get(var))

    def esIntOFloat(self, var):
        return isinstance(var, int) or isinstance(var, float)
    def esUnTemporal(self, var):
        return var.startswith('_t')
    
        