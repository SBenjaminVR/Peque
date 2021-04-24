'''
Implementacion de cubo semantico

utilizamos un dictionario anidado, ya que en python tiene una complejidad constante el utilizar este tipo de estructura
'''
cuboSemantico = {
    'int' : {
        'int' : {
            '+' : 'int',
            '-' : 'int',
            '*' : 'int',
            '/' : 'int',
            '>' : 'bool',
            '>=' : 'bool',
            '<' : 'bool',
            '<=' : 'bool',
            '==' : 'bool',
            '!=' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'float' : {
            '+' : 'float',
            '-' : 'float',
            '*' : 'float',
            '/' : 'float',
            '>' : 'bool',
            '>=' : 'bool',
            '<' : 'bool',
            '<=' : 'bool',
            '==' : 'bool',
            '!=' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'char' : {
            '+' : 'int',
            '-' : 'int',
            '*' : 'int',
            '/' : 'int',
            '>' : 'bool',
            '>=' : 'bool',
            '<' : 'bool',
            '<=' : 'bool',
            '==' : 'bool',
            '!=' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },'fila' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            '>' : 'err',
            '>=' : 'err',
            '<' : 'err',
            '<=' : 'err',
            '==' : 'err',
            '!=' : 'err',
            '||' : 'err',
            '&&' : 'err',
        }
    },
    'float' : {
        'int' : {
            '+' : 'float',
            '-' : 'float',
            '*' : 'float',
            '/' : 'float',
            '>' : 'bool',
            '>=' : 'bool',
            '<' : 'bool',
            '<=' : 'bool',
            '==' : 'bool',
            '!=' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'float' : {
            '+' : 'float',
            '-' : 'float',
            '*' : 'float',
            '/' : 'float',
            '>' : 'bool',
            '>=' : 'bool',
            '<' : 'bool',
            '<=' : 'bool',
            '==' : 'bool',
            '!=' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'char' : {
            '+' : 'float',
            '-' : 'float',
            '*' : 'float',
            '/' : 'float',
            '>' : 'bool',
            '>=' : 'bool',
            '<' : 'bool',
            '<=' : 'bool',
            '==' : 'bool',
            '!=' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },'fila' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            '>' : 'err',
            '>=' : 'err',
            '<' : 'err',
            '<=' : 'err',
            '==' : 'err',
            '!=' : 'err',
            '||' : 'err',
            '&&' : 'err',
        }
    },
    'char' : {
        'int' : {
            '+' : 'int',
            '-' : 'int',
            '*' : 'int',
            '/' : 'int',
            '>' : 'bool',
            '>=' : 'bool',
            '<' : 'bool',
            '<=' : 'bool',
            '==' : 'bool',
            '!=' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'float' : {
            '+' : 'float',
            '-' : 'float',
            '*' : 'float',
            '/' : 'float',
            '>' : 'bool',
            '>=' : 'bool',
            '<' : 'bool',
            '<=' : 'bool',
            '==' : 'bool',
            '!=' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'char' : {
            '+' : 'int',
            '-' : 'int',
            '*' : 'int',
            '/' : 'int',
            '>' : 'bool',
            '>=' : 'bool',
            '<' : 'bool',
            '<=' : 'bool',
            '==' : 'bool',
            '!=' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },'fila' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            '>' : 'err',
            '>=' : 'err',
            '<' : 'err',
            '<=' : 'err',
            '==' : 'err',
            '!=' : 'err',
            '||' : 'err',
            '&&' : 'err',
        }
    },
    'fila' : {
        'int' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            '>' : 'err',
            '>=' : 'err',
            '<' : 'err',
            '<=' : 'err',
            '==' : 'err',
            '!=' : 'err',
            '||' : 'err',
            '&&' : 'err',
        },
        'float' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            '>' : 'err',
            '>=' : 'err',
            '<' : 'err',
            '<=' : 'err',
            '==' : 'err',
            '!=' : 'err',
            '||' : 'err',
            '&&' : 'err',
        },
        'char' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            '>' : 'err',
            '>=' : 'err',
            '<' : 'err',
            '<=' : 'err',
            '==' : 'err',
            '!=' : 'err',
            '||' : 'err',
            '&&' : 'err',
        },'fila' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            '>' : 'err',
            '>=' : 'err',
            '<' : 'err',
            '<=' : 'err',
            '==' : 'err',
            '!=' : 'err',
            '||' : 'err',
            '&&' : 'err',
        }
    }
}

