import simpy
from Nodo import *
from Canales.CanalBroadcast import *

TICK = 1
GO_MSG = "GO"
BACK_MSG = "BACK"

class NodoGenerador(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de flooding.'''
    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        
        # Atributos propios del algoritmo
        #self.padre = None if id_nodo != 0 else id_nodo # Si es el nodo distinguido, el padre es el mismo 
        self.padre = None
        self.hijos = list()
        self.mensajes_esperados = len(vecinos) # Cantidad de mensajes que esperamo
        

    def tostring(self):
        return f"ID: {self.id_nodo}, Parent: {self.padre}, Children: {self.hijos}"

    
    def genera_arbol(self, env):
        """Implementación corregida y robusta del algoritmo GO/BACK.
        Asume que canal_entrada.get() retorna la tupla de mensaje, p.e. ("GO", sender_id) o ("BACK", sender_id_or_None).
        """
      
        if self.id_nodo == 0:
            self.padre = self.id_nodo
            self.mensajes_esperados = len(self.vecinos)
            for v in self.vecinos:
                self.canal_salida.envia((self.id_nodo, GO_MSG), [v])

        while True:
            remitente, tipo_mensaje = yield self.canal_entrada.get()

            if tipo_mensaje == GO_MSG:
                if self.padre is None:
                    self.padre = remitente
                    self.mensajes_esperados = len(self.vecinos) - 1
                    if self.mensajes_esperados == 0:
                        self.canal_salida.envia((self.id_nodo, BACK_MSG), [remitente])
                    else:
                        for v in self.vecinos:
                            if v != remitente:
                                self.canal_salida.envia((self.id_nodo, GO_MSG), [v])
                else:
                    self.canal_salida.envia((None, BACK_MSG), [remitente])

            elif tipo_mensaje == BACK_MSG:
                self.mensajes_esperados -= 1
                if remitente is not None:
                    self.hijos.append(remitente)

                if self.mensajes_esperados == 0:
                    if self.padre != self.id_nodo:
                        self.canal_salida.envia((self.id_nodo, BACK_MSG), [self.padre])
