from memory import Memory
from stack import Stack
from localMemory import LocalMemory
import time

returnDirection = Stack()
functions = Stack() 
NewLocalMemory = Stack()

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

            elif operation == 27:
                self.ProcessAPPEND(iz, res)

            current = current + 1
                
                
    def ProcessPLUS(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        print(str(iz) + ' + ' + str(de))
        self.memory.SetValue(result, iz + de, functions.top())
    
    def ProcessMINUS(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        print(str(iz) + ' - ' + str(de))
        self.memory.SetValue(result, iz - de, functions.top())

    def ProcessTIMES(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz * de, functions.top())

    def ProcessDIVIDE(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        if self.IsInt(iz) and self.IsInt(de):
            self.memory.SetValue(result, iz // de, functions.top())
        else:
            self.memory.SetValue(result, iz / de, functions.top())

    def ProcessASSIGN(self, left, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        print('Asignando ' + str(iz) + ' en direccion ' + str(result))
        if not isinstance(result, int):
            if result[0] == '(':
                result = result[1:-1]
                res = self.memory.GetValue(int(result), functions.top())
            else:
                res = result.split('.')
        else:
            res = int(result)
        self.memory.SetValue(res, iz, functions.top())
        

    def ProcessBIGGER(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz > de, functions.top())
    
    def ProcessLESS(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz < de, functions.top())

    def ProcessBIGGER_EQUAL(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz >= de, functions.top())

    def ProcessLESS_EQUAL(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz <= de, functions.top())

    def ProcessEQUAL(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz == de, functions.top())

    def ProcessDIFFERENT(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz != de, functions.top())

    def ProcessAND(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz and de, functions.top())

    def ProcessOR(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz or de, functions.top())

    def IsGOTOF(self, left):
        value = self.GetValueInsideValueIfParenthesis(left)
        print('ADENTRO DEL GOTOF')
        print(value)
        if not value:
            return True
        return False

    def ProcessERA(self, left, res):
        space = self.memory.directory.GetFunctionSpace(left, res)
        NewLocalMemory.push(self.memory.CreateNewLocalMemory(space))

    def ProcessGOSUB(self, left, right):
        if right != '_':
            obj = self.memory.directory.Objetos[right].get('Address')
        else: 
            obj = '_'
        address = self.memory.directory.GetObjectAddress(left, right)
        functions.push({'Name': left, 'Address': address, 'Object': obj})
        functions.printStack()
        self.memory.MountNewLocalMemory(NewLocalMemory.pop())

    def ProcessPARAMETRO(self, left, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        print("PARAM " + str(iz) + ' --->' + str(result))
        currentMemory = NewLocalMemory.top()
        currentMemory.SetValue(result, iz)

    def ProcessReturn(self, res):
        value = self.GetValueInsideValueIfParenthesis(res)
        currentFunction = functions.top()
        address = currentFunction.get('Address')
        self.memory.SetValue(address, value, functions.top())

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
        self.memory.SetValue(left, userInput, functions.top())

    def ProcessEND(self):
        print('Programa se termino de ejecutar en: ' + str(time.time() - self.start_time) + ' s')

    def ProcessAPPEND(self, left, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        available = self.GetNextAvailableSpaceOfList(result)
        self.memory.SetValue(result + available, iz, functions.top())

    def GetValueInsideValueIfParenthesis(self, value):
        if isinstance(value, int):
            current = self.memory.GetValue(value, functions.top())
        else:
            #Se quitan los parentesis y se accede al primer valor
            if value[0] == '(':
                value = value[1:-1]
                aux = self.memory.GetValue(int(value), functions.top())
            else:
                # Entonces detectamos que se esta accediendo a un parametro de un objeto
                aux = value.split('.')
            print(aux)
            current = self.memory.GetValue(aux, functions.top())
        # Se checa que no se este tratando de acceder a una casilla vacia
        if current != None:
            return current
        else:
            raise ErrorMsg('Se esta tratando de acceder a una casilla sin valor')

    def GetNextAvailableSpaceOfList(self, baseAddress):
        c = 0
        res = self.memory.GetValue(baseAddress + c, functions.top())
        while res != None:
            c = c + 1
            res = self.memory.GetValue(baseAddress + c, functions.top())
        return c

    def IsString(self, var):
        if isinstance(var, str):
            return var[0] == '"'
        return False

    def IsFloat(self, var):
        return isinstance(var, float)

    def IsInt(self, var):
        return isinstance(var, int)

class ErrorMsg(Exception):
    def __init__(self, message):
        self.message = message