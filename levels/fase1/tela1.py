import settings
from core.level import Level

# Tela 1 da Fase 1 — floresta, entrada do castelo
class Fase1Tela1(Level):

    FUNDO = "assets/fase1/fase1-bg1.png"

    LAYOUT_PLATAFORMAS = [
        # (x, y, largura, altura[, caminho_imagem])
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),  # Chão invisível — visual vem do fundo
    ]
