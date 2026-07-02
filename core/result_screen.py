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
        
        # 1. Carrega a arte customizada se o jogador perder
        if self.estado == GameState.GAME_OVER:
            self.background = pygame.image.load("assets/game_over/game_over.png").convert()
            self.background = pygame.transform.scale(self.background, (settings.LARGURA_TELA, settings.ALTURA_TELA))
            
            # Caixas de colisão invisíveis calibradas sobre os botões de game_over.png
            self.rect_reiniciar = pygame.Rect(440, 495, 400, 85)  # "TENTAR NOVAMENTE"
            self.rect_sair = pygame.Rect(440, 605, 400, 80)       # "RETORNAR AO MENU"
            self.cor_seletor = (212, 175, 55)                     # Dourado para o hover

        # 2. Carrega a belíssima arte customizada com texto embutido se o jogador vencer
        elif self.estado == GameState.WIN:
            self.background = pygame.image.load("assets/vitoria/game_wins.png").convert()
            self.background = pygame.transform.scale(self.background, (settings.LARGURA_TELA, settings.ALTURA_TELA))

    def processar_evento(self, evento):
        # 1. Processamento por clique de mouse (Apenas no Game Over)
        if self.estado == GameState.GAME_OVER:
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                posicao_mouse = pygame.mouse.get_pos()
                if self.rect_reiniciar.collidepoint(posicao_mouse):
                    self.reiniciar_solicitado = True
                    return
                elif self.rect_sair.collidepoint(posicao_mouse):
                    self.sair_solicitado = True
                    return

        # 2. Mantém o suporte original por teclado para ambos os estados
        if evento.type == pygame.KEYDOWN:
            tecla_reiniciar = pygame.key.key_code(settings.TECLA_REINICIAR_JOGO)
            tecla_sair = pygame.key.key_code(settings.TECLA_SAIR_JOGO)

            if evento.key == tecla_reiniciar:
                self.reiniciar_solicitado = True
            elif evento.key in (tecla_sair, pygame.K_q):
                self.sair_solicitado = True

        # Se o usuário apertar ESC na tela de fim de jogo, também retorna/sai
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.sair_solicitado = True

    def desenhar(self, tela):
        if self.estado == GameState.GAME_OVER:
            posicao_mouse = pygame.mouse.get_pos()
            
            # Desenha o plano de fundo completo gerado pela IA
            tela.blit(self.background, (0, 0))
            
            # Desenha os triângulos indicadores de foco (Hover) nas laterais dos botões
            if self.rect_reiniciar.collidepoint(posicao_mouse):
                pygame.draw.polygon(tela, self.cor_seletor, [(400, 525), (400, 545), (420, 535)])
                pygame.draw.polygon(tela, self.cor_seletor, [(880, 525), (880, 545), (860, 535)])
            elif self.rect_sair.collidepoint(posicao_mouse):
                pygame.draw.polygon(tela, self.cor_seletor, [(400, 630), (400, 650), (420, 640)])
                pygame.draw.polygon(tela, self.cor_seletor, [(880, 630), (880, 650), (860, 640)])
                
        elif self.estado == GameState.WIN:
            # Desenha o plano de fundo triunfante completo (com o Parabéns! pixelado nativo)
            tela.blit(self.background, (0, 0))
            
            # Renderiza as instruções de controle para guiar o usuário na base da tela
            texto_opcoes = f"[{settings.TECLA_REINICIAR_JOGO.upper()}] Jogar Novamente   [Esc/Q] Sair"
            opcoes = self.fonte_texto.render(texto_opcoes, True, settings.WHITE)
            opcoes_sombra = self.fonte_texto.render(texto_opcoes, True, settings.BLACK)
            
            centro_x = settings.LARGURA_TELA // 2
            pos_y = settings.ALTURA_TELA - 50  # Posicionado sutilmente acima da margem inferior
            
            # Carimba a sombra deslocada e o texto por cima para destacar das moedas de ouro
            tela.blit(opcoes_sombra, opcoes_sombra.get_rect(center=(centro_x + 2, pos_y + 2)))
            tela.blit(opcoes, opcoes.get_rect(center=(centro_x, pos_y)))
            
        else:
            # Mantém o comportamento em texto original para qualquer outro estado genérico
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