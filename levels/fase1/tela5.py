import settings
from core.level import Level
from classes.coletavel import Pocao, FragmentoChave, Gema

# Tela 5 da Fase 1
# TODO: substituir FUNDO pelo asset correto em assets/fase1/tela5/
# TODO: definir LAYOUT_PLATAFORMAS com as plataformas desta tela
class Fase1Tela5(Level):

    FUNDO = "assets/fase1/fase1-bg1.png"  # placeholder — trocar quando o asset estiver pronto

    LAYOUT_PLATAFORMAS = [
        # (x, y, largura, altura[, caminho_imagem])
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),  # Chão invisível
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)
        chao = settings.ALTURA_TELA - 152

        self.coletaveis.add(Pocao(300, chao - 32))
        self.coletaveis.add(FragmentoChave(500, chao - 32))
        self.coletaveis.add(Gema(700, chao - 32, cor="azul"))