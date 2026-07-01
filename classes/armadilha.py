import pygame

import settings


class ArmadilhaEspinhos:
    def __init__(self, rect, dano=settings.ESPINHOS_DANO):
        self.rect = pygame.Rect(rect)
        self.dano = dano
        self.ativa = True

    def desativar(self):
        self.ativa = False

    def aplicar_dano(self, player):
        if self.ativa and player.rect.colliderect(self.rect):
            player.levar_dano(self.dano)
