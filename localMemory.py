from direcciones import DireccionesMemoria
Dir = DireccionesMemoria()

# Initializes the given addresses with a None
def InsertAddresses(local, number, base):
    for x in range(number):
        local[str(x + base)] = None
    return local

# Assigns the direction of the local memory according to the data type
def AssignLocalStorage(local, number, option):
    if option == 0:
        return InsertAddresses(local, number, Dir.INT_LOCAL)
    if option == 1:
        return InsertAddresses(local, number, Dir.FLOAT_LOCAL)
    if option == 2:
        return InsertAddresses(local, number, Dir.BOOL_LOCAL)
    if option == 3:
        return InsertAddresses(local, number*100, Dir.LIST_INT_LOCAL)
    if option == 4:
        return InsertAddresses(local, number*100, Dir.LIST_FLOAT_LOCAL)
    if option == 5:
        return InsertAddresses(local, number*100, Dir.LIST_BOOL_LOCAL)
    if option == 6:
        return InsertAddresses(local, number, Dir.INT_LOCAL_TEMPORAL)
    if option == 7:
        return InsertAddresses(local, number, Dir.FLOAT_LOCAL_TEMPORAL)
    if option == 8:
        return InsertAddresses(local, number, Dir.BOOL_LOCAL_TEMPORAL)

class LocalMemory():
    # Creates the local memory
    def __init__(self, space):
        self.local = {}
        spaceSize = len(space)
        for i in range(spaceSize): 
            self.local = AssignLocalStorage(self.local, space[i], i)

    # Returns the value stored in the given address 
    def GetValue(self, address):
        address = str(address)
        return self.local.get(address)

    # Stores the given value in the address
    def SetValue(self, address, value):
        address = str(address)
        self.local[address] = value


