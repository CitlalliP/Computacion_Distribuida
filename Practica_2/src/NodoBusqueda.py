import simpy
from Nodo import *
from Canales.CanalBroadcast import *
from Auxiliares import *

TICK = 1
class NodoBusqueda(Nodo):
    def __init__(self, id_nodo,vecinos,cantidad_nodos ,canal_entrada, canal_salida,mensaje=None):
        '''Inicializamos el nodo.'''
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.cantidad_nodos =  cantidad_nodos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.arr = []
        self.contenido = False 
    

    def toString(self):
        return f"Id_nodo = {self.id_nodo},Vecinos: {self.vecinos},array: {self.arr},estado: {self.contenido}"

    def busqueda(self,env,arr,elemento):
        '''Implementar'''
        


        if self.id_nodo == 0 :
          

            self.arr = 0
            #Cuadricula -> 
            yield env.timeout(TICK)
           
            self.canal_salida.envia(("GO", arr ,elemento), self.vecinos)

        while True :
            orden,arr_,elem = yield self.canal_entrada.get()
            self.arr = arr_
            
            if orden == "GO" :
                encontrado = False 
                for e in arr_ :
                    if e == elem :
                        encontrado = True 
                        break

                if encontrado :
                    msg =  ("FOUND",arr_,elemento)  
                    self.contenido = True 
                    self.canal_salida.envia(msg,[0])
                else:
                    msg =  ("NOT_FOUND",arr_,elemento)  
                    self.contenido = False
                    self.canal_salida.envia(msg,[0])

            else:
                if orden == "FOUND":
                    self.contenido = True 

import random 
TIEMPO_DE_EJECUCION = 10
env = simpy.Environment()
bc_pipe = CanalBroadcast(env)
estrella =  [[1,2,3,4,5,6,7],[0],[0],[0],[0],[0],[0],[0]]
arr  = [random.randint(0, 99) for _ in range(11)]
elem = 100 
arr.append(elem)
random.shuffle(arr)
# La lista que representa la gráfica
grafica = []

# Creamos los nodos
for i in range(0, len(estrella)):
    grafica.append(NodoBusqueda(i, estrella[i],len(estrella)-1,
                                bc_pipe.crea_canal_de_entrada(), bc_pipe))

# Le decimos al ambiente lo que va a procesar ...
for nodo in grafica:
    #env.process(nodo.busqueda(env,arr,elem))
    env.process(nodo.busqueda(env,arr,-1000))
# ...y lo corremos
env.run(until=TIEMPO_DE_EJECUCION)
resultado =  grafica[0].contenido

for n in grafica :
    print(n.toString())


                    
                     







    
        

    
