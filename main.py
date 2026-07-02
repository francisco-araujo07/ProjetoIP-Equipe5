import os
import sys

#  localizar corretamente as pastas 'core', 'classes' e 'levels'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.game import Game

if __name__ == "__main__":
    # Inicializa o gerenciador principal do jogo
    gilded_shadows = Game()
    
    # roda o jogo (menu, fases, pausa)
    gilded_shadows.rodar()