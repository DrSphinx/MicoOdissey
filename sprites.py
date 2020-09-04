import pygame as pg
from random import randint
import json

agua = {'Nome': 'Água', 'Color': (0, 0, 255, 100)}
resolution = json.load(open('resolution', 'r'))
max_width = resolution[0]
max_height = resolution[1]
center_x, center_y = max_width/2, max_height/2
cell_size = int(max_width*0.18)


class CelulaSprite(pg.sprite.Sprite):
    def __init__(self, speed=0.5):
        super().__init__()
        self.image = pg.Surface([cell_size] *2).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = pg.Vector2(center_x, center_y)
        self.set_target((center_x, center_y))
        self.speed = speed
        self.load_images()

        self.image.blit(self.cell, self.rect)
        
    def set_target(self, pos):
        pos_target = (pos[0] - self.rect.w/2, pos[1] - self.rect.h/2)
        self.target = pg.Vector2(pos_target)

    def load_images(self):
        self.cell = loadify('images/celula.png')
        self.cell = pg.transform.smoothscale(self.cell, [cell_size]*2)

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
        self.image = pg.Surface((cell_size * 0.11, cell_size * 0.17)).convert_alpha()
        self.rect = self.image.get_rect()
        self.celulasprite = celulasprite
        self.rect.center = self.celulasprite.rect.center - pg.Vector2(cell_size * 0.2, cell_size * 0.08)

    def update(self):
        if self.transportando:
            self.color = (255, 255, 255)
            self.transportando = False
        else:
            self.color = (0, 255, 0, 200)
        pg.draw.ellipse(self.celulasprite.image, self.color, self.rect)


class LeftGui(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((max_width * 0.15, max_height * 0.25)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = (max_width * 0.02, max_height * 0.025)
        self.load_images()
        
        pg.draw.rect(self.image, (255, 255, 255), self.rect, 0, 30)
        self.image.blit(self.lab, (self.rect.x + (self.rect.w * 0.07), self.rect.y))
        self.image.blit(self.dna_icon, (self.rect.x + (self.rect.w * 0.07), self.rect.h * 0.47))
    
    def load_images(self):
        self.lab = loadify('images/lab_icon.png')
        self.lab = pg.transform.smoothscale(self.lab, (int(max_width * 0.12), int(max_height * 0.13)))
        self.dna_icon = loadify('images/dna_icon.png')
        self.dna_icon = pg.transform.smoothscale(self.dna_icon, (int(max_width * 0.13), int(max_height * 0.13)))


class BottomGui(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((max_width * 0.7, max_height * 0.1))
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = (max_width * 0.16, max_height * 0.83)
        self.show = True
        self.cor = (0, 150, 150, 80)
        self.quick_alpha = 100

        self.tamanho_buttons = (max_width * 0.09, max_width * 0.09)
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
        self.image = pg.Surface((max_width * 0.25, max_height * 0.2)).convert_alpha()
        self.rect = self.image.get_rect()
        self.image.fill((0, 0, 0, 0))
        self.pos = (max_width * 0.7, max_height * 0.025)
        self.collapse = True
        self.collapsed = False
        pg.draw.rect(self.image, (250, 250, 250, 80), self.rect, 100, 30)


class SubstanciaSprite(pg.sprite.Sprite):
    def __init__(self, substancia):
        super().__init__()
        self.image = pg.Surface((10, 10)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = self.set_pos()
        self.substancia = substancia
        if self.substancia == "Água":
            self.draw_agua()
        elif self.substancia == "CO2":
            self.draw_dioxidocarbono()

    def set_pos(self):
        return randint(int(max_width*0.2), int(max_height*0.8)), randint(int(max_width*0.2), int(max_height*0.8))

    def draw_agua(self):
        pg.draw.ellipse(self.image, (0, 0, 255), self.rect, 7)

    def draw_dioxidocarbono(self):
        pg.draw.ellipse(self.image, (30, 30, 30), self.rect, 5)

    def update(self): pass


def loadify(imgname):
    return pg.image.load(imgname).convert_alpha()
