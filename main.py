#!/usr/bin/env python3
import simpy
import random

env = simpy.Environment()
RAM_Total = simpy.Container(env, init=100, capacity = 100)
running = simpy.Resource(env, capacity = 1)
new = simpy.Resource(env, capacity = 200)
ready = simpy.Resource(env, capacity = 100)
waiting = simpy.Resource(env, capacity = 200)



def proceso(env, nombre):
    memoria = random.expovariate(1.0/10)

    instructions = random.expovariate(1.0/10)

    with new.request() as req:
        yield req
        print("Se ha creado el proceso %s" %(nombre))
    is_running = True

    while True:
        if (memoria < RAM_Total.level):
            with ready.request() as req1:
                yield req1
                RAM_Total.get(memoria)
            break
        else:
            continue
    while is_running:

        with running.request() as req2:
            yield req2
            if(instructions >= 3):
                yield env.timeout(3)
                instructions -= 3

            else:
                yield env.timeout(3)
                instructions = 0

        if(instructions == 0):
            print("El proceso %s ha terminado" %(nombre))
            RAM_Total.put(memoria)
            is_running = False

        else:
            cola = random.randint(1,2)
            if(cola == 1):
                with waiting.request() as req3:
                    yield req3
                    yield env.timeout(instructions)

            with ready.request() as req4:
                yield req4
                continue


random.seed(10)
for i in range(25):
    env.process(proceso(env, 'programa %d' %(i+1)))

env.run()
