import math

import pygame
import settings


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, estado=None):
        super().__init__()

        self.image = pygame.Surface((40, 56))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.velocidade_y = 0
        self.no_chao = False
        self.velocidade = settings.VELOCIDADE_PLAYER
        self.vida_max = settings.PLAYER_VIDA_MAX
        self.tem_espada = False
        self.fragmentos_chave = 0
        self.tem_gema = False
        self.vida = self.vida_max
        self.dano = settings.PLAYER_DANO

        if estado is not None:
            self.carregar_estado(estado)

        self.atualizar_visual()

        self.direcao = 1
        self.ultimo_ataque_ms = -settings.PLAYER_ATAQUE_COOLDOWN_MS
        self.inicio_ataque_ms = 0
        self._hitbox_ataque = None
        self.inimigos_acertados = set()

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
        if not self.tem_espada:
            return False

        agora = pygame.time.get_ticks()
        tempo_desde_ultimo_ataque = agora - self.ultimo_ataque_ms

        if tempo_desde_ultimo_ataque < settings.PLAYER_ATAQUE_COOLDOWN_MS:
            return False

        self.ultimo_ataque_ms = agora
        self.inicio_ataque_ms = agora
        self._hitbox_ataque = self._criar_hitbox_ataque()
        self.inimigos_acertados = set()
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

    def atualizar_visual(self):
        caminho = (
            settings.SPRITE_PLAYER_COM_ESPADA
            if self.tem_espada
            else settings.SPRITE_PLAYER_SEM_ESPADA
        )
        self.image = pygame.image.load(caminho).convert_alpha()

    def carregar_estado(self, estado):
        self.tem_espada = estado.tem_espada
        self.fragmentos_chave = estado.fragmentos_chave
        self.tem_gema = estado.tem_gema
        self.vida = min(estado.vida_atual, self.vida_max)
        self.dano = estado.dano_atual
        self.atualizar_visual()

    def salvar_estado(self, estado):
        estado.tem_espada = self.tem_espada
        estado.fragmentos_chave = self.fragmentos_chave
        estado.tem_gema = self.tem_gema
        estado.vida_atual = self.vida
        estado.dano_atual = self.dano

    def desenhar_efeito_gema(self, tela):
        """Desenha brilho dourado pulsante ao redor do player quando tem_gema=True."""
        if not self.tem_gema:
            return

        agora = pygame.time.get_ticks()
        # sin oscila entre -1 e 1 → alpha entre 60 e 140
        pulso = math.sin(agora / 300)
        alpha = int(100 + pulso * 40)

        margem = 8
        largura_brilho = self.rect.width + margem * 2
        altura_brilho = self.rect.height + margem * 2

        superficie_brilho = pygame.Surface((largura_brilho, altura_brilho), pygame.SRCALPHA)

        # Três elipses concêntricas com alpha decrescente para suavizar as bordas
        for camada, fator_alpha in enumerate([alpha, alpha // 2, alpha // 4]):
            recuo = camada * 3
            rect_elipse = pygame.Rect(recuo, recuo, largura_brilho - recuo * 2, altura_brilho - recuo * 2)
            cor_brilho = (255, 210, 50, fator_alpha)  # dourado semi-transparente
            pygame.draw.ellipse(superficie_brilho, cor_brilho, rect_elipse)

        pos_brilho = (self.rect.x - margem, self.rect.y - margem)
        tela.blit(superficie_brilho, pos_brilho)