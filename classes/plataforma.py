import pygame

class Plataforma(pygame.sprite.Sprite):

    # Representa uma plataforma sólida.
    def __init__(self, x, y, largura, altura, caminho_imagem=None):

        super().__init__()

        if caminho_imagem:
            self.image = pygame.image.load(caminho_imagem).convert_alpha()
            self.image = pygame.transform.scale(self.image, (largura, altura))  # Redimensiona para o tamanho da plataforma
        else:
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)  # Superfície transparente

        self.rect = self.image.get_rect(topleft=(x, y))

def resolver_colisao_x(player, grupo_plataformas):
    colisoes = pygame.sprite.spritecollide(player, grupo_plataformas, False)
    for plat in colisoes:
        if player.velocidade_x > 0:
            player.rect.right = plat.rect.left
        elif player.velocidade_x < 0:
            player.rect.left = plat.rect.right


def resolver_colisao_y(player, grupo_plataformas):
    colisoes = pygame.sprite.spritecollide(player, grupo_plataformas, False)
    player.no_chao = False

    for plat in colisoes:
        if player.velocidade_y > 0:
            player.rect.bottom = plat.rect.top
            player.velocidade_y = 0
            player.no_chao = True
            player.plataforma_atual = plat
        elif player.velocidade_y < 0:
            player.rect.top = plat.rect.bottom
            player.velocidade_y = 0

class PlataformaMovel(Plataforma):
    def __init__(self, x, y, largura, altura, destino, velocidade, eixo="x", caminho_imagem=None):
        super().__init__(x, y, largura, altura, caminho_imagem)
        self.eixo = eixo  # "x" ou "y"
        self.velocidade_x = velocidade if eixo == "x" else 0
        self.velocidade_y = velocidade if eixo == "y" else 0

        if eixo == "x":
            self.pos_inicial = x
            self.pos_final = destino
        else:
            self.pos_inicial = y
            self.pos_final = destino

    def update(self, *args):
        if self.eixo == "x":
            self.rect.x += self.velocidade_x
            pos_atual = self.rect.x
        else:
            self.rect.y += self.velocidade_y
            pos_atual = self.rect.y

        if self.velocidade_x > 0 and pos_atual >= self.pos_final:
            self.rect.x = self.pos_final
            self.velocidade_x *= -1
        elif self.velocidade_x < 0 and pos_atual <= self.pos_inicial:
            self.rect.x = self.pos_inicial
            self.velocidade_x *= -1
        elif self.velocidade_y > 0 and pos_atual >= self.pos_final:
            self.rect.y = self.pos_final
            self.velocidade_y *= -1
        elif self.velocidade_y < 0 and pos_atual <= self.pos_inicial:
            self.rect.y = self.pos_inicial
            self.velocidade_y *= -1