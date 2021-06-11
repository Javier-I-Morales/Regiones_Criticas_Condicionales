import random
import time
import logging
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class Tenedores(Recurso):

    listaTenedores = [True,True,True,True,True]
    cantFilosofos = 0


recursoFilosofo = Tenedores()

region_Filosofos = Region(recursoFilosofo, threading.Semaphore(int(len(recursoFilosofo.listaTenedores)/2)))


@region_Filosofos.region
def seccionCritica():
    for i in range(2):
        indice = recursoFilosofo.listaTenedores.index(True)
        recursoFilosofo.listaTenedores[indice] = False
    logging.info(f'Filosofo comiendo, quedan {recursoFilosofo.listaTenedores.count(True)} tenedores')
    time.sleep(random.randint(3, 6))
    for i in range(2):
        indice = recursoFilosofo.listaTenedores.index(False)
        recursoFilosofo.listaTenedores[indice] = True
    logging.info(f'Filosofo Termino de comer, quedan {recursoFilosofo.listaTenedores.count(True)} tenedores')
    time.sleep(random.randint(3, 6))



def Cenar():
    while True:
        time.sleep(0.1)
        seccionCritica()



def main():

    cantidadDeFilosofos = 5

    for i in range(cantidadDeFilosofos):
        threading.Thread(target=Cenar,daemon=True).start()

    time.sleep(300)


if __name__ == "__main__":
    main()