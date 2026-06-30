import pygame

import settings
from core.level import Level


class Fase1Tela3(Level):
    FUNDO = "assets/fase1/fase1-bg3-comespada.png"
    FUNDO_SEM_ESPADA = "assets/fase1/fase1-bg3-semespada.png"
    DIALOGOS = [
        "Os corredores ainda cheiram a pedra umida e tempo perdido.",
        "Tudo exatamente como eu deixei. Cada detalhe, cada sombra.",
        "Exceto isso.",
        "Uma espada esquecida num pedestal de pedra. Simples. Direta.",
        "Servira.",
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)
        fundo_sem_espada = pygame.image.load(self.FUNDO_SEM_ESPADA).convert()
        self.fundo_sem_espada = pygame.transform.scale(
            fundo_sem_espada,
            (settings.LARGURA_TELA, settings.ALTURA_TELA),
        )

        if self.player.tem_espada:
            self.fundo = self.fundo_sem_espada

        self.pedestal_rect = pygame.Rect(
            settings.LARGURA_TELA // 2 - 35,
            settings.ALTURA_TELA - 252,
            70,
            100,
        )
        self.fonte_prompt = pygame.font.Font(None, 30)

    def processar_evento(self, evento):
        if self.dialogo_ativo:
            super().processar_evento(evento)
            return

        if (
            evento.type == pygame.KEYDOWN
            and evento.key == pygame.K_e
            and not self.player.tem_espada
            and self.player.rect.colliderect(self.pedestal_rect)
        ):
            self.player.tem_espada = True
            self.player.dano = settings.PLAYER_DANO
            self.player.atualizar_visual()
            self.fundo = self.fundo_sem_espada
            self.salvar_estado_jogador()
            return

        super().processar_evento(evento)

    def desenhar(self, tela):
        super().desenhar(tela)

        if (
            not self.player.tem_espada
            and self.player.rect.colliderect(self.pedestal_rect)
            and not self.dialogo_ativo
        ):
            prompt = self.fonte_prompt.render("[E] Pegar espada", True, settings.WHITE)
            tela.blit(prompt, (self.pedestal_rect.x - 55, self.pedestal_rect.y - 42))

    def terminou(self):
        return super().terminou() and self.player.tem_espada
