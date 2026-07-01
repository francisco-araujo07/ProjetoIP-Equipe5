import settings
from classes.coletavel import Pocao
from classes.enemy import Saqueador
from core.level import Level


class Fase2Tela2(Level):
    FUNDO = "assets/fase2/fase2-tela2.png"
    DIALOGOS = [
        "Dois guardas. Aurum colocou mais gente desde a ultima vez que passei por aqui.",
        "Eles ainda usam o padrao de patrulha que eu mesmo escrevi no manual do castelo.",
        "Isso significa que conheco cada ponto cego deles.",
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)
        y_chao = settings.ALTURA_TELA - 152
        s1 = Saqueador(250, y_chao - 56, 80, 560)
        s2 = Saqueador(950, y_chao - 56, 640, 1200)
        self.grupo_inimigos.add(s1, s2)

        pocao = Pocao(600, y_chao - 32)
        self.coletaveis.add(pocao)

    def terminou(self):
        return super().terminou() and len(self.grupo_inimigos) == 0
