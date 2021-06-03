from memory import Memory
from stack import Stack
from localMemory import LocalMemory
import time

returnDirection = Stack()
functions = Stack() 
NewLocalMemory = Stack()

# Returns the value of the operations of the quadruple
def GetQuadrupleValue(quadruple):
    iz = quadruple.get('iz')
    de = quadruple.get('de')
    res = quadruple.get('res')
    return iz, de, res

class VirtualMachine():
    # Creates the memory and starts to track the execution time
    def __init__(self, data):
        self.memory = Memory(data)
        self.start_time = time.time()

    # Starts to process the quadruples in order until it reaches the end
    def run(self):
        self.ProcessQuadruples()

    # The main function that is going to be processing each quadruple according to their operation
    def ProcessQuadruples(self):
        current = 0
        quadruples = len(self.memory.quadruples)
        #Process each quadruple until we finish
        while current < quadruples:
            quadruple = self.memory.quadruples[current]
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
                #Saves the quadruple to return after it finishes to execute the function
                returnDirection.push(current + 1)
                current = res
                continue

            elif operation == 18:
                self.ProcessPARAMETRO(iz, res)

            elif operation == 19:
                self.ProcessRETURN(res)

            elif operation == 20:
                self.ProcessENDPROC()
                #Returns to the direction saved after finishing a function
                current = returnDirection.pop()
                continue

            elif operation == 21:
                self.ProcessVER(iz, de, res)

            elif operation == 22:
                self.ProcessPRINT(iz)

            elif operation == 23:
                self.ProcessINPUT(iz, de)

            elif operation == 24:
                self.ProcessEND()

            elif operation == 27:
                self.ProcessAPPEND(iz, res)

            elif operation == 28:
                self.ProcessPOP(iz)

            elif operation == 29:
                self.ProcessSORT(iz)

            elif operation == 30:
                self.ProcessFIND(iz, de, res)

            elif operation == 31:
                self.ProcessHEAD(iz, res)

            elif operation == 32:
                self.ProcessTAIL(iz, res)

            elif operation == 33:
                self.ProcessKEY(iz, de, res)

            current = current + 1
                
    # Sums the values stored in the left and right addresses and stores the result in the result address
    def ProcessPLUS(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz + de, functions.top())
    
    # Substracts the values stored in the left and right addresses and stores the result in the result address
    def ProcessMINUS(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz - de, functions.top())

    # Miltiplies the values stored in the left and right addresses and stores the result in the result address
    def ProcessTIMES(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz * de, functions.top())

    # Divides the values stored in the left and right addresses and stores the result in the result address
    def ProcessDIVIDE(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        #Checks if it has to do a int division or a float division
        if self.IsInt(iz) and self.IsInt(de):
            self.memory.SetValue(result, iz // de, functions.top())
        else:
            self.memory.SetValue(result, iz / de, functions.top())

    # Assigns the value in the left address and stores the result in the result address
    def ProcessASSIGN(self, left, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        # Checks if we are trying to assign the value of an object or the address of another address
        if not isinstance(result, int):
            if result[0] == '(':
                result = result[1:-1]
                res = self.memory.GetValue(int(result), functions.top())
            else:
                res = result.split('.')
        else:
            res = int(result)
        self.memory.SetValue(res, iz, functions.top())
        

    # Checks if the value of the left address is bigger than the one in the right address and stores the result in the result address
    def ProcessBIGGER(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz > de, functions.top())
    
    # Checks if the value of the left address is lower than the one in the right address and stores the result in the result address
    def ProcessLESS(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz < de, functions.top())

    # Checks if the value of the left address is bigger or equal than the one in the right address and stores the result in the result address
    def ProcessBIGGER_EQUAL(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz >= de, functions.top())


     # Checks if the value of the left address is lower or equal than the one in the right address and stores the result in the result address
    def ProcessLESS_EQUAL(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz <= de, functions.top())

     # Checks if the value of the left address is bigger or equal than the one in the right address and stores the result in the result address
    def ProcessEQUAL(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz == de, functions.top())

     # Checks if the value of the left address is diferent than the one on the right address and stores the result in the result address
    def ProcessDIFFERENT(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz != de, functions.top())

     # Checks if the value of the left address and the one on the right address are both true and stores the result in the result address
    def ProcessAND(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz and de, functions.top())

    # Checks if either the value of the left address or the one on the right address is true and stores the result in the result address
    def ProcessOR(self, left, right, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        de = self.GetValueInsideValueIfParenthesis(right)
        self.memory.SetValue(result, iz or de, functions.top())

    # Checks if the value of the left address is false to known wheter it should make a jump or continue to the next quadruple
    def IsGOTOF(self, left):
        value = self.GetValueInsideValueIfParenthesis(left)
        if not value:
            return True
        return False

    # Gets the space of the function and creates a new local memory with the space required
    def ProcessERA(self, left, res):
        space = self.memory.directory.GetFunctionSpace(left, res)
        NewLocalMemory.push(self.memory.CreateNewLocalMemory(space))

    # Goes to the address of the "left" function and mounts the local memory in the memory, it also stores the address of the object if there's any
    def ProcessGOSUB(self, left, right):
        if right != '_':
            obj = self.memory.directory.Objetos[right].get('Address')
        else: 
            obj = '_'
        address = self.memory.directory.GetObjectAddress(left, right)
        functions.push({'Name': left, 'Address': address, 'Object': obj})
        self.memory.MountNewLocalMemory(NewLocalMemory.pop())

    # Stores the value of the left address in the result address of the last created local memory
    def ProcessPARAMETRO(self, left, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        currentMemory = NewLocalMemory.top()
        currentMemory.SetValue(result, iz)

    #Stores the value of the res address in the address of the current function
    def ProcessRETURN(self, res):
        value = self.GetValueInsideValueIfParenthesis(res)
        currentFunction = functions.top()
        address = currentFunction.get('Address')
        self.memory.SetValue(address, value, functions.top())

    # Unmounts the last local memory and the last stored function 
    def ProcessENDPROC(self):
        functions.pop()
        self.memory.UnloadLastLocalMemory()
    
    # Checks if the value of the left address is between right and res
    def ProcessVER(self, left, right, res):
        val = self.GetValueInsideValueIfParenthesis(left)
        if right <= val and val <= res:
            return
        else: 
            raise ErrorMsg('Se esta tratando de acceder a un espacio fuera del limite de un arreglo')

    # Prints the value stored in the left address
    def ProcessPRINT(self, left):
        iz = self.GetValueInsideValueIfParenthesis(left)
        print(str(iz))

    # Checks if the text inputted by the user corresponds to the type in right and stores its value in the left address
    def ProcessINPUT(self, left, right):
        userInput = input()
        value = self.GetUserInput(userInput, right)
        if not isinstance(left, int):
            if left[0] == '(':
                left = left[1:-1]
                res = self.memory.GetValue(int(left), functions.top())
            else:
                res = left.split('.')
        else:
            res = int(left)
        self.memory.SetValue(res, value, functions.top())

    # Prints a finish text and the time it took to execute the program
    def ProcessEND(self):
        print('Programa se termino de ejecutar en: ' + str(time.time() - self.start_time) + ' s')

    # Adds an element to the end of a list
    def ProcessAPPEND(self, left, result):
        iz = self.GetValueInsideValueIfParenthesis(left)
        available = self.GetNextAvailableSpaceOfList(result)
        self.memory.SetValue(result + available, iz, functions.top())

    # Removes the element at the end of the list
    def ProcessPOP(self, address):
        available = self.GetLastAvailableSpaceOfList(address)
        self.memory.SetValue(address + available, None, functions.top())

    # Sorts the elements of a list in increasing value
    def ProcessSORT(self, address):
        lista = []
        lastAvailable = self.GetNextAvailableSpaceOfList(address)
        for i in range(address, address + lastAvailable):
            lista.append(self.memory.GetValue(i, functions.top()))
        lista.sort()
        current = 0
        for i in range(address, address + lastAvailable):
            self.memory.SetValue(i, lista[current], functions.top())
            current = current + 1

    # Searches the first position of the given value on the list and stores it in tempAdress
    # Stores a -1 if it doesn't find the element on the list
    def ProcessFIND(self, address, val, tempAddress):
        lastAvailable = self.GetNextAvailableSpaceOfList(address)
        value = self.GetValueInsideValueIfParenthesis(val)
        spot = -1
        number = 0
        #Searches from 0 to the last spot available of the list
        for i in range(address, address + lastAvailable):
            current = self.memory.GetValue(i, functions.top())
            if current == value:
                spot = number
                break
            number = number + 1
        self.memory.SetValue(tempAddress, spot, functions.top())
        

    # Stores the value of the last element the list on tempAdress
    def ProcessHEAD(self, address, tempAddress):
        lastAvailable = self.GetLastAvailableSpaceOfList(address)
        value = self.memory.GetValue(address + lastAvailable, functions.top())
        self.memory.SetValue(tempAddress, value, functions.top())

    # Stores the value of the first element the list on tempAdress
    def ProcessTAIL(self, address, tempAddress):
        value = self.memory.GetValue(address, functions.top())
        self.memory.SetValue(tempAddress, value, functions.top())

    # Stores the value of the position of the val element the list on tempAdress
    def ProcessKEY(self, address, val, tempAddress):
        val = self.GetValueInsideValueIfParenthesis(val)
        value = self.memory.GetValue(address + val, functions.top())
        self.memory.SetValue(tempAddress, value, functions.top())

    # Returns the value of the given address or the value of the address inside the adress if it has ()
    # It also checks if the for the adress if it's an object
    def GetValueInsideValueIfParenthesis(self, value):
        if isinstance(value, int):
            current = self.memory.GetValue(value, functions.top())
        else:
            # Removes the () and access the first value
            if value[0] == '(':
                value = value[1:-1]
                aux = self.memory.GetValue(int(value), functions.top())
            else:
                # Detects that we are acceding to an object 
                aux = value.split('.')
            current = self.memory.GetValue(aux, functions.top())
        # Shows an error message if you're trying to access to an access out of bounds
        if current != None:
            return current
        else:
            raise ErrorMsg('Se esta tratando de acceder a una casilla sin valor')

    # Returns the next space of the list that can be filled up
    def GetNextAvailableSpaceOfList(self, baseAddress):
        c = 0
        res = self.memory.GetValue(baseAddress + c, functions.top())
        while res != None and c < 99:
            c = c + 1
            res = self.memory.GetValue(baseAddress + c, functions.top())
        return c

    # Returns the last used space of the list
    def GetLastAvailableSpaceOfList(self, baseAddress):
        res = self.memory.GetValue(baseAddress, functions.top())
        if res != None:
            c = 0
            while res != None and c < 100:
                c = c + 1
                res = self.memory.GetValue(baseAddress + c, functions.top())
            return c - 1
        else:
            raise ErrorMsg('Se esta tratando de hacer pop() de una lista vacia')

    # Transforms the input of the user to the corresponding type
    def GetUserInput(self, input, type):
        if type == 'int':
            input = int(input)
        if type == 'float':
            input = float(input)
        return input

    # Checks if var is a string
    def IsString(self, var):
        if isinstance(var, str):
            return var[0] == '"'
        return False

    # Checks if var is a float
    def IsFloat(self, var):
        return isinstance(var, float)

    # Checks if var is a int
    def IsInt(self, var):
        return isinstance(var, int)

# Class to throw error messages
class ErrorMsg(Exception):
    def __init__(self, message):
        self.message = message