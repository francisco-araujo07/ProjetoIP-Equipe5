import pygame

import settings
from core.level import Level
from classes.coletavel import Gema


class Fase3Tela3(Level):
    # TODO: substituir pelos assets reais da Fase 3 quando estiverem prontos
    FUNDO = "assets/fase1/fase1-bg1.png"          # placeholder
    FUNDO_SEM_GEMA = "assets/fase1/fase1-bg1.png"  # placeholder

    DIALOGOS = [
        "No coracao da linha de montagem, algo pulsa com luz propria.",
        "Uma gema. Engastada no aco como se sempre tivesse pertencido aqui.",
        "Sinto o peso dela antes mesmo de tocar.",
        "Com isso, nenhuma armadura do Rei vai segurar o que vem a seguir.",
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)

        fundo_sem_gema = pygame.image.load(self.FUNDO_SEM_GEMA).convert()
        self.fundo_sem_gema = pygame.transform.scale(
            fundo_sem_gema,
            (settings.LARGURA_TELA, settings.ALTURA_TELA),
        )

        # Se o jogador já tem a gema (recarregou a tela), mostra o background sem ela
        if self.player.tem_gema:
            self.fundo = self.fundo_sem_gema

        # Rect invisível sobre o pedestal — mesmo padrão da Fase1Tela3
        self.pedestal_rect = pygame.Rect(
            settings.LARGURA_TELA // 2 - 35,
            settings.ALTURA_TELA - 252,
            70,
            100,
        )
        self.fonte_prompt = pygame.font.Font(None, 30)

    def processar_evento(self, evento):
        # Diálogos têm prioridade
        if self.dialogo_ativo:
            super().processar_evento(evento)
            return

        if (
            evento.type == pygame.KEYDOWN
            and evento.key == pygame.K_e
            and not self.player.tem_gema
            and self.player.rect.colliderect(self.pedestal_rect)
        ):
            # Aplica o efeito via Gema (dobra dano + tem_gema = True)
            gema_temp = Gema(0, 0)
            gema_temp._aplicar_efeito(self.player)

            self.fundo = self.fundo_sem_gema
            self.salvar_estado_jogador()
            return

        super().processar_evento(evento)

    def desenhar(self, tela):
        super().desenhar(tela)

        # Mostra o prompt apenas quando próximo ao pedestal e sem a gema
        if (
            not self.player.tem_gema
            and self.player.rect.colliderect(self.pedestal_rect)
            and not self.dialogo_ativo
        ):
            prompt = self.fonte_prompt.render("[E] Pegar gema", True, settings.WHITE)
            tela.blit(prompt, (self.pedestal_rect.x - 30, self.pedestal_rect.y - 42))

    def terminou(self):
        # Só libera a borda direita após coletar a gema
        return super().terminou() and self.player.tem_gema