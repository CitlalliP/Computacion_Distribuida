"""CanalBroadcast.py

Módulo que implementa CanalBroadcast, un canal one-to-many para enviar
mensajes entre nodos usando SimPy.
"""

import simpy
from Canales.Canal import Canal


class CanalBroadcast(Canal):
    '''
    Clase que modela un canal, permite enviar mensajes one-to-many.

    Atributos:
        env: simpy.Environment
            Ambiente de simulación donde se crean los Stores.
        capacidad: int | float
            Capacidad de cada Store creado (por defecto infinita).
        canales: list[simpy.Store]
            Lista de objetos Store que actúan como canales de entrada para cada nodo.
    '''

    def __init__(self, env, capacidad=simpy.core.Infinity):
        self.env = env
        self.capacidad = capacidad
        self.canales = []


    '''
    Metodo que regresa la lista de canales 
    '''
    def get_canales(self):
        """Devuelve la lista interna de canales (Stores).

        Útil para inspección o pruebas.
        """
        return self.canales 
    

    def envia(self, mensaje, vecinos):
        '''
        Envia un mensaje a los canales de salida de los vecinos.

        Parámetros
        ----------
        mensaje : any
            Contenido del mensaje a enviar.
        vecinos : iterable[int]
            Lista o colección de índices de vecinos a los que enviar.

        Comportamiento
        --------------
        - Si no hay canales registrados se lanza RuntimeError.
        - Para cada vecino válido (índice dentro de self.canales) se hace
          un put del mensaje en su Store y se acumula el evento en una lista.

        Nota: actualmente los eventos se crean pero no se espera explícitamente
        sobre ellos en este método — eso lo maneja el scheduler de SimPy cuando
        los procesos consumidores esperan con `yield canal.get()`.
        '''
        # Tu código aquí
        if not self.canales:
            raise RuntimeError( "No hay canales disponibles ")
        eventos = [] 
        
        for vecino in vecinos:
            if vecino in range(len(self.canales)):
                eventos.append(self.canales[vecino].put(mensaje))



    def crea_canal_de_entrada(self):
        '''
        Creamos un canal de entrada

        Crea un simpy.Store asociado al ambiente `self.env`, lo añade a
        la lista `self.canales` y lo devuelve para que el nodo lo use como su
        canal de entrada.
        '''
        canal_entrada = simpy.Store(self.env, capacity=self.capacidad)
        self.canales.append(canal_entrada)
        return canal_entrada