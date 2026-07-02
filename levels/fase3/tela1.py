import settings
from core.level import Level


class Fase3Tela1(Level):
    FUNDO = "assets/fase3/fase3-tela1.png"
    DIALOGOS = [
        "Consigo ouvir o calor antes mesmo de vê-lo. O coração de latão do castelo."
        "Tudo aqui se move em um ritmo impiedoso. Um passo em falso e as engrenagens trituram você."
        "E Aurum colocou suas sentinelas de metal para patrulhar. Meus antigos protótipos."
        "Os Autômatos são pesados, blindados. Minha lâmina normal vai precisar de três golpes."
        "Preciso de precisão... ou de algo que amplifique minha força."
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),
    ]
    def terminou(self):
        return super().terminou() and self.fragmento_coletado