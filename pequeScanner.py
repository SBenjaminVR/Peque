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
from parserYacc import Cuartetos, Temporales, Tabla, Constantes, popper, tipos
import virtualMachine as mv

fileData = Path('prueba.pq').read_text()
resultado = py.parser.parse(fileData)
print(resultado)
print('----------------Variables--------------')

print(Tabla.Variables)
print('----------------Funciones--------------')

print(Tabla.Funciones)
print('-----------------Clases--------------')
print(Tabla.Clases)
print('----------------Popper--------------')
popper.printStack()
print('----------------Tipos--------------')
tipos.printStack()
print('----------------Temporales--------------')
print(Temporales)
print('----------------Cuartetos--------------')
print(Cuartetos)
