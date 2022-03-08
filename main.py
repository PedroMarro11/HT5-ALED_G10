#Main.py
#Pedro Javier Marroquin Carne 21801
#Juan Miguel Gonzalez-Campo Carne 21077
#Paulo Raul Sanchez Gonzalez Carne 21401
#!/usr/bin/env python3
import simpy
import random
#Declaracion de variables
env = simpy.Environment()
RAM_Total = simpy.Container(env, init=100, capacity = 100)
running = simpy.Resource(env, capacity = 1)
new = simpy.Resource(env, capacity = 200)
ready = simpy.Resource(env, capacity = 100)
waiting = simpy.Resource(env, capacity = 200)


#Clase proceso
def proceso(env, nombre):
    """Proceso que se corre dentro de una CPU"""
    #Generacion de random
    memoria = random.expovariate(1.0/10)

    instructions = random.expovariate(1.0/10)
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
            break
        else:
            continue
    #Ciclo while
    while is_running:
        with running.request() as req2:
            yield req2
            if(instructions >= 3):
                yield env.timeout(3)
                instructions -= 3

            else:
                yield env.timeout(3)
                instructions = 0
        #Condicin al no haber instrucciones dispoibles
        if(instructions == 0):
            print("El proceso %s ha terminado" %(nombre))
            RAM_Total.put(memoria)
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


#def crear_procesos():
contador = 0
#Ciclo for para repetir los procesos
random.seed(10)
while (contador != 25):
    crear = random.expovariate(1.0/10.0)
    crear = int(crear)
    for i in range(crear):
        if (contador < 25):
            env.process(proceso(env, 'programa %d' %(contador+1)))
            #if(crear == new.count):
            contador += 1
            print("Proceso creado")
        else:
            break

#Corrida del environment
env.run()
