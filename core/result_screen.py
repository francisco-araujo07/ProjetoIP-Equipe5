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
        self.cor_seletor = (212, 175, 55)  # Dourado para o hover
        
        self.fonte_titulo = pygame.font.Font(None, settings.FONTE_TITULO_RESULTADO)
        self.fonte_texto = pygame.font.Font(None, settings.FONTE_TEXTO_RESULTADO)
        
        # 1. Carrega a arte customizada se o jogador perder
        if self.estado == GameState.GAME_OVER:
            self.background = pygame.image.load("assets/game_over/game_over.png").convert()
            self.background = pygame.transform.scale(self.background, (settings.LARGURA_TELA, settings.ALTURA_TELA))
            
            # Caixas de colisão invisíveis calibradas sobre os botões de game_over.png
            self.rect_reiniciar = pygame.Rect(440, 495, 400, 85)  # "TENTAR NOVAMENTE"
            self.rect_sair = pygame.Rect(440, 605, 400, 80)       # "RETORNAR AO MENU"

        # 2. Carrega a arte customizada com os botões embutidos se o jogador vencer
        elif self.estado == GameState.WIN:
            self.background = pygame.image.load("assets/vitoria/game_wins.png").convert()
            self.background = pygame.transform.scale(self.background, (settings.LARGURA_TELA, settings.ALTURA_TELA))
            
            # Caixas de colisão calibradas sobre os botões metálicos de game_wins.png
            self.rect_reiniciar = pygame.Rect(430, 475, 420, 75)  # "JOGAR NOVAMENTE"
            self.rect_sair = pygame.Rect(430, 580, 420, 75)       # "SAIR DO JOGO"

    def processar_evento(self, evento):
        # 1. Processamento por clique de mouse (Habilitado para Game Over e Vitória)
        if self.estado in (GameState.GAME_OVER, GameState.WIN):
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
        posicao_mouse = pygame.mouse.get_pos()

        # --- TELA DE GAME OVER ---
        if self.estado == GameState.GAME_OVER:
            # Desenha o plano de fundo completo gerado pela IA
            tela.blit(self.background, (0, 0))
            
            # Desenha os triângulos indicadores de foco (Hover) nas laterais dos botões de derrota
            if self.rect_reiniciar.collidepoint(posicao_mouse):
                pygame.draw.polygon(tela, self.cor_seletor, [(400, 525), (400, 545), (420, 535)])
                pygame.draw.polygon(tela, self.cor_seletor, [(880, 525), (880, 545), (860, 535)])
            elif self.rect_sair.collidepoint(posicao_mouse):
                pygame.draw.polygon(tela, self.cor_seletor, [(400, 630), (400, 650), (420, 640)])
                pygame.draw.polygon(tela, self.cor_seletor, [(880, 630), (880, 650), (860, 640)])
                
        # --- TELA DE VITÓRIA ---
        elif self.estado == GameState.WIN:
            # Desenha o plano de fundo triunfante completo (com o Parabéns! e botões nativos)
            tela.blit(self.background, (0, 0))
            
            # Desenha os triângulos indicadores de foco (Hover) nas laterais dos botões de vitória
            if self.rect_reiniciar.collidepoint(posicao_mouse):
                # Alinhados perfeitamente com o botão "JOGAR NOVAMENTE"
                pygame.draw.polygon(tela, self.cor_seletor, [(390, 502), (390, 522), (410, 512)])
                pygame.draw.polygon(tela, self.cor_seletor, [(870, 502), (870, 522), (850, 512)])
            elif self.rect_sair.collidepoint(posicao_mouse):
                # Alinhados perfeitamente com o botão "SAIR DO JOGO"
                pygame.draw.polygon(tela, self.cor_seletor, [(390, 607), (390, 627), (410, 617)])
                pygame.draw.polygon(tela, self.cor_seletor, [(870, 607), (870, 627), (850, 617)])
            
        # --- OUTROS ESTADOS GENÉRICOS ---
        else:
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