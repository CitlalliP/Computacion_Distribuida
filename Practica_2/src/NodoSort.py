import simpy
from Nodo import *
from Canales.CanalBroadcast import *
from Auxiliares import *



class NodoSort(Nodo):
    def __init__(self, id_nodo,vecinos,cantidad_nodos,canal_entrada, canal_salida,mensaje=None):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.cantidad_nodos =  cantidad_nodos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.arr = []

    def ordernar(self,env,arr):
        '''Implementar'''


    


        






