import pygame
import settings
from classes.player import Player
from classes.coletavel import Collectible
from classes.plataforma import Plataforma, resolver_colisao_chao

# Classe que representa o nível do jogo, responsável por atualizar e desenhar os elementos do nível.
class Level:
    def __init__(self):
        self.player = Player(100, settings.ALTURA_TELA - 80)  # Posição inicial do jogador (x, y)
        self.plataformas = pygame.sprite.Group()
        self.coletaveis = pygame.sprite.Group()

        # Guardando parâmetros das plataformas, nesse caso so tem o chão por que é so para teste.
        self.layout_plataformas = [
            #(x, y, largura, altura)
            (0, settings.ALTURA_TELA - 80, settings.LARGURA_TELA, 80),  # Chão
        ]

        self.criar_plataformas()

        



    #Função que cria as plataformas a partir dos parâmetros definidos em layout_plataformas
    def criar_plataformas(self):
        for (x, y, largura, altura) in self.layout_plataformas:
            plataforma = Plataforma(x, y, largura, altura)
            self.plataformas.add(plataforma)

    def processar_evento(self, evento):
        tecla_ataque = pygame.key.key_code(settings.TECLA_ATAQUE_PLAYER)
        if evento.type == pygame.KEYDOWN and evento.key == tecla_ataque:
            self.player.atacar()

    #função pra implementação da colisão no futuro
    # def _checar_coletaveis(self):
    #     pegos = pygame.sprite.spritecollide(self.player, self.grupo_coletaveis, True)
    #     for item in pegos:
    #         item.aplicar_efeito(self.player) 

    def atualizar(self):
        self.player.update() # Atualiza o estado do jogador (movimento, física, etc.)
        resolver_colisao_chao(self.player, self.plataformas) # Verifica e resolve colisões entre o jogador e as plataformas
        

    def desenhar(self, tela):
        tela.fill(settings.BLACK)  # Limpa a tela com preto
        self.plataformas.draw(tela)  # Desenha as plataformas
        tela.blit(self.player.image, self.player.rect)  # Desenha o jogador

        hitbox = self.player.hitbox_ataque()
        if hitbox is not None:
            pygame.draw.rect(tela, settings.ORANGE, hitbox, 2)


    def terminou(self):
        return False
