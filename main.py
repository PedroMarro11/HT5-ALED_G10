#Main.py
#Pedro Javier Marroquin Carne 21801
#Juan Miguel Gonzalez-Campo Carne 21077
#Paulo Raul Sanchez Gonzalez Carne 21401
#!/usr/bin/env python3
import simpy
import random
import numpy as np

#Declaracion de variables
env = simpy.Environment()
RAM = 100
RAM_Total = simpy.Container(env, init=RAM, capacity = RAM)
running = simpy.Resource(env, capacity = 2)
new = simpy.Resource(env, capacity = 200)
ready = simpy.Resource(env, capacity = 100)
waiting = simpy.Resource(env, capacity = 200)
Programas = 200
Intervalo = 1.0
crear = 0
instrucciones = 3
#Clase proceso
def proceso(env, nombre):
    global tiempoPromedio
    global listaT
    
    """Proceso que se corre dentro de una CPU"""
    #Generacion de random
    memoria = random.randint(1,10)

    instructions = random.randint(1,10)
    #Ciclo with
    with new.request() as req:
        yield req
        print("Se ha creado el proceso %s" %(nombre))

    is_running = True
    #Ciclo while
    #Determina a partir si hay memoria disponible para llevar a cabo el proceso
    while True:     
        if (memoria < RAM_Total.level):
            with ready.request() as req1:
                yield req1
                RAM_Total.get(memoria)
                tiempoInicio = env.now
            break
        else:
            yield env.timeout(1)
            continue
        
    #Ciclo while
    while is_running:
        with running.request() as req2:
            yield req2
            if(instructions >= instrucciones):
                yield env.timeout(1)
                instructions -= instrucciones

            else:
                yield env.timeout(1)
                instructions = 0
        #Condicin al no haber instrucciones dispoibles
        if(instructions == 0):
            print("El proceso %s ha terminado" %(nombre))
            RAM_Total.put(memoria)
            tiempoFinal = env.now
            tiempoTotal = (tiempoFinal - tiempoInicio)
            tiempoPromedio += tiempoTotal
            listaT.append(tiempoTotal)
            is_running = False
        #Generacion de random para los elementos que se encuentren en la cola
        else:
            cola = random.randint(1,2)
            if(cola == 1):
                with waiting.request() as req3:
                    yield req3
                    yield env.timeout(instructions)

            with ready.request() as req4:
                yield req4
                continue

def crear_procesos():
    global contador
    for i in range(Programas):
        c = proceso(env, 'programa %d' %(contador+1))
        env.process(c)
        contador += 1
        crear = random.expovariate(1.0/Intervalo)
        print("Proceso creado")
        yield env.timeout(crear)

random.seed(10)
#Corrida del environment
tiempoPromedio = 0
listaT = []
contador = 0
env.process(crear_procesos())
env.run()
print("Promedio de tiempo: %d" %(tiempoPromedio/Programas))
print("Desviacion estandar: %d" %(np.std(listaT)))
