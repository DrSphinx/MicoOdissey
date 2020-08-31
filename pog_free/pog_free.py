#BRUNO DE OLIVEIRA 31/08/2020
#MICOODISSEY Future Bio
import time

import pygame as pg
import json
import utils
from random import randint

class Celula(object):
    def __init__(self):
        self.xna = json.load(open('xna_tiles/xna_demo.json', 'r'))
        #self.display = display
        self.gerar_estrutura()

    def gerar_estrutura(self):
        self.carioteca = Carioteca()
        self.citoplasma = Citoplasma()
        self.membrana = Membrana()
        self.cloroplastos = Cloroplasto()
        self.parede_celular = Parede_celular()

    def transporte_passivo(self):
        tempo = time.perf_counter()
        incial = tempo
        ##CONTROLE DE TRANSPORTE INTRA/EXTRA-CELULAR. NÃO MEXER!
        #DE: CARIOTECA
        for id, particula in self.carioteca.interior.copy().items():
            if particula.transportando:
                self.citoplasma.ocupa_interior(particula)
                self.carioteca.interior.pop(id)

                if particula.destino != "Citoplasma" and particula.destino != "Cloroplastos":
                    self.membrana.ocupa_interior(particula)
                    self.citoplasma.interior.pop(id)

                    if particula.destino != "Membrana":
                        self.parede_celular.emissor = {particula.nome: particula.destino}
                        self.membrana.interior.pop(id)

                elif particula.destino != "Cloropastos":
                    self.cloroplastos.ocupa_interior(particula)
                    self.citoplasma.interior.pop(id)


        #DE: CITOPLASMA
        for id, particula in self.citoplasma.interior.copy().items():
            if particula.transportando:
                if particula.destino == "Carioteca":
                    self.carioteca.ocupa_interior(particula)
                    self.citoplasma.interior.pop(id)

                elif particula.destino != "Cloroplasto":
                    self.membrana.ocupa_interior(particula)
                    self.citoplasma.interior.pop(id)

                    if particula.destino != "Membrana":
                        self.parede_celular.emissor = {particula.nome: particula.destino}
                        self.membrana.interior.pop(id)

                elif particula.destino != "Cloropasto":
                    self.cloroplastos.ocupa_interior(particula)
                    self.citoplasma.interior.pop(id)

        #DE: MEMBRANA
        for id, particula in self.membrana.interior.copy().items():
            if particula.transportando:
                if particula.destino == "Parede":
                    self.parede_celular.emissor = {particula.nome: particula.destino}
                    self.membrana.interior.pop(id)
                else:
                    self.citoplasma.ocupa_interior(particula)
                    self.membrana.interior.pop(id)

                if particula.destino != "Citoplasma" and particula.destino != "Cloroplasto":
                    self.carioteca.ocupa_interior(particula)
                    self.citoplasma.interior.pop(id)

                elif particula.destino != "Cloropasto":
                    self.cloroplastos.ocupa_interior(particula)
                    self.citoplasma.interior.pop(id)

        print(f'Tempo laço: {time.perf_counter() - incial}')

class Carioteca(Celula):
    def __init__(self):
        self.interior = {}

    def ocupa_interior(self, particle):
        self.interior[particle.id] = particle


class Citoplasma(object):
    def __init__(self):
        self.interior = {}

    def ocupa_interior(self, particle):
        self.interior[particle.id] = particle

class Membrana(object):
    def __init__(self):
        self.osmose_taxa = 0
        self.interior = {}

    def ocupa_interior(self, particle):
        self.interior[particle.id] = particle

class Parede_celular(object):
    def __init__(self):
        self.receptores = {}
        self.emissor = {}

class Cloroplasto(object):
    def __init__(self):
        self.interior = {}
        self.retorno_energetico = None
        self.alias = "Cloroplasto"

    def ocupa_interior(self, particle):
        self.interior[particle.id] = particle

class Particula(object):
    def __init__(self, nome, xna_tile="", transportando=False, destino=""):
        self.nome = nome
        self.xna_tile = xna_tile
        self.transportando = transportando
        self.destino = destino
        self.id = f"{randint(0,9)}{randint(0,9)}{randint(0,9)}"

rnae = Particula("RnaE", transportando=True, destino="Cloroplasto")
ribossomo = Particula("Ribossomo", transportando=True, destino="Cloroplasto")
adrenalina = Particula("Adrenalina", transportando=True, destino="Cloroplasto")

celula = Celula()
celula.carioteca.ocupa_interior(rnae)
celula.citoplasma.ocupa_interior(ribossomo)
celula.membrana.ocupa_interior(adrenalina)

print("\n\n\n")
celula.transporte_passivo()