#this class assign the address of memory when ask for
#it is just a counter for each space of memory
#this class needs DirrecionesMemoria
#since you can find the exact base address anything

from direcciones import DireccionesMemoria
Dir = DireccionesMemoria()


class AsignadorMemoria:
    last = []
    def __init__(self):
        self.last = [0]*25
    #special function to assign address to an object
    def AssignMemoryAddressObject(self):
        address = Dir.OBJETOS + self.last[24]
        self.last[24] = self.last[24] + 1
        return address
    #function to assign memory depending on this values
    #type of function
    #scope of where are we
    #Location if we are assigning inside a function in a class or inside a function outside the class
    #we need the location, so we can return a temporal, a constant or a normal address dependening on the actual scope
    def AssignMemoryAddress(self, tipo, scope, location):
        address = -1
        i = 0
        N = 1
        if scope == 'GLOBAL':
            if location != 'TEMPORAL':
                if tipo == 'int':
                    i = 0
                    address = Dir.INT_GLOBAL + self.last[i]
                elif tipo == 'float':
                    i = 1
                    address = Dir.FLOAT_GLOBAL + self.last[i]
                elif tipo == 'bool':
                    i = 2
                    address = Dir.BOOL_GLOBAL + self.last[i]
                elif tipo == 'list_int':
                    i = 3
                    address = Dir.LIST_INT_GLOBAL + self.last[i]
                    N = 100
                elif tipo == 'list_float':
                    i = 4
                    address = Dir.LIST_FLOAT_GLOBAL + self.last[i]
                    N = 100
                elif tipo == 'list_bool':
                    i = 5
                    address = Dir.LIST_BOOL_GLOBAL + self.last[i]
                    N = 100
            else:
                if tipo == 'int':
                    i = 6
                    address = Dir.INT_GLOBAL_TEMPORAL + self.last[i]
                elif tipo == 'float':
                    i = 7
                    address = Dir.FLOAT_GLOBAL_TEMPORAL + self.last[i]
                elif tipo == 'bool':
                    i = 8
                    address = Dir.BOOL_GLOBAL_TEMPORAL + self.last[i]
                elif tipo == 'list_int':
                    i = 9
                    address = Dir.LIST_INT_GLOBAL_TEMPORAL + self.last[i]
                    N = 100
                elif tipo == 'list_float':
                    i = 10
                    address = Dir.LIST_FLOAT_GLOBAL_TEMPORAL + self.last[i]
                    N = 100
                elif tipo == 'list_bool':
                    i = 11
                    address = Dir.LIST_BOOL_GLOBAL_TEMPORAL + self.last[i]
                    N = 100
        else:
            if location != 'TEMPORAL':
                if tipo == 'int':
                    i = 12
                    address = Dir.INT_LOCAL + self.last[i]
                elif tipo == 'float':
                    i = 13
                    address = Dir.FLOAT_LOCAL + self.last[i]
                elif tipo == 'bool':
                    i = 14
                    address = Dir.BOOL_LOCAL + self.last[i]
                elif tipo == 'list_int':
                    i = 15
                    address = Dir.LIST_INT_LOCAL + self.last[i]
                    N = 100
                elif tipo == 'list_float':
                    i = 16
                    address = Dir.LIST_FLOAT_LOCAL + self.last[i]
                    N = 100
                elif tipo == 'list_bool':
                    i = 17
                    address = Dir.LIST_BOOL_LOCAL + self[i]
                    N = 100     
            else:
                if tipo == 'int':
                    i = 18
                    address = Dir.INT_LOCAL_TEMPORAL + self.last[i]
                elif tipo == 'float':
                    i = 19
                    address = Dir.FLOAT_LOCAL_TEMPORAL + self.last[i]
                elif tipo == 'bool':
                    i = 20
                    address = Dir.BOOL_LOCAL_TEMPORAL + self.last[i]
                elif tipo == 'list_int':
                    i = 21
                    address = Dir.LIST_INT_LOCAL_TEMPORAL + self.last[i]
                    N = 100
                elif tipo == 'list_float':
                    i = 22
                    address = Dir.LIST_FLOAT_LOCAL_TEMPORAL + self.last[i]
                    N = 100
                elif tipo == 'list_bool':
                    i = 23
                    address = Dir.LIST_BOOL_LOCAL_TEMPORAL + self[i]
                    N = 100    
        
        self.last[i] = self.last[i] + N               
        return address
        
        #function to reset the local memory
        #use when trying to reset the memory assing to a function which is temporal
    def ResetLocalMemory(self):
        for x in range(12, 23):
            self.last[x] = 0
       











