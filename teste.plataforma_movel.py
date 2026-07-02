# teste_plataforma_movel.py
import pygame
import settings
from classes.player import Player
from classes.plataforma import Plataforma, PlataformaMovel

pygame.init()
tela = pygame.display.set_mode((settings.LARGURA_TELA, settings.ALTURA_TELA))
clock = pygame.time.Clock()

chao = Plataforma(0, settings.ALTURA_TELA - 40, settings.LARGURA_TELA, 40)
chao.image.fill(settings.GRAY)

movel_x = PlataformaMovel(200, 400, 120, 20, destino=800, velocidade=3, eixo="x")
movel_x.image.fill(settings.ORANGE)

movel_y = PlataformaMovel(1000, 200, 100, 20, destino=550, velocidade=2, eixo="y")
movel_y.image.fill(settings.BLUE)

plataformas = pygame.sprite.Group(chao, movel_x, movel_y)
player = Player(100, settings.ALTURA_TELA - 210)

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            player.pular()

    plataformas.update()
    player.update(plataformas)

    tela.fill(settings.BLACK)
    plataformas.draw(tela)
    tela.blit(player.image, player.rect)
    pygame.display.flip()
    clock.tick(settings.FPS)

pygame.quit()