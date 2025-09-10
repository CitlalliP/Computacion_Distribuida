"""NodoBroadcast.py

Módulo que define la clase NodoBroadcast para el algoritmo de Broadcast (flooding).
"""

import simpy

from Nodo import *

from Canales.CanalBroadcast import *


# La unidad de tiempo
TICK = 1


class NodoBroadcast(Nodo):
    '''Nodo que participa en el algoritmo de Broadcast.

    Atributos:
        id_nodo: identificador del nodo.
        vecinos: lista de ids de vecinos.
        canal_entrada: Store donde recibe mensajes.
        canal_salida: CanalBroadcast para enviar mensajes.
        mensaje: contenido actual del nodo (puede ser None).
        seen_message: indica si ya recibió el mensaje.

    Comportamiento:
        - El nodo 0 inicia el broadcast creando/teniendo un mensaje y enviándolo
          a sus vecinos.
        - Cada nodo espera mensajes en su canal de entrada y, al recibir el
          primer mensaje, lo almacena, marca `seen_message` y lo reenvía a sus
          vecinos.
    '''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
        # Inicializamos los atributos del nodo
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida

        self.mensaje = mensaje

        self.seen_message =  False 

    def broadcast(self, env):
        '''Proceso SimPy que implementa el broadcast.

        Parámetros
        ----------
        env : simpy.Environment
            Ambiente de simulación en el que corre el proceso.
        '''
        # Si soy el nodo distinguido (0), inicio el broadcast
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
