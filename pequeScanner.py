#--------------------------------------- Autores---------------------------------------
# Benjamín Valdez Rodríguez A00822027
#Juan Carlos Garza Lopez A00822601

#ITESM
#--------------------------------------- Autores---------------------------------------
import ply.lex as lex           # Scanner
import ply.yacc as yacc         # Parser
from pathlib import Path        # Read files
import sys


#local modules
import parserYacc as py



parser = py.parser

#--------------------------------------- funciones de prueba---------------------------------------

def prueba(data):
  result = parser.parse(data)
  print(result)


# lectura de archivo
from pathlib import Path

aceptado = Path('prueba.txt').read_text()
aceptado = aceptado
prueba(aceptado)
