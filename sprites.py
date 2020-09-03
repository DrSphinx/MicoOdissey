import pygame as pg


class CelulaSprite(pg.sprite.Sprite):
    def __init__(self, speed=0.5):
        super().__init__()
        self.image = pg.Surface((100, 60)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = pg.Vector2(300, 300)
        self.set_target((300, 300))
        self.speed = speed
        self.surface_rect = pg.Rect((self.rect.x + self.pos[0], self.rect.y + self.pos[1]), (15, 20))

        undercell_rect = pg.Rect(self.rect.x +3, self.rect.y + 2, self.rect.w - 10, self.rect.h - 5)
        pg.draw.ellipse(self.image, (0, 150, 150), self.rect)
        pg.draw.ellipse(self.image, (175, 255, 250), undercell_rect)
        
    def set_target(self, pos):
        pos_target = (pos[0] - self.rect.w/2, pos[1] - self.rect.h/2)
        self.target = pg.Vector2(pos_target)


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
        self.image = pg.Surface((5, 22)).convert_alpha()
        self.rect = self.image.get_rect()
        self.celulasprite = celulasprite
        self.pos = self.celulasprite.rect.center + pg.Vector2(15, 0)
        self.color = color
        self.transportando = transportando

    def update(self):
        if self.transportando:
            self.color = (255, 255, 255)
            self.transportando = False
        else:
            self.color = (20, 25, 20)
        pg.draw.circle(self.celulasprite.image, self.color, self.pos, 12, 1)


class CloroplastoSprite(pg.sprite.Sprite):
    def __init__(self, celulasprite):
        super().__init__()
        self.image = pg.Surface((10, 15)).convert_alpha()
        self.rect = self.image.get_rect()
        self.celulasprite = celulasprite
        self.rect.center = self.celulasprite.rect.center - pg.Vector2(20, 7)

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
        self.image = pg.Surface((75, 150)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = (10, 15)
        self.load_images()
        
        pg.draw.rect(self.image, (255, 255, 255), self.rect, 0, 30)
        self.image.blit(self.lab, (self.rect.x + 6, self.rect.y))
        self.image.blit(self.dna_icon, (self.rect.x + 6, self.rect.h - 80))
    
    def load_images(self):
        self.lab = loadify('images/lab_icon.png')
        self.lab = pg.transform.smoothscale(self.lab, (60, 80))
        self.dna_icon = loadify('images/dna_icon.png')
        self.dna_icon = pg.transform.smoothscale(self.dna_icon, (65, 80))


class BottomGui(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((350, 60))
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = (75, 500)
        self.show = True
        self.cor = (0, 150, 150, 80)

        # quick acess button 1
        self.quick_acess_a = pg.Rect((0, 0), (45, 45))
        self.quick_acess_a.center = (self.rect.x + (self.rect.w / 6) * 1, self.rect.y + self.rect.h / 2)
        # quick acess button 2
        self.quick_acess_b = pg.Rect((0, 0), (45, 45))
        self.quick_acess_b.center = (self.rect.x + (self.rect.w / 6) * 3, self.rect.y + self.rect.h / 2)
        # quick acess buttom 3
        self.quick_acess_c = pg.Rect((0, 0), (45, 45))
        self.quick_acess_c.center = (self.rect.x + (self.rect.w / 6) * 5, self.rect.y + self.rect.h / 2)

    def update(self):
        if not self.show:
            self.cor = (0, 0, 0, 0)
        else:
            self.cor = (0, 150, 150)

        pg.draw.rect(self.image, self.cor, self.rect, 0, 80)
        pg.draw.rect(self.image, (0, 255, 0), self.quick_acess_a, 0, 15)
        pg.draw.rect(self.image, (0, 255, 255), self.quick_acess_b, 0, 15)
        pg.draw.rect(self.image, (255, 255, 0), self.quick_acess_c, 0, 15)


class RightGui(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((125, 120)).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.pos = (350, 15)
        pg.draw.rect(self.image, (250, 250, 250, 80), self.rect, 0, 30)


def loadify(imgname):
    return pg.image.load(imgname).convert_alpha()
