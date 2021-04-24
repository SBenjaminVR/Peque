
from stack import Stack

inputString = '(1+2*3+3) - 3 > 4'
popper = Stack()
tipos = Stack()
pilaO = Stack()

for item in inputString:
    if item == '+' or item =='-' or item == '*' or item == '/' or item == '>':
        popper.push(item)
    
    else:
        tipos.push('int')
        if item != '(' or item != ')':
            pilaO.push(int(item))
        else
popper.printStack()
tipos.printStack()
pilaO.printStack()
    
