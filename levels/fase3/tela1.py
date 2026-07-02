import settings
from classes.enemy import Automato
from core.game_state import GameState
from core.level import Level


class Fase3Tela1(Level):
    FUNDO = "assets/fase3/fase3-tela1.png"

    DIALOGOS = [
        "Consigo ouvir o calor antes mesmo de ve-lo. O coracao de latao do castelo.",
        "Tudo aqui se move em um ritmo impiedoso. Um passo em falso e as engrenagens trituram voce.",
        "E Aurum colocou suas sentinelas de metal para patrulhar. Meus antigos prototipos.",
        "Os Automatos sao pesados, blindados. Minha lamina normal vai precisar de tres golpes.",
        "Preciso de precisao... ou de algo que amplifique minha forca.",
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 90, 380, 90),
        (740, settings.ALTURA_TELA - 90, settings.LARGURA_TELA - 740, 90),
    ]

    LAYOUT_PLATAFORMAS_MOVEIS = [
        (390, settings.ALTURA_TELA - 172, 110, 40, 630, 1, "x", settings.IMAGEM_PLATAFORMA_COMUM),
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)

        y_chao = settings.ALTURA_TELA - 90
        automato = Automato(950, y_chao - 64, 780, settings.LARGURA_TELA - 60)
        self.grupo_inimigos.add(automato)

    def atualizar(self):
        super().atualizar()

        if self.dialogo_ativo or self.estado != GameState.PLAYING:
            return

        # se o player cair no poco, morre na hora
        if self.player.rect.top > settings.ALTURA_TELA:
            self.player.vida = 0
            self.estado = GameState.GAME_OVER

    def terminou(self):
        return super().terminou() and len(self.grupo_inimigos) == 0
