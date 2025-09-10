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
        self.id_nodo =  id_nodo 
        self.vecinos =  vecinos  # Vecinos del proceso
        self.canal_entrada = canal_entrada 
        self.canal_salida = canal_salida 
        self.mensaje = mensaje
        self.procesos_conocido =  {self.id_nodo}
        self.canales_conocidos =  {(self.id_nodo,y)  for y in self.vecinos }

    def toString(self):
        return f'Nodo : {self.id_nodo},\n vecinos: {self.vecinos},\nprocesos conocidos{self.procesos_conocido},\n canales_conocidos: {self.canales_conocidos}'

    def topologia(self, env):
        # Tú código aquí
        self.canal_salida.envia((self.id_nodo,self.vecinos),self.vecinos)

        while True :
            mssg = yield  self.canal_entrada.get()
            k,vecinos_j = mssg[0], mssg[1]
            if k not in self.procesos_conocido :
                self.procesos_conocido.add(k)
                #self.procesos_conocido.update({k})
                nuevos_canales = {(k,l)  for l in vecinos_j}
                self.canales_conocidos.update(nuevos_canales)
                vecinos_filtrados =  [m for m in self.vecinos if m != k]
                self.canal_salida.envia((k,vecinos_j),vecinos_filtrados)

                todos_conocidos =  True 

                for l,m in self.canales_conocidos :
                    evaluador =  l in self.procesos_conocido  and m in self.procesos_conocido 
                    todos_conocidos = todos_conocidos  and evaluador 
                
                if todos_conocidos :
                    break 

env = simpy.Environment()
bc_pipe = CanalBroadcast(env)

grafica =  [[1,2],[0],[0,3],[2]]
#grafica2 = [[1],[0,2,3],[1,4,5],[1],[2],[2]]
sistema_distribuido =  []

tick = 1

for i in range(0, len(grafica)):
            sistema_distribuido.append(NodoTopologia(i, grafica[i],
                                       bc_pipe.crea_canal_de_entrada(), bc_pipe))

                        
for nodo in sistema_distribuido:
    env.process(nodo.topologia(env))


env.run(until=10)

#
print("Grafica : ", grafica )
print("Final de ejecucion")

for nodo in sistema_distribuido :
    print(nodo.toString())









            
    
    
