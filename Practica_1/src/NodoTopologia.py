import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

# La unidad de tiempo
TICK = 1


class NodoTopologia(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
	#Tú código aquí

        self.proc_conocidos= {id_nodo}
        self.canales_conocidos = {(id_nodo,j) for j in self.vecinos}


    def topologia(self, env):
        # Tú código aquí







            
    
    
