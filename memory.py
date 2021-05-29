class Memory:
    def __init__(self, data):
        self.memory = [None]*30000
        self.quadruples = data.get('Cuadruplos')
        self.directory = data.get('Directorio')

    def getValue(self, address):
        print(address)
