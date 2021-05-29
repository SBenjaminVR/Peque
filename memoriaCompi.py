
class MemoriaCompi:
    #----------------Direciones De Memoria -----------------#
    intGT =  0
    floatGT = 1000
    charGT = 2000
    boolGT =  3000

    intG = 4000
    floatG = 5000
    charG =  6000
    boolG = 7000

    intL =  8000
    floatL = 90000
    charL =  10000
    boolL = 11000

    intLT = 12000
    floatLT = 13000
    charLT = 14000
    boolLT = 15000
#-------------------------------------------------------#

    last = []
    def __init__(self):
        self.last = [0]*16
   
    def addMemory(self,tipo,Scope,temp):
        answ = -1
        if tipo == 'int':
            if Scope == 'G':
                if temp == 'N':
                    self.last[0] = self.last[0] + 1
                    answ = self.intG + self.last[0]
                elif temp == 'T':
                    self.last[1] = self.last[1] + 1
                    answ = self.intGT + self.last[1]
            elif Scope == 'L':
                if temp == 'N':
                    self.last[2] = self.last[2] + 1
                    answ = self.intL + self.last[2] 
                elif temp == 'T':
                    self.last[3] = self.last[3] + 1
                    answ = self.intLT + self.last[3]
        elif tipo == 'float':
            if Scope == 'G':
                if temp == 'N':
                    self.last[4] = self.last[4] + 1
                    answ = self.floatG + self.last[4]
                elif temp == 'T':
                    self.last[5] = self.last[5] + 1
                    answ = self.floatGT + self.last[5]
            elif Scope == 'L':
                if temp == 'N':
                    self.last[6] = self.last[6] + 1
                    answ = self.floatL + self.last[6]
                elif temp == 'T':
                    self.last[7] = self.last[7] + 1
                    answ = self.floatLT + self.last[7]
        elif tipo == 'bool':
            if Scope == 'G':
                    if temp == 'N':
                        self.last[8] = self.last[8] + 1
                        answ = self.boolG + self.last[8]
                    elif temp == 'T':
                        self.last[9] = self.last[9] + 1
                        answ = self.boolGT + self.last[9]
            elif Scope == 'L':
                    if temp == 'N':
                        self.last[10] = self.last[10] + 1
                        answ = self.boolL + self.last[10]
                    elif temp == 'T':
                        self.last[11] = self.last[11] + 1
                        answ = self.boolLT + self.last[11]
        elif tipo == 'char':
                if Scope == 'G':
                    if temp == 'N':
                        self.last[12] = self.last[12] + 1
                        answ = self.charG + self.last[12]
                    elif temp == 'T':
                        self.last[13] = self.last[13] + 1
                        answ = self.charGT + self.last[13]
                elif Scope == 'L':
                    if temp == 'N':
                        self.last[14] = self.last[14] + 1
                        answ = self.charL + self.last[14]
                    elif temp == 'T':
                        self.last[15] = self.last[15] + 1
                        answ = self.charLT + self.last[15]
        return answ - 1
    def printMemoria(self):
        print(self.last)
    def resetearMemoriaLocal(self):
        self.Last[2] = 0
        self.Last[3] = 0
        self.Last[6] = 0
        self.Last[7] = 0
        self.Last[10] = 0
        self.Last[11] = 0
        self.Last[14] = 0
        self.Last[15] = 0











