import pygame
import settings

class Collectible(pygame.sprite.Sprite):
    CORES = {
        settings.TIPO_VIDA: settings.GREEN,
        settings.TIPO_DANO: settings.RED, 
        settings.TIPO_VELOCIDADE: settings.BLUE 
    }

    def __init__(self, x, y, tipo):
        super().__init__()

        self.tipo = tipo

        # --- Visual ---
        self.image = pygame.Surface((24,24))
        cor = self.CORES.get(tipo, settings.WHITE) #
        self.image.fill(cor)

        self.rect = self.image.get_rect(topleft=(x, y))

    def efeito (self, player):
        #Aumenta um atributo do player

        if self.tipo == settings.TIPO_VIDA:
            player.maxv_vida += settings.UPGRADE_VIDA
        
        elif self.tipo == settings.TIPO_DANO:
            player.dano += settings.UPGRADE_DANO
 
        elif self.tipo == settings.TIPO_VELOCIDADE:
            player.velocidade += settings.UPGRADE_VELOCIDADE