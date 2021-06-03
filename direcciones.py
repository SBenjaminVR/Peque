#Base address of all the variables
#you can manually asssing where all the memory start
# you need to make sure to leave a space between address

class DireccionesMemoria:
    def __init__(self):
        self.INT_GLOBAL = 0
        self.FLOAT_GLOBAL = 1000
        self.BOOL_GLOBAL = 2000
        self.LIST_INT_GLOBAL = 3000 
        self.LIST_FLOAT_GLOBAL = 4000
        self.LIST_BOOL_GLOBAL = 5000
    
        self.INT_GLOBAL_TEMPORAL =  6000
        self.FLOAT_GLOBAL_TEMPORAL = 7000
        self.BOOL_GLOBAL_TEMPORAL =  8000
        self.LIST_INT_GLOBAL_TEMPORAL = 9000 
        self.LIST_FLOAT_GLOBAL_TEMPORAL = 10000
        self.LIST_BOOL_GLOBAL_TEMPORAL = 11000

        self.INT_LOCAL =  12000
        self.FLOAT_LOCAL = 13000
        self.BOOL_LOCAL = 14000
        self.LIST_INT_LOCAL = 15000 
        self.LIST_FLOAT_LOCAL = 16000
        self.LIST_BOOL_LOCAL = 17000

        self.INT_LOCAL_TEMPORAL = 18000
        self.FLOAT_LOCAL_TEMPORAL = 19000
        self.BOOL_LOCAL_TEMPORAL = 20000
        
        self.INT_CONSTANTE = 25000
        self.FLOAT_CONSTANTE = 26000
        self.BOOL_CONSTANTE = 27000
        self.STRING_CONSTANTE =  28000

        self.OBJETOS = 30000