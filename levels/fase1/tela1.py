import settings
from core.level import Level


class Fase1Tela1(Level):
    FUNDO = "assets/fase1/fase1-bg1.png"
    DIALOGOS = [
        "Sete anos. Foi quanto tempo passei nessas masmorras.",
        "Nao fui preso por ser fraco. Fui preso por saber demais.",
        "Cada corredor, cada alavanca, cada armadilha daquele castelo... eu projetei.",
        "O Rei Aurum me prometeu liberdade. Me deu correntes.",
        "Hoje, as correntes sao dele.",
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),
    ]
