import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

# La unidad de tiempo
TICK = 1


class NodoBroadcast(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
	#Tu codigo aqui
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida

        self.mensaje = mensaje

        self.seen_message =  False 

    def broadcast(self, env):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0)
            vamos a enviar un mensaje a todos los demás nodos.'''
        # Tú código aquí
        if self.id_nodo == 0:
            if self.mensaje is None:
                self.mensaje = f"msg_from_{self.id_nodo}"
            self.seen_message = True

            self.canal_salida.envia(self.mensaje, self.vecinos)

        while True:
            mensaje =  yield self.canal_entrada.get()
            if not self.seen_message:
                self.mensaje = mensaje
                self.seen_message = True

                self.canal_salida.envia(self.mensaje, self.vecinos)





