import pygame
import settings


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Imagem do jogador (substitua pelo caminho da sua imagem)
        self.image = pygame.Surface((40,56))
        self.image.fill(settings.BLUE)

        # Rect define a posição e a área de de colisão do jogador
        self.rect= self.image.get_rect(topleft=(x, y))

        # Atributos de movimento
        self.velocidade_y = 0
        self.no_chao = False
        self.velocidade = settings.VELOCIDADE_PLAYER
        self.vida_max = settings.PLAYER_VIDA_MAX
        self.vida = self.vida_max
        self.dano = settings.PLAYER_DANO

    def aplicar_gravidade(self):
        self.velocidade_y += settings.GRAVIDADE
        if self.velocidade_y > settings.VELOCIDADE_MAX_QUEDA:
            self.velocidade_y = settings.VELOCIDADE_MAX_QUEDA
        self.rect.y += self.velocidade_y
        
    def pular(self):
        if self.no_chao:
            self.velocidade_y = -settings.FORCA_PULO
            self.no_chao = False

    
    def update(self):
        teclas = pygame.key.get_pressed()

        # Movimento horizontal
        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade

        # Limitar às bordas laterais
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.LARGURA_TELA:
            self.rect.right = settings.LARGURA_TELA

        # Física vertical
        self.aplicar_gravidade()