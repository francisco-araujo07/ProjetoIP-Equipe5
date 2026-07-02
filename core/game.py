import pygame

import settings
from core.game_state import GameState
from core.player_state import PlayerState
from core.result_screen import ResultScreen
from core.menu import TelaIntroducao
from core.pause_screen import PauseScreen                         
from levels.fase1.tela1 import Fase1Tela1
from levels.fase1.tela2 import Fase1Tela2
from levels.fase1.tela3 import Fase1Tela3
from levels.fase1.tela4 import Fase1Tela4
from levels.fase1.tela5 import Fase1Tela5
from levels.fase2.tela1 import Fase2Tela1
from levels.fase2.tela2 import Fase2Tela2
from levels.fase2.tela3 import Fase2Tela3
from levels.fase3.tela1 import Fase3Tela1


class Game:
    SEQUENCIA_LEVELS = [
        Fase1Tela1,
        Fase1Tela2,
        Fase1Tela3,
        Fase1Tela4,
        Fase1Tela5,
        Fase2Tela1,
        Fase2Tela2,
        Fase2Tela3,
        Fase3Tela1,
    ]

    def __init__(self):
        pygame.init()

        self.tela = pygame.display.set_mode((settings.LARGURA_TELA, settings.ALTURA_TELA))
        pygame.display.set_caption(settings.TITULO_TESTE)

        self.clock = pygame.time.Clock()
        self.rodando = True

        self.estado = GameState.MENU
        self.menu = TelaIntroducao(self.tela)
        self.tela_resultado = None
        self.tela_pausa = None 
        self.nivel_atual = 0
        self.player_state = PlayerState()
        self.nivel = self.SEQUENCIA_LEVELS[0](self.player_state)

    def _reiniciar(self):
        self.estado = GameState.PLAYING
        self.tela_resultado = None
        self.nivel_atual = 0
        self.tela_pausa = None   
        self.player_state = PlayerState()
        self.nivel = self.SEQUENCIA_LEVELS[0](self.player_state)

    def _mostrar_resultado(self, estado):
        self.estado = estado
        self.tela_resultado = ResultScreen(estado)
    
    def _pausar(self):
        self.estado = GameState.PAUSED
        self.tela_pausa = PauseScreen()

    def _avancar_nivel(self):
        self.nivel.salvar_estado_jogador()
        self.nivel_atual += 1

        if self.nivel_atual < len(self.SEQUENCIA_LEVELS):
            self.nivel = self.SEQUENCIA_LEVELS[self.nivel_atual](self.player_state)
        else:
            self._mostrar_resultado(GameState.WIN)

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif self.estado == GameState.PAUSED:
                self.tela_pausa.processar_evento(evento)
            elif self.estado == GameState.MENU:
                self.menu.processar_evento(evento)
            elif self.estado in (GameState.GAME_OVER, GameState.WIN):
                self.tela_resultado.processar_evento(evento)
            else:
                self.nivel.processar_evento(evento)
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()
                    elif evento.key == pygame.key.key_code(settings.TECLA_PAUSAR):
                        self._pausar()  

    def atualizar(self):
        if self.estado == GameState.PAUSED:
            if self.tela_pausa.continuar_solicitado:
                self.estado = GameState.PLAYING
                self.tela_pausa = None
            elif self.tela_pausa.sair_solicitado:
                self.rodando = False
            return      

        if self.estado == GameState.MENU:
            if self.menu.iniciar_solicitado:
                self.estado = GameState.PLAYING
            elif self.menu.sair_solicitado:
                self.rodando = False
            return

        if self.estado in (GameState.GAME_OVER, GameState.WIN):
            if self.tela_resultado.reiniciar_solicitado:
                self._reiniciar()
            elif self.tela_resultado.sair_solicitado:
                self.rodando = False
            return

        self.nivel.atualizar()
        if self.nivel.estado == GameState.GAME_OVER:
            self._mostrar_resultado(GameState.GAME_OVER)
            return

        if self.nivel.terminou():
            self._avancar_nivel()

    def desenhar(self):
        if self.estado == GameState.PAUSED:
            self.nivel.desenhar(self.tela)
            self.tela_pausa.desenhar(self.tela)
        elif self.estado == GameState.MENU:
            self.menu.desenhar(self.tela)
        elif self.estado in (GameState.GAME_OVER, GameState.WIN):
            self.tela_resultado.desenhar(self.tela)
        else:
            self.nivel.desenhar(self.tela)
        pygame.display.flip()

    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(settings.FPS)

        pygame.quit()