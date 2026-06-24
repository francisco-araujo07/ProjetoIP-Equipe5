import pygame
import settings
import game_state
from classes.player import Player
from classes.coletavel import Collectible
from classes.plataforma import Plataforma, resolver_colisao_chao

# Classe que representa o nível do jogo, responsável por atualizar e desenhar os elementos do nível.
class Level:
    def __init__(self):
        self.player = Player(100, settings.ALTURA_TELA - 400)  # Posição inicial do jogador (x, y)
        self.plataformas = pygame.sprite.Group()
        self.coletaveis = pygame.sprite.Group()

        # Guardando parâmetros das plataformas, nesse caso so tem o chão por que é so para teste.
        self.layout_plataformas = [
            #(x, y, largura, altura, caminho da imagem)
            (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),  # Chão invisível — visual vem do fundo
        ]

        self.criar_plataformas()

        fundo = pygame.image.load("assets/fase1/fase1-bg1.png").convert()
        self.fundo = pygame.transform.scale(fundo, (settings.LARGURA_TELA, settings.ALTURA_TELA))





    """ Cria as plataformas a partir dos parâmetros definidos em layout_plataformas.
    Cada entrada pode ter 4 valores (sem imagem) ou 5 (com imagem).
    Sem imagem a plataforma fica invisível e serve apenas para colisão. """
    def criar_plataformas(self):
        for entrada in self.layout_plataformas:
            x, y, largura, altura = entrada[:4]  # Primeiros 4 valores são sempre obrigatórios
            caminho_imagem = entrada[4] if len(entrada) > 4 else None  # 5º valor (imagem) é opcional
            plataforma = Plataforma(x, y, largura, altura, caminho_imagem)
            self.plataformas.add(plataforma)

    #função pra implementação da colisão no futuro
    # def _checar_coletaveis(self):
    #     pegos = pygame.sprite.spritecollide(self.player, self.grupo_coletaveis, True)
    #     for item in pegos:
    #         item.aplicar_efeito(self.player) 

    def atualizar(self):
        self.player.update() # Atualiza o estado do jogador (movimento, física, etc.)
        resolver_colisao_chao(self.player, self.plataformas) # Verifica e resolve colisões entre o jogador e as plataformas
        

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))
        
        self.plataformas.draw(tela)  # Desenha as plataformas
        tela.blit(self.player.image, self.player.rect)  # Desenha o jogador

    def leitura_dano (self):
        tocados = pygame.sprite.spritecollide(self.player, self.grupo_inimigos, False) # Lê os inimigos que tiveram colisão

        for inimigo in tocados:
            self.player.levar_dano(inimigo.dano) # Registra o dano tirando a vida do Player
        
        if not self.player.esta_vivo():
            self.estado = game_state.GAME_OVER # Regista se o jogador morreu pra dar game over

    def terminou(self):
        return False 