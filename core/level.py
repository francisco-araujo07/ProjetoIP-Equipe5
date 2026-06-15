import pygame
import settings

# Classe que representa o nível do jogo, responsável por atualizar e desenhar os elementos do nível.
class Level:
    def __init__(self):
        pass
    #função pra implementação da colisão no futuro
    # def _checar_coletaveis(self):
    #     pegos = pygame.sprite.spritecollide(self.player, self.grupo_coletaveis, True)
    #     for item in pegos:
    #         item.aplicar_efeito(self.player) 

    def atualizar(self):
        pass 

    def desenhar(self, tela):
        tela.fill(settings.BLUE)  # Limpa a tela com preto

    def terminou(self):
        return False 