import threading
import logging
import random
import time
from regionCondicional import *

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)


class Este_Recurso(Recurso):
        dato1 = 0
        numLectores = 0


Mi_Recurso = Este_Recurso()


def condicion_Escritor():
    return Mi_Recurso.numLectores == 0


Region_Lectores = Region(Mi_Recurso)

Region_Condicional_Escritores = RegionCondicional(Mi_Recurso, condicion_Escritor)


@Region_Lectores.region
def seccionCriticaLector():
    Mi_Recurso.numLectores += 1
    time.sleep(1)
    Mi_Recurso.numLectores -= 1


def Lector():
    while True:
        seccionCriticaLector()
        logging.info(f'Lector lee dato1 = {Mi_Recurso.dato1}')
        time.sleep(random.randint(3,6))


@Region_Condicional_Escritores.condicion
def seccionCriticaEscritor():
    Mi_Recurso.dato1 = random.randint(0, 100)
    logging.info(f'Escritor escribe dato1 = {Mi_Recurso.dato1}')


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

