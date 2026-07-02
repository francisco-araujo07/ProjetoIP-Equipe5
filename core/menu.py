import pygame
import sys

class TelaIntroducao:
    def __init__(self, tela):
        self.tela = tela
        
        # Carrega e escala a imagem de fundo do cofre real
        self.background = pygame.image.load("assets/menu/menu_principal.png").convert()
        self.background = pygame.transform.scale(self.background, (1280, 720))
        
        # area de clique dos botoes (invisivel, so pra pegar o clique)
        self.rect_iniciar = pygame.Rect(470, 495, 340, 90)
        self.rect_sair = pygame.Rect(490, 605, 300, 80)
        self.cor_seletor = (212, 175, 55)

        # guarda se o jogador clicou em iniciar ou sair
        self.iniciar_solicitado = False
        self.sair_solicitado = False

    def processar_evento(self, evento):
        """Trata o clique nos botoes de iniciar e sair."""
        posicao_mouse = pygame.mouse.get_pos()
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if self.rect_iniciar.collidepoint(posicao_mouse):
                self.iniciar_solicitado = True
            elif self.rect_sair.collidepoint(posicao_mouse):
                self.sair_solicitado = True

    def desenhar(self, superficie):
        """Desenha o fundo e o efeito de quando o mouse passa em cima dos botoes."""
        posicao_mouse = pygame.mouse.get_pos()

        # imagem de fundo do menu
        superficie.blit(self.background, (0, 0))

        # desenha as setinhas do lado do botao quando o mouse passa em cima
        if self.rect_iniciar.collidepoint(posicao_mouse):
            pygame.draw.polygon(superficie, self.cor_seletor, [(430, 530), (430, 550), (450, 540)])
            pygame.draw.polygon(superficie, self.cor_seletor, [(850, 530), (850, 550), (830, 540)])
        elif self.rect_sair.collidepoint(posicao_mouse):
            pygame.draw.polygon(superficie, self.cor_seletor, [(450, 635), (450, 655), (470, 645)])
            pygame.draw.polygon(superficie, self.cor_seletor, [(830, 635), (830, 655), (810, 645)])