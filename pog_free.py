# BRUNO DE OLIVEIRA 31/08/2020
# MICOODISSEY Future Bio

import time

import pygame as pg
import json
from random import randint


class Celula(object):
    def __init__(self):
        self.xna = json.load(open('xna_tiles/xna_demo.json', 'r'))
        # self.display = display
        self.energia = 0
        self.fonte_luz = None
        self.gerar_estrutura()

    def gerar_estrutura(self):
        self.carioteca = Carioteca()
        self.citoplasma = Citoplasma()
        self.membrana = Membrana()
        self.cloroplastos = Cloroplasto()
        self.parede_celular = ParedeCelular()

    def transporte_passivo(self):
        #tempo = time.perf_counter()
        #incial = tempo
        ##CONTROLE DE TRANSPORTE INTRA/EXTRA-CELULAR. NÃO MEXER!
        #DE: CARIOTECA
        for id, particula in self.carioteca.interior.copy().items():
            if particula.transportando:
                self.citoplasma.ocupa_interior(particula)
                self.carioteca.interior.pop(id)

                if particula.destino != "Citoplasma" and particula.destino != "Cloroplasto":
                    self.membrana.ocupa_interior(particula)
                    self.citoplasma.interior.pop(id)

                    if particula.destino != "Membrana":
                        self.parede_celular.emissor = {particula.nome: particula.destino}
                        self.membrana.interior.pop(id)

                if particula.destino == "Cloroplasto":
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

                else:
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

                    elif particula.destino == "Cloroplasto":
                        self.cloroplastos.ocupa_interior(particula)
                        self.citoplasma.interior.pop(id)

        #print(f'Tempo laço: {time.perf_counter() - incial}')

    def gera_energia(self):
        self.energia += self.cloroplastos.fotossintese(self.fonte_luz)


class Carioteca(object):
    def __init__(self):
        self.interior = {}

    def ocupa_interior(self, particula):
        self.interior[particula.id] = particula


class Citoplasma(object):
    def __init__(self):
        self.interior = {}

    def ocupa_interior(self, particula):
        self.interior[particula.id] = particula


class Membrana(object):
    def __init__(self):
        self.osmose_taxa = 0
        self.interior = {}

    def ocupa_interior(self, particula):
        self.interior[particula.id] = particula


class ParedeCelular(object):
    def __init__(self):
        self.receptores = {}
        self.emissor = {}


class Cloroplasto(object):
    def __init__(self):
        self.interior = {}
        self.retorno_energetico = 2
        self.alias = "Cloroplasto"
        self.recursos = {"Água": 0, "CO2": 0}

    def ocupa_interior(self, particula):
        self.interior[particula.id] = particula

    # PRECISA DE OTIMIZAÇÃO!!
    def fotossintese(self, fonte_luz):
        # conta cada tipo de substancia no interior do cloroplasto
        self.inventario()
        # verifica se tem os recursos minimos
        if fonte_luz is not None:
            if self.recursos["Água"] >= 1:
                if self.recursos['CO2'] >= 1:
                    self.recursos["Água"] -= 1
                    self.recursos["CO2"] -= 1
                    # gasta os recursos usados
                    self.gastar_substancia("Água", 1)
                    self.gastar_substancia("CO2", 1)
                    # gera e aloca o produto da reacao FUTURAMENTE USADO COMO ENERGIA BRUTA
                    acucar = Particula("O2", transportando=True, destino="Exterior")
                    self.ocupa_interior(acucar)
                    return self.retorno_energetico
            else:
                return 0

    def inventario(self):
        for particula in self.interior.values():
            if particula.nome == "CO2":
                self.recursos["CO2"] += 1
            elif particula.nome == "Água":
                self.recursos["Água"] += 1

    def gastar_substancia(self, substancia, qnt):
        ct = 0
        for particula in self.interior.copy().values():
            if ct <= qnt:
                if particula.nome == substancia:
                    self.interior.pop(particula.id)
                    ct += 1
            else: break


class Particula(object):
    def __init__(self, nome, xna_tile="", transportando=False, destino=""):
        self.nome = nome
        self.xna_tile = xna_tile
        self.transportando = transportando
        self.destino = destino
        self.id = f"{randint(0,9)}{randint(0,9)}{randint(0,9)}"


class FonteLuz(object):
    def __init__(self, comprimento, abundancia):
        self.comprimento = comprimento
        self.abundancia = abundancia


if True:
    gas_carbonico = Particula("CO2", transportando=True, destino="Cloroplasto")
    agua = Particula("Água", transportando=True, destino="Cloroplasto")
    # adrenalina = Particula("Adrenalina", transportando=True, destino="Cloroplasto")

    celula = Celula()
    celula.carioteca.ocupa_interior(gas_carbonico)
    celula.citoplasma.ocupa_interior(agua)

    # celula.membrana.ocupa_interior(adrenalina)

    print("\n\n\n")
    celula.transporte_passivo()
    celula.fonte_luz = FonteLuz(700, 1)
    celula.gera_energia()