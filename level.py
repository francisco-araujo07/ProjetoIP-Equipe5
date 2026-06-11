"""Ponto de entrada do jogo de teste de background e máscara."""

import os
import sys

import pygame

# Garante que imports funcionem a partir da raiz do projeto, mesmo ao executar
# o arquivo diretamente pelo terminal.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.GameLoop import GameLoop
from core.GameState import GameState
from core.Settings import SCREEN_WIDTH, SCREEN_HEIGHT, RENDER_WIDTH, RENDER_HEIGHT, WHITE
from core.classes.Camera import Camera
from core.classes.Player import Player
from level import Level


class Game:
    """Coordena estado, entidades e renderização do loop principal."""

    def __init__(self):
        # Inicializa pygame e cria janela + superfície de render em baixa resolução.
        pygame.init()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self._render_surface = pygame.Surface((RENDER_WIDTH, RENDER_HEIGHT))
        pygame.display.set_caption("Teste de background e mask")

        # Fonte de HUD e estado geral do jogo.
        self._font = pygame.font.SysFont(None, 20)
        self.state = GameState.PLAYING
        self.show_mask = False

        # Carrega nível inicial e configura o controlador do loop.
        self._load_level()
        self._loop = GameLoop(self._screen, self._render_surface)

    def _load_level(self):
        """Carrega cenário, câmera e entidade controlável."""
        base = os.path.join("assets", "level1")
        visual = os.path.join(base, "background.png")
        mask = os.path.join(base, "mask.png")

        # Cria nível a partir de imagem visual + máscara de colisão.
        self.level = Level(visual, mask)
        self.camera = Camera(self.level.width, self.level.height)

        # Busca ponto válido de spawn e posiciona a player inicial.
        spawn_x, spawn_y = self.level.find_spawn_point(24, 24)
        self.player = Player(spawn_x, spawn_y)
        self.camera.update(self.player.rect)

    def reset(self):
        """Reinicia o estado jogável recarregando o nível."""
        self._load_level()

    def handle_event(self, event):
        """Trata atalhos de teclado do jogo."""
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_m:
            # Exibe/oculta máscara de colisão.
            self.show_mask = not self.show_mask
        elif event.key == pygame.K_r:
            # Recarrega fase atual.
            self.reset()
        elif event.key == pygame.K_ESCAPE:
            # Encerra a aplicação.
            pygame.quit()
            sys.exit()

    def update(self, keys):
        """Atualiza entidades e reposiciona a câmera."""
        self.player.update(self.level, keys)
        self.camera.update(self.player.rect)

    def draw(self, surface):
        """Desenha mapa, opcionalmente máscara, player e HUD."""
        self.level.draw(surface, self.camera)

        if self.show_mask:
            self.level.draw_mask(surface, self.camera, alpha=110)

        self.player.draw(surface, self.camera)

        # Texto de ajuda rápido no canto superior esquerdo.
        info = "WASD/Setas: mover | M: máscara | R: reiniciar"
        label = self._font.render(info, True, WHITE)
        surface.blit(label, (8, 8))

    def run(self):
        """Inicia o loop principal."""
        self._loop.run(self)


if __name__ == "__main__":
    game = Game()
    game.run()