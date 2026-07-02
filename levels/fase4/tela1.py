import pygame

import settings
from classes.enemy import Colosso
from core.game_state import GameState
from core.level import Level


class Fase4Tela1(Level):
    FUNDO = "assets/fase4/fase4-tela1.png"

    DIALOGOS = [
        "O Cofre de Aurum. Montanhas de ouro ao redor de um trono vazio.",
        "Vazio porque o verdadeiro guardiao ainda dorme dentro dele.",
        "O Colosso Mecanico desperta. Placas se abrem, a marreta se ergue.",
        "Uma engrenagem pulsa no peito dele. O ponto fraco. Desviar, golpear, sobreviver.",
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 90, settings.LARGURA_TELA, 90),
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)

        y_chao = settings.ALTURA_TELA - 90
        self.boss = Colosso(
            820,
            y_chao - settings.COLOSSO_ALTURA_SPRITE,
            40,
            settings.LARGURA_TELA - 40,
            self.player,
        )
        self.grupo_inimigos.add(self.boss)

        self.fonte_boss = pygame.font.Font(None, 28)

    def atualizar(self):
        super().atualizar()

        if self.dialogo_ativo or self.estado != GameState.PLAYING:
            return

        # se a marretada do boss acertar o player, tira vida dele
        hitbox = self.boss.hitbox_marreta()
        if hitbox is not None and self.player.rect.colliderect(hitbox):
            self.player.levar_dano(settings.COLOSSO_DANO_MARRETA)

        if not self.player.esta_vivo():
            self.estado = GameState.GAME_OVER

    def desenhar(self, tela):
        self.boss.desenhar_efeito_estado(tela)
        super().desenhar(tela)

        if self.boss.alive():
            self._desenhar_barra_vida_boss(tela)

    def _desenhar_barra_vida_boss(self, tela):
        largura = 400
        altura = 24
        x = settings.LARGURA_TELA // 2 - largura // 2
        y = 20

        proporcao = max(0, self.boss.vida) / settings.COLOSSO_VIDA
        pygame.draw.rect(tela, (40, 40, 40), (x, y, largura, altura))
        pygame.draw.rect(tela, settings.RED, (x, y, int(largura * proporcao), altura))
        pygame.draw.rect(tela, settings.WHITE, (x, y, largura, altura), 2)

        nome = self.fonte_boss.render("Colosso Mecanico", True, settings.WHITE)
        tela.blit(nome, nome.get_rect(centerx=settings.LARGURA_TELA // 2, bottom=y - 2))

    def terminou(self):
        return self.estado == GameState.PLAYING and len(self.grupo_inimigos) == 0
