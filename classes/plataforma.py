import pygame

class Plataforma(pygame.sprite.Sprite):

    # Representa uma plataforma sólida.
    def __init__(self, x, y, largura, altura, caminho_imagem=None):

        super().__init__()

        if caminho_imagem:
            self.image = self._carregar_imagem(caminho_imagem, largura, altura)
        else:
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)  # Superfície transparente

        self.rect = self.image.get_rect(topleft=(x, y))

    def _carregar_imagem(self, caminho_imagem, largura, altura):
        # corta as bordas vazias da imagem antes de redimensionar
        imagem = pygame.image.load(caminho_imagem).convert_alpha()
        areas_visiveis = pygame.mask.from_surface(imagem).get_bounding_rects()

        if areas_visiveis:
            area = areas_visiveis[0].copy()
            for rect in areas_visiveis[1:]:
                area.union_ip(rect)
            imagem = imagem.subsurface(area).copy()

        return pygame.transform.scale(imagem, (largura, altura))

# empurra o player pra fora da plataforma no eixo x
def resolver_colisao_x(player, grupo_plataformas):
    colisoes = pygame.sprite.spritecollide(player, grupo_plataformas, False)
    for plat in colisoes:
        # se a sobreposicao vertical for menor, o contato e por cima/baixo, nao pelo lado
        sobreposicao_x = min(player.rect.right, plat.rect.right) - max(player.rect.left, plat.rect.left)
        sobreposicao_y = min(player.rect.bottom, plat.rect.bottom) - max(player.rect.top, plat.rect.top)

        if sobreposicao_y < sobreposicao_x:
            continue

        if player.velocidade_x > 0:
            player.rect.right = plat.rect.left
        elif player.velocidade_x < 0:
            player.rect.left = plat.rect.right


# empurra o player pra fora da plataforma no eixo y (pousar ou bater a cabeca)
def resolver_colisao_y(player, grupo_plataformas):
    colisoes = pygame.sprite.spritecollide(player, grupo_plataformas, False)
    player.no_chao = False
    pousou = False

    for plat in colisoes:
        if player.velocidade_y > 0:
            player.rect.bottom = plat.rect.top
            player.velocidade_y = 0
            player.no_chao = True
            player.plataforma_atual = plat
            pousou = True
        elif player.velocidade_y < 0:
            player.rect.top = plat.rect.bottom
            player.velocidade_y = 0

    if not pousou:
        # limpa a plataforma atual se o player nao esta em cima de nenhuma
        player.plataforma_atual = None

class PlataformaMovel(Plataforma):
    def __init__(self, x, y, largura, altura, destino, velocidade, eixo="x", caminho_imagem=None):
        super().__init__(x, y, largura, altura, caminho_imagem)
        self.eixo = eixo
        self.velocidade_x = velocidade if eixo == "x" else 0
        self.velocidade_y = velocidade if eixo == "y" else 0

        pos_inicial = x if eixo == "x" else y
        self.pos_min = min(pos_inicial, destino)
        self.pos_max = max(pos_inicial, destino)
        # guarda a posicao em float pra nao perder velocidades pequenas ao arredondar
        self._pos = float(pos_inicial)

    def update(self, *args):
        velocidade = self.velocidade_x if self.eixo == "x" else self.velocidade_y
        self._pos += velocidade

        # inverte a direcao quando chega no limite do trajeto
        if self._pos >= self.pos_max:
            self._pos = self.pos_max
            velocidade = -abs(velocidade)
        elif self._pos <= self.pos_min:
            self._pos = self.pos_min
            velocidade = abs(velocidade)

        if self.eixo == "x":
            self.velocidade_x = velocidade
            self.rect.x = round(self._pos)
        else:
            self.velocidade_y = velocidade
            self.rect.y = round(self._pos)