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
        if self.id_nodo == 0:
            segmentos = cuadricula(arr, self.cantidad_nodos)
            # enviar segmentos a cada vecino (si hay más vecinos que segmentos enviar [])
            for i, vecino in enumerate(self.vecinos):
                seg = segmentos[i] if i < len(segmentos) else []
                self.canal_salida.envia(("GO", self.id_nodo, seg), [vecino])

            partes_ordenadas = []
            esperados = len(self.vecinos)
            recibidos = 0
            while recibidos < esperados:
                msg = yield self.canal_entrada.get()
                if msg[0] == "BACK":
                    partes_ordenadas.append(list(msg[2]))
                    recibidos += 1
                else:
                    continue

            # merge k-way y guardar resultado
            self.arr = k_merge(partes_ordenadas)
            return self.arr

        # Trabajador
        else:
            while True:
                msg = yield self.canal_entrada.get()
                if msg[0] == "GO":
                    emisor = msg[1]
                    segmento = list(msg[2]) if len(msg) > 2 else []
                    # ordenar localmente
                    segmento.sort()
                    # pequeño retardo de procesamiento
                    yield env.timeout(1)
                    # enviar resultado al coordinador
                    self.canal_salida.envia(("BACK", self.id_nodo, segmento), [emisor])
                    self.arr = segmento
                    return segmento
                else:
                    continue


    


        






