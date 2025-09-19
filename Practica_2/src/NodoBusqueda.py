import simpy
from Nodo import *
from Canales.CanalBroadcast import *
from Auxiliares import *

TICK = 1
class NodoBusqueda(Nodo):
    def __init__(self, id_nodo,vecinos,cantidad_nodos ,canal_entrada, canal_salida,mensaje=None):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.cantidad_nodos =  cantidad_nodos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.arr = []
        self.contenido = False 
    

    def toString(self):
        return f"Id_nodo = {self.id_nodo},Vecinos: {self.vecinos},array: {self.arr},estado: {self.contenido}"

    def busqueda(self,env,arr,elemento):
        '''Implementar'''



                    
                     







    
        

    
