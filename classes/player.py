import pygame
import settings


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((40, 56))
        self.image.fill(settings.BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.velocidade_y = 0
        self.no_chao = False
        self.velocidade = settings.VELOCIDADE_PLAYER
        self.vida_max = settings.PLAYER_VIDA_MAX
        self.vida = self.vida_max
        self.dano = settings.PLAYER_DANO

        self.direcao = 1
        self.ultimo_ataque_ms = -settings.PLAYER_ATAQUE_COOLDOWN_MS
        self.inicio_ataque_ms = 0
        self._hitbox_ataque = None

        self.invencivel = False
        self.tempo_dano = 0

    def aplicar_gravidade(self):
        self.velocidade_y += settings.GRAVIDADE
        if self.velocidade_y > settings.VELOCIDADE_MAX_QUEDA:
            self.velocidade_y = settings.VELOCIDADE_MAX_QUEDA
        self.rect.y += self.velocidade_y

    def pular(self):
        if self.no_chao:
            self.velocidade_y = -settings.FORCA_PULO
            self.no_chao = False

    def atacar(self):
        agora = pygame.time.get_ticks()
        tempo_desde_ultimo_ataque = agora - self.ultimo_ataque_ms

        if tempo_desde_ultimo_ataque < settings.PLAYER_ATAQUE_COOLDOWN_MS:
            return False

        self.ultimo_ataque_ms = agora
        self.inicio_ataque_ms = agora
        self._hitbox_ataque = self._criar_hitbox_ataque()
        return True

    def hitbox_ataque(self):
        self.atualizar_ataque()
        return self._hitbox_ataque

    def atualizar_ataque(self):
        if self._hitbox_ataque is None:
            return

        agora = pygame.time.get_ticks()
        if agora - self.inicio_ataque_ms >= settings.PLAYER_ATAQUE_DURACAO_MS:
            self._hitbox_ataque = None

    def atualizar_invencibilidade(self):
        if not self.invencivel:
            return

        agora = pygame.time.get_ticks()
        if agora - self.tempo_dano >= settings.DURACAO_INVENCIBILIDADE:
            self.invencivel = False

    def _criar_hitbox_ataque(self):
        hitbox = pygame.Rect(
            0,
            0,
            settings.PLAYER_ATAQUE_ALCANCE,
            settings.PLAYER_ATAQUE_ALTURA,
        )
        hitbox.centery = self.rect.centery

        if self.direcao > 0:
            hitbox.left = self.rect.right
        else:
            hitbox.right = self.rect.left

        return hitbox

    def update(self):
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
            self.direcao = -1
        if teclas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
            self.direcao = 1

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.LARGURA_TELA:
            self.rect.right = settings.LARGURA_TELA

        self.aplicar_gravidade()
        self.atualizar_ataque()
        self.atualizar_invencibilidade()

    def levar_dano(self, valor):
        if not self.invencivel:
            self.vida -= valor

            if self.vida < 0:
                self.vida = 0

            self.invencivel = True
            self.tempo_dano = pygame.time.get_ticks()

    def esta_vivo(self):
        return self.vida > 0
