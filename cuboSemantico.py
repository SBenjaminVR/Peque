'''
Implementacion de cubo semantico


'''
cuboSemantico = {
    'int' : {
        'int' : {
            '+' : 'int',
            '-' : 'int',
            '*' : 'int',
            '/' : 'int',
            'comp' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'float' : {
            '+' : 'float',
            '-' : 'float',
            '*' : 'float',
            '/' : 'float',
            'comp' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'char' : {
            '+' : 'int',
            '-' : 'int',
            '*' : 'int',
            '/' : 'int',
            'comp' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },'fila' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            'comp' : 'err',
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
            'comp' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'float' : {
            '+' : 'float',
            '-' : 'float',
            '*' : 'float',
            '/' : 'float',
            'comp' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'char' : {
            '+' : 'float',
            '-' : 'float',
            '*' : 'float',
            '/' : 'float',
            'comp' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },'fila' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            'comp' : 'err',
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
            'comp' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'float' : {
            '+' : 'float',
            '-' : 'float',
            '*' : 'float',
            '/' : 'float',
            'comp' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },
        'char' : {
            '+' : 'int',
            '-' : 'int',
            '*' : 'int',
            '/' : 'int',
            'comp' : 'bool',
            '||' : 'bool',
            '&&' : 'bool',
        },'fila' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            'comp' : 'err',
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
            'comp' : 'err',
            '||' : 'err',
            '&&' : 'err',
        },
        'float' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            'comp' : 'err',
            '||' : 'err',
            '&&' : 'err',
        },
        'char' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            'comp' : 'err',
            '||' : 'err',
            '&&' : 'err',
        },'fila' : {
            '+' : 'err',
            '-' : 'err',
            '*' : 'err',
            '/' : 'err',
            'comp' : 'err',
            '||' : 'err',
            '&&' : 'err',
        }
    }
}

