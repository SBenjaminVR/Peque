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
from parserYacc import tipos, popper, values, Cuartetos, Temporales, symb
import maquinaVirtual as mv

fileData = Path('prueba.txt').read_text()
resultado = py.parser.parse(fileData)
print(resultado)
popper.printStack()
#print(popper.length())
values.printStack()
#print(values.length())
tipos.printStack()
#print(tipos.length())
print(Cuartetos)
print(Temporales)

#Memoria de las variables
#print(symb.Directory.get('Variables')) #Imprimir Variables
for item, val in symb.Directory.get('Variables').items():
    mv.AsignarMemoriaGlobal(val.get('EspacioMemoria'))

print(mv.memoriaVirtual.ds)