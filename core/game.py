import pygame

import settings
from core.player_state import PlayerState
from levels.fase1.tela1 import Fase1Tela1
from levels.fase1.tela2 import Fase1Tela2
from levels.fase1.tela3 import Fase1Tela3
from levels.fase1.tela4 import Fase1Tela4
from levels.fase1.tela5 import Fase1Tela5


class Game:
    SEQUENCIA_LEVELS = [
        Fase1Tela1,
        Fase1Tela2,
        Fase1Tela3,
        Fase1Tela4,
        Fase1Tela5,
    ]

    def __init__(self):
        pygame.init()

        self.tela = pygame.display.set_mode((settings.LARGURA_TELA, settings.ALTURA_TELA))
        pygame.display.set_caption(settings.TITULO_TESTE)

        self.clock = pygame.time.Clock()
        self.rodando = True

        self.nivel_atual = 0
        self.player_state = PlayerState()
        self.nivel = self.SEQUENCIA_LEVELS[0](self.player_state)

    def _avancar_nivel(self):
        self.nivel.salvar_estado_jogador()
        self.nivel_atual += 1

        if self.nivel_atual < len(self.SEQUENCIA_LEVELS):
            self.nivel = self.SEQUENCIA_LEVELS[self.nivel_atual](self.player_state)
        else:
            self.rodando = False

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.display.toggle_fullscreen()
            else:
                self.nivel.processar_evento(evento)

    def atualizar(self):
        self.nivel.atualizar()
        if self.nivel.terminou():
            self._avancar_nivel()

    def desenhar(self):
        self.nivel.desenhar(self.tela)
        pygame.display.flip()

    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(settings.FPS)

        pygame.quit()
