import simpy
from Nodo import *
from Canales.CanalBroadcast import * ##Mayusculas 


class NodoVecinos(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de conocer a los
        vecinos de tus vecinos.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.identifiers = set()
    
    def tostring(self):
        """Regresa la representacion en cadena del nodo."""
        return f"Nodo: {self.id_nodo}, vecinos: {self.vecinos},identificadores: {self.identifiers}"

    def conoceVecinos(self, env):
        ''' Algoritmo que hace que el nodo conozca a los vecinos de sus vecinos.
            Lo guarda en la variable identifiers.'''
     
