# Peque
Lenguaje de programación orientado a objetos realizado para la clase de Compiladores.


**AUTORES**  
**Benjamín Valdez Rodríguez A00822027**  
**Juan Carlos Garza Lopez A00822601**

### Instrucciones para correr
* Tener instalado python 3
* Ejecutar el comando "pip install -r requirements.txt"
* Correr pequeEjecutable.py TuArchivo.pq

### Estructura basica de un programa
Todo programa debe tener *programa* al inicio, seguido del *nombre del programa;*  
También es indispensable tener un *main()* en el programa ya que la ejecución del mismo comenzara a partir de esa sección.  

*Ejemplo:*
```python
programa NombreDelPrograma;

main() {
   
}

```
### Variables
#### Declaración
Para declarar una variable es necesario escribir *petite* despues el *tipo de dato* que se espera y posteriormente el *nombre* que se le quiere dar a la variable. Se puede declarar mas de una funcion en una linea, separando cada nombre con una coma.  

Tipos de datos aceptables:
* int
* float
* bool
* list *(Mas informacion en su respectiva seccion)*  

*Ejemplo:*
```python
petite int mascaras
petite float barcos
petite bool bosques, mares
petite list lista
```

#### Asignación
Para asignarle un valor a una variable es necesario escribir el *nombre* de la variable, seguido del simbolo **=** y el *valor* que se le quiere dar. 

*Ejemplo:*
```python
mascaras = 3
barcos = 2 + 6 * 3.4 / 2.1
mares = mascaras < barcos
mares = barcos
```
### Expresiones aritmeticas y de comparación
#### Aritmeticas
Las expresiones aritmeticas que acepta el lenguaje son las de suma, resta, multiplicación y división.

*Ejemplo:*
```python
a = 1 + 3
a = b - c
a = 3 * 4
a = 10 / 2
```
#### Comparación
Los comparadores que acepta son el de "menor que", "menor o igual que", "mayor que", "mayor o igual que", "igual que" y "diferente que".  
*Ejemplo:*
```python
a = 1 < 3   # Menor que
a = b <= c  # Menor o igual que
a = 3 > 4   # Mayor que
a = i >= b  # Mayor o igual que
a = 2 == 0  # Igual que
a = i <> k  # Diferente que
```

### Condicionales
#### if
Para hacer una condicional es necesatio escribir *if (condicion) { estatutos }* donde en caso de que la condicion sea verdadera, se ejecutaran los estatutos que se pusieron adentro de las llaves.  
*Ejemplo:*
```python
if (a < 3) {
   # Estatutos
}
```
#### if...else...
Se sigue la misma estructura basica del if pero se agregar un *else { estatutos }* , en donde van los estatutos que se quieren ejecutar si no se cumple la condicion original.   
*Ejemplo:*
```python
if (a < 3) {
   # Estatutos
} else {
   # Estatutos
}
```
### Ciclos
#### while
Para hacer un estatuto de repetición es necesario escribir *while (condicion) { estatutos }* donde mientras la condicion sea verdadera, se ejecutaran los estatutos en el interior una y otra vez.  
**Advertencia: Ninguna variable aumenta automaticamente, asi que es tu responsabilidad aumentar variables para romper el ciclo.**  

*Ejemplo:*
```python
while (i < 3) {
   # Estatutos
   i = i + 1
}
```

#### for
Para hacer un estatuto de repetición es necesario escribir *for (inicio to fin, salto) { estatutos }* donde los estatutos se ejecutaran la cantidad de veces que de la diferencia entre fin e inicio, haciendo saltos de lo declarado en salto.  
```python
for (0 to 4, 1) {
   # Estatutos
}
```

### Funciones
Para declarar una funcion es necesario declarar escribir *mini tipo nombre(parametros) { estatutos return}* donde los tipos que regrese la función pueden ser int, float, bool o void (nada). Puede o no llevar parametros de tipo int, float o bool. Al final se debe terminar con un return que de el valor de retorno.  
**OJO: Si la funcion es de tipo void, no debe llevar un return**  
*Ejemplo:*
```python
mini int fibonacci(int n) {
   # Estatutos
   
   return n
}

mini void titulos() {
   # Estatutos
   
}
```

### Clases
#### Declaracion
Para declarar una clase simplemente hay que escribir *peque nombre { }* donde nombre es el nombre que le quieres dar a tu clase.  

*Ejemplo:*
```python
peque animal {
   # Atributos
   # Funciones
}
```

#### Herencia
Para que una clase tenga herencia de otra (hereda todos los métodos y atributos de su clase padre), hay que agregar la palabra *agranda* seguido del *nombre* de la clase padre despues de la declaracion normal de la clase.  
*Ejemplo:*
```python
peque canino agranda animal {
   # Atributos
   # Funciones
}
```

#### Objetos
Para hacer un objeto hay que poner *nombre = new clase* donde nombre es el nombre que le queremos dar al objeto y clase como indica su nombre es de la clase a la que va a pertenecer el objeto.  
*Ejemplo:*
```python
camaleon = new animal
ruffo = new canino
```

#### Acceder a atributos de un objeto
Simplemente hay que poner un *objeto.nombre* donde objeto es el nombre del objeto y nombre es el atributo al que le queremos dar valor dentro de la clase. (Adentro de una funcion de la clase puedes usar el atributo sin necesidad de escribir el nombre del objeto.  
*Ejemplo:*
```python
perro.nombre = 2
perro.clasificacion = 3

mini int algo() {
   return atributo
}
```

#### Acceder a funciones de un objeto
Para acceder a las funciones de un objeto es necesario poner *objeto.funcion()* donde objeto es el nombre del objeto y funcion es el nombre de la funcion adentro de la clase que se quiera llamar. Deben ir parentesis al final donde deben ir los parametros (si tiene) de la función.  
*Ejemplo:*
```python
perro.suma()
perro.resta(48.1329)
```

### Listas
#### Declaracion
Para declarar una lista es necesario escribir *petite* *list* *tipo* seguido del *nombre* que se le quiere asignar a la lista. Los tipos de datos que acepta la lista son los de int, float, y bool.  

*Ejemplo:*
```python
petite list int primeraLista
petite list float segundaLista
petite list bool terceraLista
```
#### Append
Para agregar un elemento a lista es necesario poner *nombre->append(elemento)*  
*Ejemplo:*
```python
primeraLista->append(3)
primeraLista->append(5)
primeraLista->append(7)
```
#### Pop
Para quitar un elemento a lista es necesario poner *nombre->append(elemento)*  
*Ejemplo:*
```python
primeraLista->pop()
```
#### Head
Para obtener el ultimo elemento a lista es necesario poner *nombre->head()*  
*Ejemplo:*
```python
primeraLista->head()
```
#### Tail
Para obtener el primer elemento a lista es necesario poner *nombre->head()*  
*Ejemplo:*
```python
primeraLista->tail()
```
#### Key
Para obtener el elemento que se encuentre en la posición *x* de la lista es necesario poner *nombre->key(x)*  
*Ejemplo:*
```python
primeraLista->key(2)
```
#### Find
Para obtener en que posición se encuentra el elemento *x* de la lista es necesario poner *nombre->find(x)*  
*Ejemplo:*
```python
primeraLista->find(5)
```
#### Sort
Para ordenar los elementos de la lista de forma ascendente es necesario poner *nombre->sort()*  
*Ejemplo:*
```python
primeraLista->sort()
```
