#--------------------------------------- Autores---------------------------------------
# Benjamín Valdez Rodríguez A00822027
#Juan Carlos Garza Lopez A00822601

#ITESM
#--------------------------------------- Autores---------------------------------------
import ply.lex as lex           # Scanner
import ply.yacc as yacc         # Parser
from pathlib import Path        # Read files
import sys


#--------------------------------------- Adding the parser ---------------------------------------

#local modules
import parserYacc as py

#--------------------------------------- Testing the parser ---------------------------------------

# lectura de archivo
from pathlib import Path

fileData = Path('prueba.txt').read_text()
resultado = py.parser.parse(fileData)
print(resultado)
