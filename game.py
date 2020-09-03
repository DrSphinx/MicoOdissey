from classes import *
import pygame as pg
import pygame.freetype
import sys
import sprites


# apenas para fins de teste
def acesso_primeiro():
    ocupa_interior(celula.citoplasma, Particula("Água", transportando=True, destino="Cloroplasto"))
    ocupa_interior(celula.citoplasma, Particula("CO2", transportando=True, destino="Cloroplasto"))
    celula.transporte_passivo()
    celula.cloroplastos.inventario()


# Incie pg
pg.init()

# tela de jogo 
janela = pg.display.set_mode((500, 600))
rect_janela = janela.get_rect()

# objeto clock
clock = pg.time.Clock()

# define fonte
pygame.freetype.init()
myfont = pg.freetype.SysFont('Comic Sans MS', 15)

# define particulas de teste
adrenalina = Particula("Adrenalina", transportando=True, destino="Cloroplasto")
gas_carbonico = Particula("CO2", transportando=True, destino="Cloroplasto")
agua = Particula("Água", transportando=True, destino="Cloroplasto")

# cria um objeto Celula
celula = Celula()
celula.citoplasma.energia = 1
celula.fonte_luz = FonteLuz(1, 1)

# Flags
count = 0
pressed, cell_pressed = False, False
quick_a_descr = False
bottom_show = True

# Sprites
sprite_celula = sprites.CelulaSprite()
left_gui = sprites.LeftGui()
bottom_gui = sprites.BottomGui()
right_gui = sprites.RightGui()

# collidepoints
quick_a = pg.Rect((bottom_gui.quick_acess_a.x + bottom_gui.pos[0],
                   bottom_gui.quick_acess_a.y + bottom_gui.pos[1]), (45, 45))
quick_b = pg.Rect((bottom_gui.quick_acess_b.x + bottom_gui.pos[0],
                   bottom_gui.quick_acess_b.y + bottom_gui.pos[1]), (45, 45))
quick_c = pg.Rect((bottom_gui.quick_acess_c.x + bottom_gui.pos[0],
                   bottom_gui.quick_acess_c.y + bottom_gui.pos[1]), (45, 45))
bottom_capsule = pg.Rect((bottom_gui.rect.x + bottom_gui.pos[0],
                          bottom_gui.rect.y + bottom_gui.pos[1]), (350, 60))

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
            elif quick_b.collidepoint(event.pos):
                acesso_primeiro()  # ADICIONA RECURSOS PARA FOTOSSINTESE
            elif bottom_capsule.collidepoint(event.pos):
                if bottom_show:
                    bottom_show = False
                elif not bottom_show:
                    bottom_show = True
            else:
                sprite_celula.set_target(pg.mouse.get_pos())

    # prenche background
    janela.fill((253, 253, 150))

    # contadores PRECISA DE OTIMIZAÇÃO
    ec_surf, energia_counter = myfont.render(f"ENERGIA: {round(celula.citoplasma.energia)}", (0, 0, 0))
    ac_surf, agua_counter = myfont.render(f"      AGUA: {celula.cloroplastos.recursos['Água']}", (0, 0, 0))
    co_surf, co_counter = myfont.render(f"          CO₂: {celula.cloroplastos.recursos['CO2']}", (0, 0, 0))
    o_surf, o_counter = myfont.render(f"            O₂: {celula.cloroplastos.recursos['O2']}", (0, 0, 0))

    # atualiza sprites da celula e define visibilidade do bottom gui
    sprite_celula.update()
    bottom_gui.show = bottom_show
    bottom_gui.update()

    # desenha sprites
    janela.blit(sprite_celula.image, sprite_celula.pos)
    janela.blit(left_gui.image, left_gui.pos)
    janela.blit(right_gui.image, right_gui.pos)
    janela.blit(bottom_gui.image, bottom_gui.pos)

    # desenha contadores
    janela.blit(ec_surf, (right_gui.pos[0] + 20, right_gui.pos[1] + 20))
    janela.blit(ac_surf, (right_gui.pos[0] + 20, right_gui.pos[1] + 45))
    janela.blit(co_surf, (right_gui.pos[0] + 20, right_gui.pos[1] + 70))
    janela.blit(o_surf, (right_gui.pos[0] + 20, right_gui.pos[1] + 95))

    # atualiza displau
    pg.display.flip()
