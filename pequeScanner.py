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

# lectura de archivo
from pathlib import Path
from parserYacc import tipos, popper, values, Cuartetos, Temporales, tabla, constantes
import virtualMachine as mv

fileData = Path('prueba1.pq').read_text()
resultado = py.parser.parse(fileData)
print(resultado)
print(tabla.Variables)
print(tabla.Funciones)
popper.printStack()
tipos.printStack()
print(Cuartetos)
print(Temporales)
