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
        # Recorta a margem transparente ao redor do desenho antes de redimensionar,
        # senao a arte fica encolhida num canto do rect (mesmo padrao usado em Player/ArmadilhaEspinhos).
        imagem = pygame.image.load(caminho_imagem).convert_alpha()
        areas_visiveis = pygame.mask.from_surface(imagem).get_bounding_rects()

        if areas_visiveis:
            area = areas_visiveis[0].copy()
            for rect in areas_visiveis[1:]:
                area.union_ip(rect)
            imagem = imagem.subsurface(area).copy()

        return pygame.transform.scale(imagem, (largura, altura))

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

        pos_inicial = x if eixo == "x" else y
        self.pos_min = min(pos_inicial, destino)
        self.pos_max = max(pos_inicial, destino)

    def update(self, *args):
        if self.eixo == "x":
            self.rect.x += self.velocidade_x
            pos_atual = self.rect.x
        else:
            self.rect.y += self.velocidade_y
            pos_atual = self.rect.y

        if pos_atual >= self.pos_max:
            if self.eixo == "x":
                self.rect.x = self.pos_max
                self.velocidade_x = -abs(self.velocidade_x)
            else:
                self.rect.y = self.pos_max
                self.velocidade_y = -abs(self.velocidade_y)
        elif pos_atual <= self.pos_min:
            if self.eixo == "x":
                self.rect.x = self.pos_min
                self.velocidade_x = abs(self.velocidade_x)
            else:
                self.rect.y = self.pos_min
                self.velocidade_y = abs(self.velocidade_y)