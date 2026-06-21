import settings
from core.level import Level

# Tela 2 da Fase 1
# TODO: substituir FUNDO pelo asset correto em assets/fase1/tela2/
# TODO: definir LAYOUT_PLATAFORMAS com as plataformas desta tela
class Fase1Tela2(Level):

    FUNDO = "assets/fase1/fase1-bg1.png"  # placeholder — trocar quando o asset estiver pronto

    LAYOUT_PLATAFORMAS = [
        # (x, y, largura, altura[, caminho_imagem])
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),  # Chão invisível
    ]
