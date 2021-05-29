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
    fileData = Path(argv[1]).read_text()
    ParserLexer = py.parser.parse(fileData)
    print(ParserLexer)
    vm = VirtualMachine(data)
    vm.run()
    
if __name__ == '__main__':
    main(sys.argv)