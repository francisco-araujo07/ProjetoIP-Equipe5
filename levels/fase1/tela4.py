import settings
from classes.enemy import Saqueador
from core.level import Level


class Fase1Tela4(Level):
    FUNDO = "assets/fase1/fase1-bg4.png"

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 152, 520, 152),
        (760, settings.ALTURA_TELA - 152, settings.LARGURA_TELA - 760, 152),
        (570, settings.ALTURA_TELA - 300, 140, 24),
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)
        y_chao = settings.ALTURA_TELA - 152
        saqueador = Saqueador(900, y_chao - 56, 780, settings.LARGURA_TELA - 80)
        self.grupo_inimigos.add(saqueador)

    def terminou(self):
        return super().terminou() and len(self.grupo_inimigos) == 0
