import pygame

import settings


class ArmadilhaEspinhos(pygame.sprite.Sprite):
    """Armadilha de espinhos reutilizável em qualquer fase.

    Se `caminho_imagem` for informado, a própria armadilha carrega e desenha
    seu sprite (podendo ser adicionada a um pygame.sprite.Group como qualquer
    outro elemento do jogo). Sem imagem, o rect continua funcionando apenas
    como área de dano invisível — comportamento original, usado quando o
    visual da armadilha já está embutido no fundo da tela (ex.: Fase 2 Tela 1).
    """

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
        imagem = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(imagem, (self.rect.width, self.rect.height))

    def _imagem_transparente(self):
        return pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

    def desativar(self):
        self.ativa = False

        if self._imagem_desativada is not None:
            self.image = self._imagem_desativada
        elif self._imagem_ativa is not None:
            self.image = self._imagem_transparente()

    def aplicar_dano(self, player):
        if self.ativa and player.rect.colliderect(self.rect):
            player.levar_dano(self.dano)
