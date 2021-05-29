
class AsignadorMemoria:
    #----------------Direciones De Memoria -----------------#
    INT_GLOBAL = 0
    FLOAT_GLOBAL = 1000
    CHAR_GLOBAL =  2000
    BOOL_GLOBAL = 3000
    
    INT_GLOBAL_TEMPORAL =  4000
    FLOAT_GLOBAL_TEMPORAL = 5000
    CHAR_GLOBAL_TEMPORAL = 6000
    BOOL_GLOBAL_TEMPORAL =  7000

    INT_LOCAL =  8000
    FLOAT_LOCAL = 90000
    CHAR_LOCAL =  10000
    BOOL_LOCAL = 11000

    INT_LOCAL_TEMPORAL = 12000
    FLOAT_LOCAL_TEMPORAL = 13000
    CHAR_LOCAL_TEMPORAL = 14000
    BOOL_LOCAL_TEMPORAL = 15000
#-------------------------------------------------------#

    last = []
    def __init__(self):
        self.last = [0]*16
   
    def AssignMemoryAddress(self, tipo, scope, location):
        address = -1
        if scope == 'GLOBAL':
            if location != 'TEMPORAL':
                if tipo == 'int':
                    address = self.INT_GLOBAL + self.last[0]
                    self.last[0] = self.last[0] + 1
                elif tipo == 'float':
                    address = self.FLOAT_GLOBAL + self.last[1]
                    self.last[1] = self.last[1] + 1
                elif tipo == 'char':
                    address = self.CHAR_GLOBAL + self.last[2]
                    self.last[2] = self.last[2] + 1
                elif tipo == 'bool':
                    address = self.BOOL_GLOBAL + self.last[3]
                    self.last[3] = self.last[3] + 1
            else:
                if tipo == 'int':
                    address = self.INT_GLOBAL_TEMPORAL + self.last[4]
                    self.last[4] = self.last[4] + 1
                elif tipo == 'float':
                    address = self.FLOAT_GLOBAL_TEMPORAL + self.last[5]
                    self.last[5] = self.last[5] + 1
                elif tipo == 'char':
                    address = self.CHAR_GLOBAL_TEMPORAL + self.last[6]
                    self.last[6] = self.last[6] + 1
                elif tipo == 'bool':
                    address = self.BOOL_GLOBAL_TEMPORAL + self.last[7]
                    self.last[7] = self.last[7] + 1
        else:
            if location != 'TEMPORAL':
                if tipo == 'int':
                    address = self.INT_LOCAL + self.last[8]
                    self.last[8] = self.last[8] + 1
                elif tipo == 'float':
                    address = self.FLOAT_LOCAL + self.last[9]
                    self.last[9] = self.last[9] + 1
                elif tipo == 'char':
                    address = self.CHAR_LOCAL + self.last[10]
                    self.last[10] = self.last[10] + 1
                elif tipo == 'bool':
                    address = self.BOOL_LOCAL + self.last[11]
                    self.last[11] = self.last[11] + 1
            else:
                if tipo == 'int':
                    address = self.INT_LOCAL_TEMPORAL + self.last[12]
                    self.last[12] = self.last[12] + 1
                elif tipo == 'float':
                    address = self.FLOAT_LOCAL_TEMPORAL + self.last[13]
                    self.last[13] = self.last[5] + 1
                elif tipo == 'char':
                    address = self.CHAR_LOCAL_TEMPORAL + self.last[14]
                    self.last[14] = self.last[6] + 1
                elif tipo == 'bool':
                    address = self.BOOL_LOCAL_TEMPORAL + self.last[15]
                    self.last[15] = self.last[7] + 1                
        return address
        
    def ResetLocalMemory(self):
        for x in range(8, 15):
            self.last[x] = 0
       











