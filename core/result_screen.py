import pygame

import settings
from core.game_state import GameState


class ResultScreen:
    TEXTOS = {
        GameState.GAME_OVER: {
            "titulo": "Game Over",
            "mensagem": "Silas caiu antes de concluir sua vinganca.",
        },
        GameState.WIN: {
            "titulo": "Vitoria",
            "mensagem": "O cofre de Aurum foi tomado.",
        },
    }

    def __init__(self, estado):
        self.estado = estado
        self.reiniciar_solicitado = False
        self.sair_solicitado = False
        self.fonte_titulo = pygame.font.Font(None, settings.FONTE_TITULO_RESULTADO)
        self.fonte_texto = pygame.font.Font(None, settings.FONTE_TEXTO_RESULTADO)

    def processar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return

        tecla_reiniciar = pygame.key.key_code(settings.TECLA_REINICIAR_JOGO)
        tecla_sair = pygame.key.key_code(settings.TECLA_SAIR_JOGO)

        if evento.key == tecla_reiniciar:
            self.reiniciar_solicitado = True
        elif evento.key in (tecla_sair, pygame.K_q):
            self.sair_solicitado = True

    def desenhar(self, tela):
        tela.fill(settings.BLACK)

        textos = self.TEXTOS[self.estado]
        titulo = self.fonte_titulo.render(textos["titulo"], True, settings.WHITE)
        mensagem = self.fonte_texto.render(textos["mensagem"], True, settings.WHITE)
        opcoes = self.fonte_texto.render(
            f"[{settings.TECLA_REINICIAR_JOGO.upper()}] Reiniciar   [Esc/Q] Sair",
            True,
            settings.GRAY,
        )

        centro_x = settings.LARGURA_TELA // 2
        centro_y = settings.ALTURA_TELA // 2

        tela.blit(titulo, titulo.get_rect(center=(centro_x, centro_y - 90)))
        tela.blit(mensagem, mensagem.get_rect(center=(centro_x, centro_y)))
        tela.blit(opcoes, opcoes.get_rect(center=(centro_x, centro_y + 70)))
