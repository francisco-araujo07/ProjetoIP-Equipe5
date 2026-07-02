import pygame

import settings


class ArmadilhaEspinhos(pygame.sprite.Sprite):
    """Armadilha de espinhos que causa dano no player."""

    def __init__(self, rect, dano=settings.ESPINHOS_DANO, caminho_imagem=None, caminho_imagem_desativada=None):
        super().__init__()
        self.rect = pygame.Rect(rect)
        self.dano = dano
        self.ativa = True

        self._imagem_ativa = self._carregar_imagem(caminho_imagem) if caminho_imagem else None
        self._imagem_desativada = (
            self._carregar_imagem(caminho_imagem_desativada) if caminho_imagem_desativada else None
        )

        self.image = self._imagem_ativa if self._imagem_ativa is not None else self._imagem_transparente()

    def _carregar_imagem(self, caminho):
        # corta as bordas vazias da imagem antes de redimensionar
        imagem = pygame.image.load(caminho).convert_alpha()
        areas_visiveis = pygame.mask.from_surface(imagem).get_bounding_rects()

        if areas_visiveis:
            area = areas_visiveis[0].copy()
            for rect in areas_visiveis[1:]:
                area.union_ip(rect)
            imagem = imagem.subsurface(area).copy()

        return pygame.transform.scale(imagem, (self.rect.width, self.rect.height))

    def _imagem_transparente(self):
        return pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

    def desativar(self):
        # desliga a armadilha, ela para de causar dano
        self.ativa = False

        if self._imagem_desativada is not None:
            self.image = self._imagem_desativada
        elif self._imagem_ativa is not None:
            self.image = self._imagem_transparente()

    def aplicar_dano(self, player):
        # causa dano se a armadilha esta ativa e encostou no player
        if self.ativa and player.rect.colliderect(self.rect):
            player.levar_dano(self.dano)
