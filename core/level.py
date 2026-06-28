import pygame
import settings
from core.game_state import GameState
from classes.player import Player
from classes.coletavel import Collectible
from classes.plataforma import Plataforma, resolver_colisao_chao

# Classe base para todos os níveis do jogo.
# Cada tela concreta herda desta classe e define apenas FUNDO e LAYOUT_PLATAFORMAS.
class Level:

    FUNDO = None            # Caminho da imagem de fundo — obrigatório nas subclasses
    LAYOUT_PLATAFORMAS = [] # Lista de tuplas (x, y, largura, altura[, caminho_imagem])

    def __init__(self):
        self.estado = GameState.PLAYING
        self.player = Player(100, settings.ALTURA_TELA - 400)
        self.plataformas = pygame.sprite.Group()
        self.coletaveis = pygame.sprite.Group()
        self.grupo_inimigos = pygame.sprite.Group()

        self.layout_plataformas = [
            (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),
        ]

        self.criar_plataformas()

        # Carrega e escala o fundo uma única vez para não repetir a operação a cada frame
        fundo = pygame.image.load(self.FUNDO).convert()
        self.fundo = pygame.transform.scale(fundo, (settings.LARGURA_TELA, settings.ALTURA_TELA))

    def criar_plataformas(self):
        for entrada in self.layout_plataformas:
            x, y, largura, altura = entrada[:4]
            caminho_imagem = entrada[4] if len(entrada) > 4 else None
            plataforma = Plataforma(x, y, largura, altura, caminho_imagem)
            self.plataformas.add(plataforma)

    def processar_evento(self, evento):
        tecla_ataque = pygame.key.key_code(settings.TECLA_ATAQUE_PLAYER)
        if evento.type == pygame.KEYDOWN and evento.key == tecla_ataque:
            self.player.atacar()

    def atualizar(self):
        self.player.update()
        resolver_colisao_chao(self.player, self.plataformas)
        self.leitura_dano()

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

        self.plataformas.draw(tela)
        tela.blit(self.player.image, self.player.rect)

        hitbox = self.player.hitbox_ataque()
        if hitbox is not None:
            pygame.draw.rect(tela, settings.ORANGE, hitbox, 2)

    def leitura_dano(self):
        tocados = pygame.sprite.spritecollide(self.player, self.grupo_inimigos, False)

        for inimigo in tocados:
            self.player.levar_dano(inimigo.dano)

        if not self.player.esta_vivo():
            self.estado = GameState.GAME_OVER

    def terminou(self):
        return False
