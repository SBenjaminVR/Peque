from memory import Memory
from stack import Stack
import time

returnDirection = Stack()
functions = Stack() 

def GetQuadrupleValue(quadruple):
    iz = quadruple.get('iz')
    de = quadruple.get('de')
    res = quadruple.get('res')
    return iz, de, res

class VirtualMachine():
    def __init__(self, data):
        print('CREANDO LA VM')
        self.memory = Memory(data)
        self.start_time = time.time()

    def run(self):
        self.ProcessQuadruples()

    def ProcessQuadruples(self):
        current = 0
        quadruples = len(self.memory.quadruples)
        while current < quadruples:
            print('A continuación el cuarteto #' +str(current))
            quadruple = self.memory.quadruples[current]
            print(quadruple)
            operation = quadruple.get('op')

            iz, de, res = GetQuadrupleValue(quadruple)

            if operation == 1:
                self.ProcessPLUS(iz, de, res)
                
            elif operation == 2:
                self.ProcessMINUS(iz, de, res)
                
            elif operation == 3:
                self.ProcessTIMES(iz, de, res)
                
            elif operation == 4:
                self.ProcessDIVIDE(iz, de, res)
                
            elif operation == 5:
                self.ProcessASSIGN(iz, res)
                
            elif operation == 6:
                self.ProcessBIGGER(iz, de, res)
                
            elif operation == 7:
                self.ProcessLESS(iz, de, res)
                
            elif operation == 8:
                self.ProcessBIGGER_EQUAL(iz, de, res)
                
            elif operation == 9:
                self.ProcessLESS_EQUAL(iz, de, res)
                
            elif operation == 10:
                self.ProcessEQUAL(iz, de, res)
                
            elif operation == 11:
                self.ProcessDIFFERENT(iz, de, res)
                
            elif operation == 12:
                self.ProcessAND(iz, de, res)
                
            elif operation == 13:
                self.ProcessOR(iz, de, res)
                
            elif operation == 14:
                current = res
                continue

            elif operation == 15:
                if self.IsGOTOF(iz):
                    current = res
                    continue

            elif operation == 16:
                self.ProcessERA(iz, res)
                functions

            elif operation == 17:
                self.ProcessGOSUB(iz, de)
                returnDirection.push(current + 1)
                current = res
                continue

            elif operation == 18:
                self.ProcessPARAMETRO(iz, res)

            elif operation == 19:
                self.ProcessReturn(res)

            elif operation == 20:
                self.ProcessENDPROC()
                current = returnDirection.pop()
                continue

            elif operation == 21:
                self.ProcessVER(iz, de, res)

            elif operation == 22:
                self.ProcessPRINT(iz)

            elif operation == 23:
                self.ProcessINPUT(iz)

            elif operation == 24:
                self.ProcessEND()

            current = current + 1
                
                
    def ProcessPLUS(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        print(str(iz) + ' + ' + str(de))
        self.memory.SetValue(result, iz + de)
    
    def ProcessMINUS(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        print(str(iz) + ' - ' + str(de))
        self.memory.SetValue(result, iz - de)

    def ProcessTIMES(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz * de)

    def ProcessDIVIDE(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        if self.IsInt(iz) and self.IsInt(de):
            self.memory.SetValue(result, iz // de)
        else:
            self.memory.SetValue(result, iz / de)

    def ProcessASSIGN(self, left, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        if not isinstance(result, int):
            result = result[1:-1]
            result = self.memory.GetValue(int(result))    
        self.memory.SetValue(result, iz)
        print('Asignando ' + str(iz) + ' en direccion ' + str(result))
        

    def ProcessBIGGER(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz > de)
    
    def ProcessLESS(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz < de)

    def ProcessBIGGER_EQUAL(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz >= de)

    def ProcessLESS_EQUAL(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz <= de)

    def ProcessEQUAL(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz == de)

    def ProcessDIFFERENT(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz != de)

    def ProcessAND(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz and de)

    def ProcessOR(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz or de)

    def IsGOTOF(self, left):
        value = self.GetValueInsideValueIfParenthesis(left)
        print('ADENTRO DEL GOTOF')
        print(value)
        if not value:
            return True
        return False

    def ProcessERA(self, left, res):
        self.memory.directory.Scope = res
        space = self.memory.directory.GetFunctionAttribute(left, 'Space')
        self.memory.CreateNewLocalMemory(space)

    def ProcessGOSUB(self, left, right):
        if right != '_':
            address = self.memory.directory.GetObjectAddress(right, left)
        else:
            address = self.memory.directory.GetFunctionAddress(left)
        functions.push({'Name': left, 'Address': address})

    def ProcessPARAMETRO(self, left, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        print("PARAM " + str(iz) + ' --->' + str(result))
        self.memory.SetValue(result, iz)

    def ProcessReturn(self, res):
        value = self.GetValueInsideValueIfParenthesis(res)
        currentFunction = functions.top()
        address = currentFunction.get('Address')
        self.memory.SetValue(address, value)

    def ProcessENDPROC(self):
        functions.pop()
        self.memory.UnloadLastLocalMemory()
    
    def ProcessVER(self, left, right, res):
        val = self.GetValueInsideValueIfParenthesis(left)
        print (str(val) + ' debe estar entre ' + str(right)  + ' y ' + str(res))
        if right <= val and val <= res:
            return
        else: 
            raise ErrorMsg('Se esta tratando de acceder a un espacio fuera del limite de un arreglo')

    def ProcessPRINT(self, left):
        iz = self.GetValueInsideValueIfParenthesis(left)
        print(str(iz))

    def ProcessINPUT(self, left):
        userInput = int(input())
        print('Asignando ' + str(userInput) + ' en direccion ' + str(left))
        self.memory.SetValue(left, userInput)

    def ProcessEND(self):
        print('Programa se termino de ejecutar en: ' + str(time.time() - self.start_time) + ' s')

    def GetValueInsideValueIfParenthesis(self, value):
        if isinstance(value, int):
            current = self.memory.GetValue(value)
        else:
            #Se quitan los parentesis y se accede al primer valor
            value = value[1:-1]
            aux = self.memory.GetValue(int(value))
            current = self.memory.GetValue(aux)
        # Se checa que no se este tratando de acceder a una casilla vacia
        if current != None:
            return current
        else:
            raise ErrorMsg('Se esta tratando de acceder a una casilla sin valor')

    def IsFloat(self, var):
        return isinstance(var, float)

    def IsInt(self, var):
        return isinstance(var, int)

class ErrorMsg(Exception):
    def __init__(self, message):
        self.message = message