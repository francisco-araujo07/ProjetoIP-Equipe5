import pygame
import settings
from classes.collectible import Collectible
 
 
class Espada(Collectible):
    """
    Coletável de espada.
    A colisão é checada internamente no update — solução temporária
    até o Level ter seu próprio _checar_coletaveis.
    """
 
    def __init__(self, x, y):
        super().__init__(x, y, settings.TIPO_DANO)
 
        # Visual provisório
        self.image = pygame.Surface((24, 40))
        self.image.fill(settings.GRAY)
        self.rect = self.image.get_rect(topleft=(x, y))
 
    def update(self, player):
        if self.rect.colliderect(player.rect):
            self.aplicar_efeito(player)
            self.kill()  # some do mapa
 
    def aplicar_efeito(self, player):
        player.arma = "espada"
        super().aplicar_efeito(player)
        print(f"[ESPADA] equipada | dano → {player.dano}")
 