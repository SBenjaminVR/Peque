import sys
import parserYacc as py
from pathlib import Path                             # Lectura Archivos
from virtualMachine import VirtualMachine
from parserYacc import Cuartetos, Tabla, Constantes

Data = {
    'Cuadruplos': Cuartetos,
    'Constantes': Constantes,
    'Directorio': Tabla
}

def main(argv):
    if checkIfFileIsDOTPQ(argv[1]):
        # Parser and lexer
        fileData = Path(argv[1]).read_text()
        py.parser.parse(fileData)
        # "Starts to run the virtual machine"
        vm = VirtualMachine(Data)
        vm.run()
    else:
        print('El archivo no tiene una extension .pq')
    
# Checks if the file has ".pq" extension
def checkIfFileIsDOTPQ(file):
    extension = file[-3:]
    return extension == '.pq'


if __name__ == '__main__':
    main(sys.argv)