import threading
import logging
import random
import time
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Este_Recurso(Recurso):
        dato1 = 0
        numEscritores = 0


Mi_Recurso = Este_Recurso()


def condicion_Lector():
    return Mi_Recurso.numEscritores == 0


def condicion_Escritor():
    return True


Region_Escritores = Region(Mi_Recurso,threading.Lock())

Region_Condicional_Lectores = RegionCondicional(Mi_Recurso, condicion_Lector)

Region_Condicional_Escritores = RegionCondicional(Mi_Recurso, condicion_Escritor)


@Region_Condicional_Lectores.condicion
def seccionCriticaLectorCondicional():
    logging.info(f'Lector lee dato1 = {Mi_Recurso.dato1}')


def Lector():
    while True:
        seccionCriticaLectorCondicional()
        time.sleep(random.randint(3,6))


@Region_Escritores.region
def seccionCriticaEscritorAntes():
    Mi_Recurso.numEscritores += 1
    time.sleep(1)

@Region_Escritores.region
def seccionCriticaEscritorDespues():
    Mi_Recurso.numEscritores -= 1


@Region_Condicional_Escritores.condicion
def seccionCriticaEscritor():
    Mi_Recurso.dato1 = random.randint(0, 100)
    seccionCriticaEscritorAntes()
    logging.info(f'Escritor escribe dato1 = {Mi_Recurso.dato1}')
    seccionCriticaEscritorDespues()


def Escritor():
    while True:
        seccionCriticaEscritor()
        time.sleep(random.randint(1,4))


def main():
    nlector = 10
    nescritor = 2

    for k in range(nlector):
        threading.Thread(target=Lector, daemon=True).start()

    for k in range(nescritor):
        threading.Thread(target=Escritor, daemon=True).start()

    time.sleep(300)


if __name__ == "__main__":
    main()
