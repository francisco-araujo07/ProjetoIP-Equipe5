import pygame

import settings


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura, vida, dano, velocidade, limite_esquerdo, limite_direito, cor):
        super().__init__()

        self.image = pygame.Surface((largura, altura))
        self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.vida = vida
        self.dano = dano
        self.velocidade = velocidade
        self.limite_esquerdo = limite_esquerdo
        self.limite_direito = limite_direito
        self.direcao = 1

    def update(self):
        self.rect.x += self.velocidade * self.direcao

        if self.rect.left <= self.limite_esquerdo:
            self.rect.left = self.limite_esquerdo
            self.direcao = 1
        elif self.rect.right >= self.limite_direito:
            self.rect.right = self.limite_direito
            self.direcao = -1

    def levar_dano(self, valor):
        self.vida -= valor
        if self.vida <= 0:
            self.kill()


class Saqueador(Enemy):
    def __init__(self, x, y, limite_esquerdo, limite_direito):
        super().__init__(
            x,
            y,
            44,
            56,
            settings.SAQUEADOR_VIDA,
            settings.SAQUEADOR_DANO,
            settings.SAQUEADOR_VELOCIDADE,
            limite_esquerdo,
            limite_direito,
            settings.RED,
        )


class Automato(Enemy):
    def __init__(self, x, y, limite_esquerdo, limite_direito):
        super().__init__(
            x,
            y,
            52,
            64,
            settings.AUTOMATO_VIDA,
            settings.AUTOMATO_DANO,
            settings.AUTOMATO_VELOCIDADE,
            limite_esquerdo,
            limite_direito,
            settings.GRAY,
        )
