import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1


class NodoBFS(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo BFS. '''
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = id_nodo
        self.hijos = []
        self.distancia = 0
        self.mensajes_esperados = 0

    def bfs(self, env):
        if self.id_nodo == 0:
            yield self.canal_salida.envia(("IR", -1, self.id_nodo), [self.id_nodo])
            yield env.timeout(TICK)

        while True:
            msg = yield self.canal_entrada.get()
            tipo = msg[0]

            if tipo == "IR":
                _, d, j = msg

                if self.padre == self.id_nodo:
                    self.padre = j
                    self.hijos = []
                    self.distancia = d + 1
                    self.mensajes_esperados = len(self.vecinos) - (1 if j in self.vecinos else 0)

                    if self.mensajes_esperados == 0:
                        yield self.canal_salida.envia(("VOLVER", "si", self.distancia, self.id_nodo), [self.padre])
                        yield env.timeout(TICK)
                    else:
                        destinos = [v for v in self.vecinos if v != j]
                        if destinos:
                            yield self.canal_salida.envia(("IR", self.distancia, self.id_nodo), destinos)
                            yield env.timeout(TICK)

                elif self.distancia > d + 1:
                    self.padre = j
                    self.hijos = []
                    self.distancia = d + 1
                    self.mensajes_esperados = len(self.vecinos) - (1 if j in self.vecinos else 0)

                    if self.mensajes_esperados == 0:
                        yield self.canal_salida.envia(("VOLVER", "si", self.distancia, self.id_nodo), [self.padre])
                        yield env.timeout(TICK)
                    else:
                        destinos = [v for v in self.vecinos if v != j]
                        if destinos:
                            yield self.canal_salida.envia(("IR", self.distancia, self.id_nodo), destinos)
                            yield env.timeout(TICK)
                else:
                    yield self.canal_salida.envia(("VOLVER", "no", d + 1, self.id_nodo), [j])
                    yield env.timeout(TICK)

            elif tipo == "VOLVER":
                if len(msg) == 4:
                    _, resp, d, j = msg
                else:
                    _, resp, d = msg
                    j = None

                if d == self.distancia + 1:
                    if resp == "si" and j is not None:
                        if j not in self.hijos:
                            self.hijos.append(j)

                    if self.mensajes_esperados > 0:
                        self.mensajes_esperados -= 1

                    if self.mensajes_esperados == 0:
                        if self.padre != self.id_nodo:
                            yield self.canal_salida.envia(("VOLVER", "si", self.distancia, self.id_nodo), [self.padre])
                            yield env.timeout(TICK)
                        else:
                            pass
                else:
                    pass
