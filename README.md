# Peque
Programming language made for the compilers course
# AUTORES
# Benjamín Valdez Rodríguez A00822027
# Juan Carlos Garza Lopez A00822601

--------AVANZE DEL LEXICO SINTACTICO 4/9/2021--------
Se utilizo python con Yacc y Lex
 
Se completaron las RE y los tokens de los diagramas entregados con este avanze, 
sin embargo para este avanze dejamos unos pendientes por realizar:

* Pendiente por implementar fila
* Funciones_Esp aun no esta implementado
* Pendiente corregir la declaración de variables para tipos de retorno normales.

Lo demas esta implementado en el Lexico-Sintactico

Se anexa una prueba para que puedar ser probado con exito

Como compilar: 
se necesita tener lar librerias
* yacc
* lex

--------DIRECTORIO DE FUNCIONES Y TABLAS DE VARIABLES 04/15/2021--------
Se hizo un directorio de funciones que guarda el nombre de la funcion y el tipo de retorno de esta, sin embargo tiene un pequeño bug en donde si la declaración de la funcion tiene parametros, el directorio no detecta bien el tipo de retorno. 
También se hizo la implementación de una tabla de variables que guarda el id de las variables globales asi como su tipo de dato. Finalmente se realizó el diseño de la tabla de consideraciones semanticas en un archivo de excel.

Queda pendiente por implementar las tabla de variables de las funciones y el tipo de retorno bool.

--------Cubo Semantico y codigo intermedio 04/23/2021--------
Se realizo la tabla de consideraciones semanticas, el cual pasamos a un cubo semantico que usamos para poder realizar el codigo intermedio y poder resolver las expresiones utilizando los algoritmos vistos en clase, a su vez, preparamos el primer paso para que nuestro compilador produzca el codigo intermedio completo.


## IMPORTANTE ##
 comando para ejectura
python pequeScanner.py

## Importante ## 
leéra el archivo "prueba.txt" solamente