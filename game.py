from pog_free import *
import pygame as pg
import pygame.freetype
import sys


def loadify(imgname):
    return pg.image.load(imgname).convert_alpha()


# Incie pg
pg.init()

# tela de jogo 
janela = pg.display.set_mode((500, 600))
rect_janela = janela.get_rect()

# Gui rects
left_rect = pg.Rect(rect_janela.w * 0.02, rect_janela.h * 0.03, rect_janela.w * 0.15, rect_janela.h * 0.26)

bottom_rect = pg.Rect((0, 0), (rect_janela.w * 0.7, rect_janela.h * 0.1))
bottom_rect.center = (rect_janela.w / 2, rect_janela.h / 1.1)
# quick acess button 1
quick_acess_a = pg.Rect((0, 0), (45, 45))
quick_acess_a.center = (bottom_rect.x + (bottom_rect.w / 6) * 1, bottom_rect.y + bottom_rect.h / 2)
# quick acess button 2
quick_acess_b = pg.Rect((0, 0), (45, 45))
quick_acess_b.center = (bottom_rect.x + (bottom_rect.w / 6) * 3, bottom_rect.y + bottom_rect.h / 2)
# quick acess buttom 3
quick_acess_c = pg.Rect((0, 0), (45, 45))
quick_acess_c.center = (bottom_rect.x + (bottom_rect.w / 6) * 5, bottom_rect.y + bottom_rect.h / 2)
quick_acess_b.center = (bottom_rect.x + (bottom_rect.w / 6) * 3, bottom_rect.y + bottom_rect.h / 2)

# Right rects
right_rect = pg.Rect((rect_janela.w * 0.67, rect_janela.h * 0.034), (rect_janela.w * 0.27, rect_janela.h * 0.2))

# pos celula
pos = [rect_janela.w / 2, rect_janela.h / 2]

# objeto clock
clock = pg.time.Clock()

# define fonte
pygame.freetype.init()
myfont = pg.freetype.SysFont('Comic Sans MS', 15)

# adrenalina = Particula("Adrenalina", transportando=True, destino="Cloroplasto")
gas_carbonico = Particula("CO2", transportando=True, destino="Cloroplasto")
agua = Particula("Água", transportando=True, destino="Cloroplasto")

# cria um objeto Celulla
celula = Celula()
celula.citoplasma.energia += 50
celula.fonte_luz = FonteLuz(700, 1)

ocupa_interior(celula.membrana, gas_carbonico)
ocupa_interior(celula.citoplasma, agua)

count = 0
pressed = False

cell_rect = pg.Rect(pos[0], pos[1], 150, 90)

lab = loadify('images/lab_icon.png')
lab = pg.transform.smoothscale(lab, (70, 85))
dna_icon = loadify('images/dna_icon.png')
dna_icon = pg.transform.smoothscale(dna_icon, (70, 85))
pressed, cell_pressed = False, False
quick_a_descr = False


def acesso_primeiro():
    ocupa_interior(celula.citoplasma, Particula("Água", transportando=True, destino="Cloroplasto"))
    ocupa_interior(celula.citoplasma, Particula("CO2", transportando=True, destino="Cloroplasto"))
    celula.transporte_passivo()
    celula.cloroplastos.inventario()


while True:  # main game loop
    clock.tick(120)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN and cell_rect.collidepoint(event.pos):
            cell_pressed = True
            pg.mouse.get_rel()
        elif event.type == pg.MOUSEBUTTONDOWN and quick_acess_a.collidepoint(event.pos):
            celula.gera_energia()  # PROCESSO DE FOTOSSINTESE
        elif event.type == pg.MOUSEMOTION and quick_acess_a.collidepoint(event.pos):
            quick_a_descr = True
        elif event.type == pg.MOUSEMOTION and not quick_acess_a.collidepoint(event.pos):
            quick_a_descr = False
        elif event.type == pg.MOUSEBUTTONDOWN and quick_acess_b.collidepoint(event.pos):
            acesso_primeiro()  # ADICIONA RECURSOS PARA FOTOSSINTESE
        elif event.type == pg.MOUSEBUTTONUP and cell_rect.collidepoint(event.pos):
            cell_pressed = False

    janela.fill((253, 253, 150))

    # GUI 

    # LEFT GUI
    pg.draw.rect(janela, (255, 255, 255), left_rect, 0, 30)
    janela.blit(lab, (left_rect.x, left_rect.y))
    janela.blit(dna_icon, (left_rect.x, left_rect.h - 65))

    # BOTTOM GUI
    pg.draw.rect(janela, (0, 150, 150, 80), bottom_rect, 0, 80)
    pg.draw.rect(janela, (0, 255, 0), quick_acess_a, 0, 15)
    pg.draw.rect(janela, (0, 255, 255), quick_acess_b, 0, 15)
    pg.draw.rect(janela, (255, 255, 255), quick_acess_c, 0, 15)
    descr_surf, descr = myfont.render(f"Gerar energia", (0, 0, 0))

    # RIGHT GUI
    # contadores
    pg.draw.rect(janela, (250, 250, 250, 80), right_rect, 0, 30)
    # contador de energia
    ec_surf, energia_counter = myfont.render(f"ENERGIA: {round(celula.citoplasma.energia)}", (0, 0, 0))
    energia_counter.center = (right_rect.x + right_rect.w / 2, right_rect.y + right_rect.height / 8)
    # contador de água
    ac_surf, agua_counter = myfont.render(f"AGUA: {celula.cloroplastos.recursos['Água']}", (0, 0, 0))
    agua_counter.center = (right_rect.x + right_rect.w / 2, right_rect.y + right_rect.height / 8 * 3)
    # contador de carbono
    co_surf, co_counter = myfont.render(f"CO₂: {celula.cloroplastos.recursos['CO2']}", (0, 0, 0))
    co_counter.center = (right_rect.x + right_rect.w / 2, right_rect.y + right_rect.height / 8 * 5)
    # contador de oxigenio
    o_surf, o_counter = myfont.render(f"O₂: {celula.cloroplastos.recursos['O2']}", (0, 0, 0))
    o_counter.center = (right_rect.x + right_rect.w / 2, right_rect.y + right_rect.height / 8 * 7)

    janela.blit(ec_surf, energia_counter)
    janela.blit(ac_surf, agua_counter)
    janela.blit(co_surf, co_counter)
    janela.blit(o_surf, o_counter)

    # desenha a célula
    if cell_pressed:
        cell_rect.move_ip(pg.mouse.get_rel())
        pos[0] = cell_rect.x
        pos[1] = cell_rect.y

    undercell_rect = pg.Rect(cell_rect.x + 2, cell_rect.y + 2, 140, 85)
    pg.draw.ellipse(janela, (0, 150, 150, 150), cell_rect)
    pg.draw.ellipse(janela, (175, 255, 250, 100), undercell_rect)
    celula.cloroplastos.draw(janela, cell_rect)

    if quick_a_descr:
        janela.blit(descr_surf, (quick_acess_a.x - 40, quick_acess_a.y - 30))
    # pg.draw.circle(janela, (60, 60, 60, 10), (pos[0] + 100, pos[1] + 100), 17)

    # update e round ++)
    pg.display.update()
    count += 1

    if count % 30 == 0:
        celula.t += 1

# controle.desenha(janela)
# ev = pg.event.wait()

# if ev.type == TIMEREVENT:
#    controle.desenha(janela)
#    pg.display.flip()
# else:
#    controle.evento(ev)

# if (ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE) or ev.type == pg.QUIT:
#    break
