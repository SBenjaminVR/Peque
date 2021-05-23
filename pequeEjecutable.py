import sys
import parserYacc as py
from pathlib import Path        # Read files
from virtualMachine import VirtualMachine

data = []

def main(argv):
    fileData = Path(argv[1]).read_text()
    ParserLexer = py.parser.parse(fileData)
    print(ParserLexer)
    vm = VirtualMachine(data)
    vm.run()
    
if __name__ == '__main__':
    main(sys.argv)