# BRUNO DE OLIVEIRA 31/08/2020 <- data de inicio.
# MICOODISSEY Future B

import pygame as pg
import json
from random import randint


def ocupa_interior(self, particula):
    self.interior[particula.id] = particula


class Celula(object):
    def __init__(self):
        self.xna = json.load(open('xna_tiles/xna_demo.json', 'r'))
        # self.display = display
        self.fonte_luz = None
        self.gerar_estrutura()
        self.t = 0

    def gerar_estrutura(self):
        self.carioteca = Carioteca()
        self.citoplasma = Citoplasma()
        self.membrana = Membrana()
        self.cloroplastos = Cloroplasto()
        self.parede_celular = ParedeCelular()

    def transporte_passivo(self):
        # tempo = time.perf_counter()
        # incial = tempo
        ##CONTROLE DE TRANSPORTE INTRA/EXTRA-CELULAR. NÃO MEXER!
        # DE: CARIOTECA
        for id, particula in self.carioteca.interior.copy().items():
            if particula.transportando:
                self.migrar(self.citoplasma, self.carioteca, particula)

                if particula.destino != "Citoplasma" and particula.destino != "Cloroplasto":
                    self.migrar(self.membrana, self.citoplasma, particula)

                    if particula.destino != "Membrana":
                        self.parede_celular.emissor = {particula.nome: particula.destino}
                        self.membrana.interior.pop(id)
                        self.citoplasma.pedir_energia(self.parede_celular, 1, 1)

                if particula.destino == "Cloroplasto":
                    self.migrar(self.cloroplastos, self.citoplasma, particula)

        # DE: CITOPLASMA
        for id, particula in self.citoplasma.interior.copy().items():
            if particula.transportando:
                if particula.destino == "Carioteca":
                    self.migrar(self.carioteca, self.citoplasma, particula)

                elif particula.destino != "Cloroplasto":
                    self.migrar(self.membrana, self.citoplasma, particula)

                    if particula.destino != "Membrana":
                        self.parede_celular.emissor = {particula.nome: particula.destino}
                        self.membrana.interior.pop(id)
                        self.citoplasma.pedir_energia(self.parede_celular, 1, 1)

                else:
                    self.migrar(self.cloroplastos, self.citoplasma, particula)

        # DE: MEMBRANA
        for id, particula in self.membrana.interior.copy().items():
            if particula.transportando:
                if particula.destino == "Parede":
                    self.parede_celular.emissor = {particula.nome: particula.destino}
                    self.membrana.interior.pop(id)
                    self.citoplasma.pedir_energia(self.parede_celular, 1, 1)
                else:
                    self.migrar(self.citoplasma, self.membrana, particula)

                    if particula.destino != "Citoplasma" and particula.destino != "Cloroplasto":
                        self.migrar(self.carioteca, self.citoplasma, particula)

                    elif particula.destino == "Cloroplasto":
                        self.migrar(self.cloroplastos, self.citoplasma, particula)

        # print(f'Tempo laço: {time.perf_counter() - incial}')

    def gera_energia(self):
        self.citoplasma.energia += self.cloroplastos.fotossintese(self.fonte_luz)

    def migrar(self, destino, origem, particula):
        if destino in ["Parede", "Cloroplasto"]:
            if self.citoplasma.pedir_energia(self.parede_celular, 1, 1, retorno=True):
                self.parede_celular.emissor = {particula.nome: particula.destino}
                self.membrana.interior.pop(id)
        else:
            if self.citoplasma.pedir_energia(destino, 1, 0.1):
                ocupa_interior(destino, particula)
                origem.interior.pop(particula.id)

    def iter(self):
        def transporte():
            self.transporte_passivo()

        def energizar():
            self.gera_energia()


class Carioteca(object):
    def __init__(self):
        self.interior = {}
        self.energia = 0


class Citoplasma(object):
    def __init__(self):
        self.interior = {}
        self.energia = 0
        self.pilha = []

    def pedir_energia(self, receptor, importancia, quantidade, retorno=False):
        self.pilha.append(
            {"receptor": receptor, "importancia": importancia, "quantidade": quantidade, "retorno": retorno})
        return self.conceder_energia()

    def conceder_energia(self):
        for pedido in self.pilha:
            pedido["importancia"] -= 1
            maior = {"importancia": 0}  # maior importancia
        for i, pedido in enumerate(self.pilha):
            if pedido["importancia"] > maior["importancia"]:
                maior = pedido
                print(f'maior = {maior} {pedido}')

        if self.energia > pedido["quantidade"]:
            self.energia -= pedido["quantidade"]
            if pedido["retorno"]:
                pedido["receptor"].energia += pedido["quantidade"]
            del (self.pilha[i])
            return True
        else:
            return False


class Membrana(object):
    def __init__(self):
        self.osmose_taxa = 0
        self.interior = {}
        self.energia = 0


class ParedeCelular(object):
    def __init__(self):
        self.receptores = {}
        self.emissor = {}
        self.energia = 0


class Cloroplasto(object):
    def __init__(self):
        self.interior = {}
        self.retorno_energetico = 2
        self.alias = "Cloroplasto"
        self.recursos = {"Água": 0, "CO2": 0, "O2": 0}
        self.rect = pg.Rect((0, 0), (10, 10))
        self.cor = (0, 255, 0)

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
                    # gera e aloca o produto da reacao
                    oxigenio = Particula("O2", transportando=True, destino="Exterior")
                    ocupa_interior(self, oxigenio)
                    self.cor = (255, 255, 255)
                    return self.retorno_energetico
            else:
                return 0

    def inventario(self):
        self.recursos = {"Água": 0, "CO2": 0, "O2": 0}
        for particula in self.interior.values():
            if particula.nome == "CO2":
                self.recursos["CO2"] += 1
            elif particula.nome == "Água":
                self.recursos["Água"] += 1
            elif particula.nome == "O2":
                self.recursos["O2"] += 1

    def gastar_substancia(self, substancia, qnt):
        ct = 0
        for particula in self.interior.copy().values():
            if ct <= qnt:
                if particula.nome == substancia:
                    self.interior.pop(particula.id)
                    ct += 1
            else:
                break

    def draw(self, display, cell_rect):
        self.rect.center = (cell_rect.x + cell_rect.w / 2, cell_rect.y + cell_rect.h / 2 + 3)
        pg.draw.ellipse(display, self.cor, self.rect, 5)
        pg.time.wait(50)
        self.cor = (0, 255, 0)


class Particula(object):
    def __init__(self, nome, xna_tile="", transportando=False, destino=""):
        self.nome = nome
        self.xna_tile = xna_tile
        self.transportando = transportando
        self.destino = destino
        self.id = f"{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}"


class FonteLuz(object):
    def __init__(self, comprimento, abundancia):
        self.comprimento = comprimento
        self.abundancia = abundancia
