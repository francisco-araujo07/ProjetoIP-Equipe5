import pygame
import settings
from classes.player import Player
from classes.coletavel import Collectible
from classes.plataforma import Plataforma, resolver_colisao_chao

# Classe base para todos os níveis do jogo.
# Cada tela concreta herda desta classe e define apenas FUNDO e LAYOUT_PLATAFORMAS.
class Level:

    FUNDO = None            # Caminho da imagem de fundo — obrigatório nas subclasses
    LAYOUT_PLATAFORMAS = [] # Lista de tuplas (x, y, largura, altura[, caminho_imagem])

    def __init__(self):
        self.player = Player(100, settings.ALTURA_TELA - 400)  # Posição inicial do jogador (x, y)
        self.plataformas = pygame.sprite.Group()
        self.coletaveis = pygame.sprite.Group()

        self.criar_plataformas()

        # Carrega e escala o fundo uma única vez para não repetir a operação a cada frame
        fundo = pygame.image.load(self.FUNDO).convert()
        self.fundo = pygame.transform.scale(fundo, (settings.LARGURA_TELA, settings.ALTURA_TELA))

    """ Cria as plataformas a partir dos parâmetros definidos em LAYOUT_PLATAFORMAS.
    Cada entrada pode ter 4 valores (sem imagem) ou 5 (com imagem).
    Sem imagem a plataforma fica invisível e serve apenas para colisão. """
    def criar_plataformas(self):
        for entrada in self.LAYOUT_PLATAFORMAS:
            x, y, largura, altura = entrada[:4]  # Primeiros 4 valores são sempre obrigatórios
            caminho_imagem = entrada[4] if len(entrada) > 4 else None  # 5º valor (imagem) é opcional
            plataforma = Plataforma(x, y, largura, altura, caminho_imagem)
            self.plataformas.add(plataforma)

    def atualizar(self):
        self.player.update()                             # Atualiza o estado do jogador (movimento, física, etc.)
        resolver_colisao_chao(self.player, self.plataformas)  # Verifica e resolve colisões com as plataformas

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))          # Desenha o fundo
        self.plataformas.draw(tela)            # Desenha as plataformas
        tela.blit(self.player.image, self.player.rect)  # Desenha o jogador

    # Retorna True quando o jogador completou a tela; subclasses sobrescrevem quando necessário
    def terminou(self):
        return False
