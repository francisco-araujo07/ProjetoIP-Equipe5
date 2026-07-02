import settings
from core.level import Level


class Fase1Tela2(Level):
    FUNDO = "assets/fase1/fase1-bg2.png"
    DIALOGOS = [
        "Lembro quando inaugurei este portao. O rei sorriu.",
        "'Ninguem entra aqui sem minha permissao', ele disse.",
        "Eu sorri de volta. Porque fui eu quem projetou a falha.",
        "Esta noite eu levo tudo. O tesouro, a dignidade, a historia.",
        "Silas atravessa o portao.",
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),
    ]
