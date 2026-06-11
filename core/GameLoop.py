"""Loop principal de execução e tratamento de eventos do jogo."""

import pygame
import sys
from core.GameState import GameState
from core.Settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    RENDER_WIDTH, RENDER_HEIGHT,
    FPS, BLACK, WHITE, RED, YELLOW
)


class GameLoop:
    """Centraliza atualização, renderização e eventos globais."""

    def __init__(self, screen, render_surface):
        # Referências de superfícies de exibição e render interno.
        self._screen         = screen
        self._render_surface = render_surface
        # Clock para limitar FPS.
        self._clock          = pygame.time.Clock()
        pygame.font.init()
        # Fontes reservadas para HUDs e mensagens.
        self._font_big   = pygame.font.SysFont(None, 48)
        self._font_small = pygame.font.SysFont(None, 24)

    # ------------------------------------------------------------------ #
    #  LOOP PRINCIPAL                                                      #
    # ------------------------------------------------------------------ #

    def run(self, game):
        """Executa o ciclo infinito de atualização e desenho."""
        while True:
            # Mantém taxa de frames estável.
            self._clock.tick(FPS)
            self._handle_events(game)

            if game.state == GameState.PLAYING:
                # Atualiza estado jogável e redesenha em superfície base.
                keys = pygame.key.get_pressed()
                game.update(keys)
                self._render_surface.fill(BLACK)
                game.draw(self._render_surface)

            # Escala resolução de render para o tamanho atual da janela.
            scaled = pygame.transform.scale(
                self._render_surface, self._screen.get_size()
            )
            # Publica frame final na janela.
            self._screen.blit(scaled, (0, 0))
            pygame.display.flip()

    # ------------------------------------------------------------------ #
    #  EVENTOS                                                             #
    # ------------------------------------------------------------------ #

    def _handle_events(self, game):
        """Processa eventos de janela e teclado."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Fecha aplicação ao receber evento de encerramento.
                pygame.quit()
                sys.exit()

            # Delega eventos específicos para a camada de jogo, se existir.
            if hasattr(game, "handle_event"):
                game.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    # Atalho global para alternar fullscreen.
                    self._toggle_fullscreen()





    # ------------------------------------------------------------------ #
    #  FULLSCREEN                                                          #
    # ------------------------------------------------------------------ #

    def _toggle_fullscreen(self):
        """Alterna entre janela normal e tela cheia."""
        flags = self._screen.get_flags()
        if flags & pygame.FULLSCREEN:
            self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        else:
            self._screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)