class Memory:
    INT = 0
    FLOAT = 500
    BOOLEAN = 1000
    CHAR = 1500
    ARR = 2000
    def __init__(self):
        self.memory = [None]*5000
    def getValue(self, type, address) {
        if type == "Int":
            return self.memory[self.INT + address]
        elif type == "Float":
            return self.memory[self.FLOAT + address]
        elif type == "Bool":
            return self.memory[self.BOOLEAN + address]
        elif type == "Char":
            return self.memory[self.CHAR + address]
        elif type == "Arr":
            return self.memory[self.ARR + address]
    }
    def addValueToMemory(self, value, type, address) {
        if type == "Int":
            self.memory[self.INT + address] = value
        elif type == "Float":
            self.memory[self.FLOAT + address] = value
        elif type == "Bool":
            self.memory[self.BOOLEAN + address] = value
        elif type == "Char":
            self.memory[self.CHAR + address] = value
        elif type == "Arr":
            self.memory[self.ARR + address] = value
    }
