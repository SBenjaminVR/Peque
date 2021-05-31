class TablaOperaciones:
    def __init__(self):
        self.Tabla = {
            "+": 1,
            "-": 2,
            "*": 3,
            "/": 4,
            "=": 5,
            ">": 6,
            "<": 7,
            ">=": 8,
            "<=": 9,
            "==": 10,
            "<>": 11,
            "&&": 12,
            "||": 13,
            "GOTO": 14,
            "GOTOF": 15,
            "ERA": 16,
            "GOSUB": 17,
            "PARAMETRO": 18,
            "RETURN": 19,
            "END PROC": 20,
            "VER": 21,
            "PRINT": 22,
            "INPUT": 23,
            "END": 24,
            "START PROC" : 26
        }

    def GetNumber(self, Operation):
        Operation = str(Operation)
        return self.Tabla.get(Operation)
        
          

    