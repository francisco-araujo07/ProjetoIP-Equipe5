import settings
from classes.armadilha import ArmadilhaEspinhos
from classes.coletavel import Gema
from classes.enemy import Automato
from classes.plataforma import Plataforma
from core.game_state import GameState
from core.level import Level


class Fase3Tela2(Level):
    FUNDO = "assets/fase3/fase3-tela2.png"

    DIALOGOS = [
        "La em cima, nos dutos de ventilacao... vejo o brilho de uma Gema de Atributo.",
        "Eu a usei para energizar as caldeiras. Se eu a fundir com a minha espada, o latao desses guardas vai rasgar como papel.",
        "O Colosso no final do caminho nao tera chance se eu estiver com ela.",
        "O preco? Um salto cego entre as engrenagens que sobem.",
    ]

    # Chao continuo (sem vao) — uma faixa de espinhos no trecho sob as plataformas
    # verticais substitui o poco mortal: errar o salto custa dano, nao a vida toda.
    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 90, settings.LARGURA_TELA, 90),
    ]

    # Duas plataformas verticais em fase oposta: A comeca embaixo subindo, B comeca em cima descendo.
    # O ponto mais baixo (460) fica acima do alcance da hitbox do player parado no chao (altura do
    # sprite ~120px + espessura da propria plataforma, 40px), pra nao brigar com o chao continuo por
    # baixo dos espinhos. Percurso curto (100px) e lento (1px/frame) pra dar bastante margem de tempo
    # pro salto. Afastadas 80px uma da outra em X pra exigir um pulo de verdade entre elas.
    LAYOUT_PLATAFORMAS_MOVEIS = [
        (470, 460, 110, 40, 360, -1, "y", settings.IMAGEM_PLATAFORMA_COMUM),
        (660, 360, 110, 40, 460, 1, "y", settings.IMAGEM_PLATAFORMA_COMUM),
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)

        # Plataforma da gema fica ao lado do topo do elevador B (nao em cima), so um pulo curto
        # horizontal + uma leve subida — e da pra descer direto andando pro chao B logo depois.
        plataforma_gema = Plataforma(810, 300, 170, 40, settings.IMAGEM_PLATAFORMA_COMUM)
        self.plataformas.add(plataforma_gema)

        gema = Gema(879, 268)
        self.coletaveis.add(gema)

        y_chao = settings.ALTURA_TELA - 90
        a1 = Automato(860, y_chao - 64, 810, 970)
        a2 = Automato(1080, y_chao - 64, 1000, 1170)
        self.grupo_inimigos.add(a1, a2)

        # Faixa de espinhos alargada pra cobrir os dois elevadores, agora mais afastados.
        self.armadilha = ArmadilhaEspinhos((450, y_chao - 50, 340, 60))
        self.armadilha.image.fill(settings.RED)

    def atualizar(self):
        super().atualizar()

        if self.dialogo_ativo or self.estado != GameState.PLAYING:
            return

        self.armadilha.aplicar_dano(self.player)

        if not self.player.esta_vivo():
            self.estado = GameState.GAME_OVER

    def desenhar(self, tela):
        super().desenhar(tela)
        tela.blit(self.armadilha.image, self.armadilha.rect)

    def terminou(self):
        return super().terminou() and len(self.grupo_inimigos) == 0
