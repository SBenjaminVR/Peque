import ply.lex as lex           # Scanner
import ply.yacc as yacc         # Parser
from pathlib import Path        # Read files
import sys

#tokens reservados o palabras reservadas
reserved = {
    'programa': 'PROGRAMA',
    'escribe': 'ESCRIBE',
    'variable': 'VARIABLE',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'void' : 'VOID'
    'if': 'IF',
    'else': 'ELSE'
    'mini' : 'MINI',
    'agranda': 'AGRANDA',
    'peque': 'PEQUE',
    'regreso':'REGRESO',
    'lee' : 'LEE',
    'for':'FOR',
    'while' : 'WHILE'
}

tokens = [
    'ID',
    'CTEI', 'CTEF', 'CTEC',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'DOTS', 'EQUALS', 'SEMICOLON', 'PERIOD', 'COMMA',
    'LESS', 'BIGGER', 'DIFFERENT','EQUAL','BIGGER_EQUAL', 'LESS_EQUAL'
    'L_PARENTHESIS', 'R_PARENTHESIS', 'L_BRACKET', 'R_BRACKET',
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_DOTS = r'\:'
t_EQUALS = r'\='
t_SEMICOLON = r'\;'
t_PERIOD = r'\.'
t_COMMA = r'\,'
t_LESS = r'\<'
t_BIGGER = r'\>'
t_DIFFERENT = r'\<\>'
t_EQUAL = r'\=\='
t_BIGGER_EQUAL = r'\>\='
t_LESS_EQUAL = r'\<\='
t_L_PARENTHESIS = r'\('
t_R_PARENTHESIS = r'\)'
t_L_BRACKET = r'\{'
t_R_BRACKET = r'\}'

# Caracteres ignorados (Espacios y tabs)
t_ignore = ' \t'
#ignore newlines
def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
#id regular expresion
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t
 #error 
 def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)
