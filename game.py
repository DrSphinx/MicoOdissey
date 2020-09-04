from classes import *
import pygame as pg
import pygame.freetype
import sys
import sprites
from random import choice
import json


# apenas para fins de teste
particulas = {"Água": Particula("Água", transportando=True, destino="Cloroplasto"), "CO2": Particula("CO2", transportando=True, destino="Cloroplasto")}



# Incie pg
pg.init()

# tela de jogo 
janela = pg.display.set_mode((500, 600))
rect_janela = janela.get_rect()

# salva a resolução num arquivo resolution
json.dump((janela.get_width(), janela.get_height()), open('resolution', 'w'))

# objeto clock
clock = pg.time.Clock()

# define fonte
pygame.freetype.init()
myfont = pg.freetype.SysFont('Comic Sans MS', int(janela.get_width() * 0.03))
myfont_b = pg.freetype.SysFont('Comic Sans MS', int(janela.get_width() * 0.02))

# define particulas de teste
adrenalina = Particula("Adrenalina", transportando=True, destino="Cloroplasto")
gas_carbonico = Particula("CO2", transportando=True, destino="Cloroplasto")
agua = Particula("Água", transportando=True, destino="Cloroplasto")

# cria um objeto Celula
celula = Celula()
celula.citoplasma.energia = 2.5
celula.fonte_luz = FonteLuz(1, 1)

# Flags
count = 0
quick_a_descr = False
quick_b_descr = False
quick_c_descr = False
bottom_show = True
r_collapse = False

# Sprites
sprite_celula = sprites.CelulaSprite(speed=((janela.get_width() + janela.get_height()) * 0.001))
left_gui = sprites.LeftGui()
bottom_gui = sprites.BottomGui()
right_gui = sprites.RightGui()
carioteca = sprites.CariotecaSprite(sprite_celula)
cloroplasto = sprites.CloroplastoSprite(sprite_celula)

# collidepoints PRECISA DE OTIMIZAÇÃO
if True:
    tamanho_collider = bottom_gui.tamanho_buttons
    quick_a = pg.Rect((bottom_gui.quick_acess_a.x + bottom_gui.pos[0],
                       bottom_gui.quick_acess_a.y + bottom_gui.pos[1]), tamanho_collider)

    quick_b = pg.Rect((bottom_gui.quick_acess_b.x + bottom_gui.pos[0],
                       bottom_gui.quick_acess_b.y + bottom_gui.pos[1]), tamanho_collider)

    quick_c = pg.Rect((bottom_gui.quick_acess_c.x + bottom_gui.pos[0],
                       bottom_gui.quick_acess_c.y + bottom_gui.pos[1]), tamanho_collider)

    bottom_capsule = pg.Rect((bottom_gui.rect.x + bottom_gui.pos[0],
                              bottom_gui.rect.y + bottom_gui.pos[1]), (bottom_gui.image.get_width(),
                                                                       bottom_gui.image.get_height()))

    right_capsule = pg.Rect((right_gui.rect.x + right_gui.pos[0],
                             right_gui.rect.y + right_gui.pos[1]), (right_gui.image.get_width(),
                                                                    right_gui.image.get_height()))

# grupo sprites da celula

celula_group = pg.sprite.Group(sprite_celula, carioteca, cloroplasto)
gui_group = pg.sprite.Group(left_gui, right_gui, bottom_gui)

substancia_group = pg.sprite.Group()
substancias = ["Água", "CO2"]
for i in range(5):
    substancia_group.add(sprites.SubstanciaSprite(choice(substancias)))

while True:  # main game loop
    clock.tick(120)

    # trata os eventos de mouse e sistema
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if quick_a.collidepoint(event.pos):
                celula.gera_energia()  # PROCESSO DE FOTOSSINTESE
            elif quick_a.collidepoint(event.pos):
                quick_a_descr = True
            elif bottom_capsule.collidepoint(event.pos):
                if bottom_show:
                    bottom_show = False
                elif not bottom_show:
                    bottom_show = True
            elif right_capsule.collidepoint(event.pos):
                if r_collapse:
                    r_collapse = False
                elif not r_collapse:
                    r_collapse = True
            else:
                sprite_celula.set_target(pg.mouse.get_pos())
        elif event.type == pg.MOUSEMOTION:
            if quick_a.collidepoint(event.pos):
                quick_a_descr = True
            elif quick_b.collidepoint(event.pos):
                quick_b_descr = True
            elif quick_c.collidepoint(event.pos):
                quick_c_descr = True
            else:
                quick_a_descr = False
                quick_b_descr = False
                quick_c_descr = False

    # animação piscar ao ativar função (transporte ou fotossintese, mudar nome da variavel)
    carioteca.transportando = celula.carioteca.transportando
    cloroplasto.transportando = celula.cloroplastos.transportando

    # flags de animação de transporte
    if carioteca.transportando:
        if count % 30 == 0:
            celula.carioteca.transportando = False
    if cloroplasto.transportando:
        if count % 30 == 0:
            celula.cloroplastos.transportando = False

    # prenche background
    janela.fill((253, 253, 150))

    # contadores PRECISA DE OTIMIZAÇÃO
    ec_surf, energia_counter = myfont.render(f"ENERGIA: {round(celula.citoplasma.energia, 2)}", (0, 0, 0))
    ac_surf, agua_counter = myfont.render(f"      AGUA: {celula.cloroplastos.recursos['Água']}", (0, 0, 0))
    co_surf, co_counter = myfont.render(f"          CO₂: {celula.cloroplastos.recursos['CO2']}", (0, 0, 0))
    o_surf, o_counter = myfont.render(f"            O₂: {celula.cloroplastos.recursos['O2']}", (0, 0, 0))
    fps_surf, fps_rect = myfont.render(f"fps: {round(clock.get_fps())}", (50, 50, 50))

    # descricoes PRECISA DE OTIMIZAÇÃO
    qa_descr_surf, qb_descr = myfont_b.render(f"Gerar Energia", (0, 0, 0))
    qb_descr_surf, qb_descr = myfont_b.render(f"Coletar Água e CO2", (0, 0, 0))
    qc_descr_surf, qc_descr = myfont_b.render(f"Acesso Rapido 3", (0, 0, 0))

    # atualiza sprites da celula e define visibilidade do bottom gui
    celula_group.update()
    bottom_gui.show = bottom_show
    bottom_gui.update()
    substancia_group.update()

    for substancia in substancia_group.sprites():
        janela.blit(substancia.image, substancia.pos)
        if sprite_celula.rect.collidepoint(substancia.pos):
            ocupa_interior(celula.membrana, Particula(substancia.substancia, transportando=True, destino="Cloroplasto"))
            substancia.kill()
            celula.transporte_passivo()
            celula.cloroplastos.inventario()

    if count % 200 == 0:
        substancia_group.add(sprites.SubstanciaSprite(choice(substancias)))

    # desenha sprites
    janela.blit(sprite_celula.image, sprite_celula.pos)
    janela.blit(bottom_gui.image, bottom_gui.pos)
    janela.blit(left_gui.image, left_gui.pos)
    janela.blit(right_gui.image, right_gui.pos)

    # desenha contadores
    espacamento = janela.get_height() * 0.042
    inicio_w = janela.get_width() * 0.04
    inicio_h = janela.get_height() * 0.033

    janela.blit(ec_surf, (right_gui.pos[0] + inicio_w, right_gui.pos[1] + inicio_h))
    janela.blit(ac_surf, (right_gui.pos[0] + inicio_w, right_gui.pos[1] + inicio_h + espacamento))
    janela.blit(co_surf, (right_gui.pos[0] + inicio_w, right_gui.pos[1] + inicio_h + espacamento * 2))
    janela.blit(o_surf, (right_gui.pos[0] + 20, right_gui.pos[1] + inicio_h + espacamento * 3))
    janela.blit(fps_surf, (rect_janela.w / 2 - 25, 10))

    # flags gui
    if quick_a_descr:
        janela.blit(qa_descr_surf, (quick_a.x - 15, quick_a.y - 25))
    if quick_b_descr:
        janela.blit(qb_descr_surf, (quick_b.x - 15, quick_b.y - 25))
    if quick_c_descr:
        janela.blit(qc_descr_surf, (quick_c.x - 15, quick_c.y - 25))

    # atualiza display
    count += 1
    pg.display.flip()
