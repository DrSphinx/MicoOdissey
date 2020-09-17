import pygame as pg
import pygame.gfxdraw
from random import randint
import json
import time

agua = {'Nome': 'Água', 'Color': (0, 0, 255, 100)}

try:
    resolution = json.load(open('resolution', 'r'))
except:
    resolution = [600, 500]

max_width = resolution[0]
max_height = resolution[1]
center_x, center_y = max_width / 2, max_height / 2
cell_size = int(max_width * 0.04)


class CelulaSprite(pg.sprite.Sprite):
    def __init__(self, speed=0.1):
        super().__init__()
        self.image = pg.Surface([cell_size] * 2).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = pg.Vector2(center_x, center_y)
        self.set_target((center_x, center_y))
        self.speed = speed
        self.load_images()
        self.carioteca = CariotecaSprite(self)
        self.cloroplasto = CloroplastoSprite(self)
        self.flagelo = Flagelos(self)

        self.image.blit(self.cell, self.rect)

    def set_target(self, pos):
        pos_target = (pos[0] - self.rect.w / 2, pos[1] - self.rect.h / 2)
        self.target = pg.Vector2(pos_target)

    def load_images(self):
        self.cell = loadify('images/celula.png')
        self.cell = pg.transform.smoothscale(self.cell, [cell_size] * 2)

    def update(self):
        move = self.target - self.pos
        move_length = move.length()

        if move_length < self.speed:
            self.pos = self.target
        elif move_length != 0:
            move.normalize_ip()
            move = move * self.speed
            self.pos += move
        self.rect.topleft = list(int(v) for v in self.pos)


class CariotecaSprite(pg.sprite.Sprite):
    def __init__(self, celulasprite, color=(20, 25, 20), transportando=False):
        super().__init__()
        self.image = pg.Surface((cell_size * 0.25, cell_size * 0.33)).convert_alpha()
        self.rect = self.image.get_rect()
        self.celulasprite = celulasprite
        self.rect.center = self.celulasprite.rect.center + pg.Vector2(cell_size * 0.27, 0)
        self.color = color
        self.transportando = transportando

    def update(self):
        if self.transportando:
            self.color = (255, 255, 255)
            self.transportando = False
        else:
            self.color = (20, 25, 20)
        pg.draw.ellipse(self.celulasprite.image, self.color, self.rect, 1)


class CloroplastoSprite(pg.sprite.Sprite):
    def __init__(self, celulasprite):
        super().__init__()
        self.transportando = False
        self.image = pg.Surface((cell_size * 0.11, cell_size * 0.17)).convert_alpha()
        self.rect = self.image.get_rect()
        self.celulasprite = celulasprite
        self.rect.center = self.celulasprite.rect.center - pg.Vector2(cell_size * 0.2, cell_size * 0.08)

    def update(self):
        if self.transportando:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 255, 0, 200)
        pg.draw.ellipse(self.celulasprite.image, self.color, self.rect)


class Flagelos(pg.sprite.Sprite):
    def __init__(self, celulasprite):
        super().__init__()
        self.celulasprite = celulasprite
        self.image = pg.Surface((cell_size * 0.25, cell_size * 0.6)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()

    def update(self):
        self.pos = self.celulasprite.pos + pygame.Vector2(20, -32)
        pygame.gfxdraw.bezier(self.image,
                              [(self.rect.x/2, 0), (self.rect.x/2 + 15, 0), (self.rect.x/2 + 15, 40),
                               (self.rect.x/2 + 15, 60)], 2, (0, 0, 0))



class LeftGui(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((100, 100)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = (max_width * 0.15, max_height * 0.2)
        self.load_images()

        pg.draw.rect(self.image, (255, 255, 255), self.rect, 0, 30)

        self.image.blit(self.dna_icon, (self.rect.x + 5, self.rect.y + 10))

    def load_images(self):
        self.dna_icon = loadify('images/dna_icon.png')
        self.dna_icon = pg.transform.smoothscale(self.dna_icon, (90, 90))


class BottomGui(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((max_width * 0.2, max_height * 0.05))
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = (max_width / 6, max_height * 0.7)
        self.show = True
        self.cor = (0, 150, 150, 80)
        self.quick_alpha = 100

        self.tamanho_buttons = (max_width * 0.01, max_width * 0.01)
        # quick acess button 1
        self.quick_acess_a = pg.Rect((0, 0), self.tamanho_buttons)
        self.quick_acess_a.center = (self.rect.x + (self.rect.w / 6) * 1, self.rect.y + self.rect.h / 2)
        # quick acess button 2
        self.quick_acess_b = pg.Rect((0, 0), self.tamanho_buttons)
        self.quick_acess_b.center = (self.rect.x + (self.rect.w / 6) * 3, self.rect.y + self.rect.h / 2)
        # quick acess buttom 3
        self.quick_acess_c = pg.Rect((0, 0), self.tamanho_buttons)
        self.quick_acess_c.center = (self.rect.x + (self.rect.w / 6) * 5, self.rect.y + self.rect.h / 2)

    def update(self):
        if not self.show:
            self.cor = (0, 0, 0, 0)
            self.quick_alpha = 100
        else:
            self.cor = (0, 150, 150)
            self.quick_alpha = 255

        pg.draw.rect(self.image, self.cor, self.rect, 0, 80)
        pg.draw.rect(self.image, (0, 255, 0, self.quick_alpha), self.quick_acess_a, 0, 15)
        pg.draw.rect(self.image, (0, 255, 255, self.quick_alpha), self.quick_acess_b, 0, 15)
        pg.draw.rect(self.image, (255, 255, 0, self.quick_alpha), self.quick_acess_c, 0, 15)


class RightGui(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((max_width * 0.6, max_height * 0.054)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0, 0))
        self.pos = (max_width * 0.22, max_height * 0.2)
        self.collapse = True
        self.collapsed = False

        pg.draw.rect(self.image, (250, 250, 250), self.rect, 100, 30)


class SubstanciaSprite(pg.sprite.Sprite):
    def __init__(self, substancia):
        super().__init__()
        self.image = pg.Surface((10, 10)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = self.set_randompos()
        self.substancia = substancia

        self.tick = -3
        self.animator = 7
        self.direction = 1
        if self.substancia == "Água":
            self.draw_agua()
        elif self.substancia == "CO2":
            self.draw_dioxidocarbono()

    def set_randompos(self):
        return randint(int(max_width * 0.2), int(max_height * 0.8)), randint(int(max_width * 0.2),
                                                                             int(max_height * 0.8))

    def draw_agua(self):
        pg.draw.ellipse(self.image, (0, 0, 255), self.rect, 7)

    def draw_dioxidocarbono(self):
        pg.draw.ellipse(self.image, (30, 30, 30), self.rect, 5)

    def glitch(self, xaxis=0, yaxis=0):
        self.pos = (self.pos[0] + xaxis, self.pos[1] + yaxis)

    def update(self):
        radius = 10
        if self.tick < - radius and self.tick > radius:
            self.tick += self.direction
        if self.tick == - radius + 1 or self.tick == radius - 1:
            self.direction *= -1
        self.glitch(self.direction / 30)

def loadify(imgname):
    return pg.image.load(imgname).convert_alpha()
