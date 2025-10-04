import simpy
from Nodo import *
from Canales.CanalRecorridos import *

# La unidad de tiempo
TICK = 1

class NodoDFS(Nodo):

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida):
        ''' Constructor de nodo que implemente el algoritmo DFS. '''
        # Tu implementación va aquí
        super().__init__(id_nodo, vecinos, canal_entrada, canal_salida)
        self.padre = None
        self.hijos = []
        self.completed_children = set()
        self.visitado = False
        self.finalizado = False



        
    def dfs(self, env):
        ''' Algoritmo DFS. '''
        # Tu implementación va aqui
        
        if self.id_nodo == 0:
            self.visitado = True
            self.padre = self.id_nodo
            self.finalizado = False
            yield env.timeout(TICK)

            candidatos = sorted(v for v in self.vecinos if v not in self.completed_children)
            if candidatos:
                siguiente = candidatos[0]
                yield self.canal_salida.envia(("GO", self.id_nodo), [siguiente])

        while True:
            raw = yield self.canal_entrada.get()  
            tipo = raw[0]

            if tipo == "GO":
                remitente = raw[1] if len(raw) > 1 else None

                if not self.visitado:
                    self.visitado = True
                    self.padre = remitente

                    yield env.timeout(TICK)
                    candidatos = sorted(v for v in self.vecinos if v != self.padre and v not in self.completed_children)

                    if candidatos:
                        siguiente = candidatos[0]
                        yield self.canal_salida.envia(("GO", self.id_nodo), [siguiente])
                    else:
                       
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(("BACK", "YES", self.id_nodo), [self.padre])
                else:
              
                    yield env.timeout(TICK)
                    yield self.canal_salida.envia(("BACK", "NO", self.id_nodo), [remitente])

            elif tipo == "BACK":
                resp = raw[1] if len(raw) > 1 else None
                hijo = raw[2] if len(raw) > 2 else None
    
                if hijo is not None:
                    self.completed_children.add(hijo)

                if resp == "YES" and hijo is not None and hijo not in self.hijos:
                    self.hijos.append(hijo)

                yield env.timeout(TICK)

                candidatos = sorted(v for v in self.vecinos if v != self.padre and v not in self.completed_children)

                if candidatos:
                    siguiente = candidatos[0]
                    yield self.canal_salida.envia(("GO", self.id_nodo), [siguiente])
                else:
                    
                    if self.padre == self.id_nodo:
                       
                        self.finalizado = True
                        return
                    else:
                        yield env.timeout(TICK)
                        yield self.canal_salida.envia(("BACK", "YES", self.id_nodo), [self.padre])

            else:
                yield env.timeout(TICK)

