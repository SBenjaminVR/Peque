from direcciones import DireccionesMemoria
Dir = DireccionesMemoria()

def InsertAddresses(local, number, base):
    for x in range(number):
        local[str(x + base)] = None
    return local

def AssignLocalStorage(local, number, option):
    if option == 0:
        return InsertAddresses(local, number, Dir.INT_LOCAL)
    if option == 1:
        return InsertAddresses(local, number, Dir.FLOAT_LOCAL)
    if option == 2:
        return InsertAddresses(local, number, Dir.BOOL_LOCAL)
    if option == 3:
        return InsertAddresses(local, number, Dir.LIST_INT_LOCAL)
    if option == 4:
        return InsertAddresses(local, number, Dir.LIST_FLOAT_LOCAL)
    if option == 5:
        return InsertAddresses(local, number, Dir.LIST_BOOL_LOCAL)
    if option == 6:
        return InsertAddresses(local, number, Dir.INT_LOCAL_TEMPORAL)
    if option == 7:
        return InsertAddresses(local, number, Dir.FLOAT_LOCAL_TEMPORAL)
    if option == 8:
        return InsertAddresses(local, number, Dir.BOOL_LOCAL_TEMPORAL)
    if option == 9:
        return InsertAddresses(local, number, Dir.LIST_INT_LOCAL_TEMPORAL)
    if option == 10:
        return InsertAddresses(local, number, Dir.LIST_FLOAT_LOCAL_TEMPORAL)
    if option == 11:
        return InsertAddresses(local, number, Dir.LIST_BOOL_LOCAL_TEMPORAL)
    

class LocalMemory():
    def __init__(self, space):
        self.local = {}
        print('--------------------------')
        print(space)
        spaceSize = len(space)
        for i in range(spaceSize): 
            self.local = AssignLocalStorage(self.local, space[i], i)
        print(self.local)

    def GetValue(self, address):
        address = str(address)
        print(self.local)
        return self.local.get(address)

    def SetValue(self, address, value):
        address = str(address)
        self.local[address] = value


