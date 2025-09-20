import simpy
from Nodo import *
from Canales.CanalBroadcast import *
from Auxiliares import *
#from NodoGenerador import NodoGenerador


TICK = 1
class NodoConvergcast(Nodo):
    '''Implementa la interfaz de Nodo para el algoritmo de convergcast.'''
    def __init__(self, id_nodo,vecinos,valor, canal_entrada, canal_salida, mensaje=None):
            self.id_nodo = id_nodo
            self.padre = None
            self.vecinos = vecinos
            self.canal_entrada = canal_entrada
            self.canal_salida = canal_salida
            self.mensaje = mensaje
            self.value =  valor #self.id_nodo #Como ejemplo para los test diremos que los valores recolectados seran los ids , no usamos un conjunto pues no sabemos que se vaya ahacer (la funcion f)
            #self.val_set = [self.value] Situacional
            self.val_set = {self.value}
            self.funcion = None 
            self.valor_final = None

    def toString(self):
        return f"Nodo : {self.id_nodo},valor: {self.value}, valores: {self.val_set}"

    def convergecast(self,env,f):
    #       '''Implementar'''

        if self.id_nodo == 0:
            self.padre = self.id_nodo
            self.funcion = f
            yield env.timeout(TICK)
            self.canal_salida.envia(("INIT", self.id_nodo, set()), self.vecinos)

        while True:
            msg = yield self.canal_entrada.get()

            if msg[0] == "INIT":
                self.padre = msg[1]

                if self.vecinos:  # Si hay hijos no es una hoja
                    msg_ = ("INIT", self.id_nodo, set())
                    self.canal_salida.envia(msg_, self.vecinos)
                else:  # Comienzo del convergecast (hoja)
                    msg_back = ("BACK", self.id_nodo, self.val_set)
                    self.canal_salida.envia(msg_back, [self.padre])

            else:  # BACK del convergecast
                self.val_set.update(msg[2])
                if self.padre != self.id_nodo:
                    msg_back = ("BACK", self.id_nodo, self.val_set)
                    self.canal_salida.envia(msg_back, [self.padre])
                else:
                    self.value = f(self.val_set)
