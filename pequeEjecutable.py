import sys
import parserYacc as py
from pathlib import Path        # Read files

def main(argv):
    fileData = Path(argv[1]).read_text()
    ParserLexer = py.parser.parse(fileData)
    print(ParserLexer)

if __name__ == '__main__':
    main(sys.argv)