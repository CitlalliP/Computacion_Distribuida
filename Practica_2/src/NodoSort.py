import simpy
from Nodo import *
from Canales.CanalBroadcast import *
from Auxiliares import *

TICK = 1

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
                    self.arr = arr
                    n = len(arr)
                    cantidad_nodos = self.cantidad_nodos
                    segmentos = [arr[i*n//cantidad_nodos:(i+1)*n//cantidad_nodos] for i in range(cantidad_nodos)]

                    yield env.timeout(TICK)

                    for i, vecino in enumerate(self.vecinos, start=1):
                        if i < len(segmentos):
                            self.canal_salida.envia(("GO", segmentos[i]), [vecino])
                        else:
                            self.canal_salida.envia(("GO", []), [vecino])

                    sorted_segments = [sorted(segmentos[0])]

                    for _ in range(cantidad_nodos - 1):
                        orden, datos = yield self.canal_entrada.get()
                        sorted_segments.append(datos)

                    resultado = sorted_segments[0]
                    for seg in sorted_segments[1:]:
                        resultado = self.merge_dos_listas(resultado, seg)

                    self.arr = resultado 
                    print("Arreglo ordenado final:", resultado)

        else:
                    while True:
                        orden, datos = yield self.canal_entrada.get()
                        if orden == "GO":
                            datos_ordenados = sorted(datos)
                            self.canal_salida.envia(("RESULT", datos_ordenados), [0])

    def merge_dos_listas(self, lista1, lista2):
                    '''Combina dos listas ordenadas en una sola lista ordenada'''
                    resultado = []
                    i = j = 0
                    while i < len(lista1) and j < len(lista2):
                        if lista1[i] <= lista2[j]:
                            resultado.append(lista1[i])
                            i += 1
                        else:
                            resultado.append(lista2[j])
                            j += 1
                    resultado.extend(lista1[i:])
                    resultado.extend(lista2[j:])
                    return resultado
                