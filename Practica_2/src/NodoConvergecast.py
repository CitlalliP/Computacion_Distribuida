import simpy
from Nodo import *
from Canales.CanalBroadcast import *
from Auxiliares import *
#from NodoGenerador import NodoGenerador


TICK = 1
class NodoConvergcast(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de convergcast.'''
    def __init__(self, id_nodo,vecinos,valor, canal_entrada, canal_salida, mensaje=None):
            self.id_nodo = id_nodo
            self.padre = None
            self.vecinos = vecinos
            self.canal_entrada = canal_entrada
            self.canal_salida = canal_salida
            self.mensaje = mensaje
            self.value =  valor #self.id_nodo #Como ejemplo para los test diremos que los valores recolectados seran los ids , no usamos un conjunto pues no sabemos que se vaya ahacer (la funcion f)
            #self.val_set = [self.value] Situacional
            self.val_set = {self.value}
            self.funcion = None 
            self.valor_final = None

    def toString(self):
        return f"Nodo : {self.id_nodo},valor: {self.value}, valores: {self.val_set}"

    def convergecast(self,env,f):

#       '''Implementar'''





