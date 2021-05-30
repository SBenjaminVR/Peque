def InsertAddresses(local, number, base):
    for x in range(number):
        local[str(x + base)] = None
    return local

def AssignLocalStorage(local, number, option):
    if option == 0:
        return InsertAddresses(local, number, 8000)
    if option == 1:
        return InsertAddresses(local, number, 9000)
    if option == 2:
        return InsertAddresses(local, number, 10000)
    if option == 3:
        return InsertAddresses(local, number, 11000)
    if option == 4:
        return InsertAddresses(local, number, 0)
    if option == 5:
        return InsertAddresses(local, number, 12000)
    if option == 6:
        return InsertAddresses(local, number, 13000)
    if option == 7:
        return InsertAddresses(local, number, 14000)
    if option == 8:
        return InsertAddresses(local, number, 15000)
    if option == 9:
        return InsertAddresses(local, number, 0)



class LocalMemory():
    def __init__(self, space):
        self.local = {}
        spaceSize = len(space)
        for i in range(spaceSize): 
            self.local = AssignLocalStorage(self.local, space[i], i)
        print(self.local)

    def GetValue(self, address):
        address = str(address)
        return self.local[address]

    def SetValue(self, address, value):
        address = str(address)
        self.local[address] = value


