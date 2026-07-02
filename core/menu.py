import pygame
import sys

class TelaIntroducao:
    def __init__(self, tela):
        self.tela = tela
        
        # Carrega e escala a imagem de fundo do cofre real
        self.background = pygame.image.load("assets/menu/menu_principal.png").convert()
        self.background = pygame.transform.scale(self.background, (1280, 720))
        
        # Caixas de colisão invisíveis sintonizadas com a arte da IA
        self.rect_iniciar = pygame.Rect(470, 495, 340, 90)
        self.rect_sair = pygame.Rect(490, 605, 300, 80)
        self.cor_seletor = (212, 175, 55)
        
        # Flags de controle idênticas ao padrão da sua ResultScreen
        self.iniciar_solicitado = False
        self.sair_solicitado = False

    def processar_evento(self, evento):
        """Processa cliques apenas quando o loop principal do jogo requisitar."""
        posicao_mouse = pygame.mouse.get_pos()
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_iniciar.collidepoint(posicao_mouse):
                self.iniciar_solicitado = True
            elif self.rect_sair.collidepoint(posicao_mouse):
                self.sair_solicitado = True

    def desenhar(self, superficie):
        """Renderiza o fundo e calcula os efeitos dinâmicos de foco (Hover)."""
        posicao_mouse = pygame.mouse.get_pos()
        
        # Blit da imagem gerada pela IA
        superficie.blit(self.background, (0, 0))
        
        # Desenha marcadores poligonais discretos nas laterais caso o mouse aponte para o botão
        if self.rect_iniciar.collidepoint(posicao_mouse):
            pygame.draw.polygon(superficie, self.cor_seletor, [(430, 530), (430, 550), (450, 540)])
            pygame.draw.polygon(superficie, self.cor_seletor, [(850, 530), (850, 550), (830, 540)])
        elif self.rect_sair.collidepoint(posicao_mouse):
            pygame.draw.polygon(superficie, self.cor_seletor, [(450, 635), (450, 655), (470, 645)])
            pygame.draw.polygon(superficie, self.cor_seletor, [(830, 635), (830, 655), (810, 645)])