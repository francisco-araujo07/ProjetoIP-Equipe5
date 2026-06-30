import pygame

import settings


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        x,
        y,
        largura,
        altura,
        vida,
        dano,
        velocidade,
        limite_esquerdo,
        limite_direito,
        cor,
        spritesheet=None,
        altura_sprite=None,
    ):
        super().__init__()

        self.vida = vida
        self.dano = dano
        self.velocidade = velocidade
        self.limite_esquerdo = limite_esquerdo
        self.limite_direito = limite_direito
        self.direcao = 1
        self.frame_index = 0
        self.animation_speed = settings.INIMIGO_ANIMATION_SPEED
        altura_sprite = altura_sprite or altura

        if spritesheet:
            self.anim_walk_right = self.recortar_frames(spritesheet, settings.SPRITESHEET_FRAMES, altura_sprite)
            self.anim_walk_left = [pygame.transform.flip(frame, True, False) for frame in self.anim_walk_right]
            self.image = self.anim_walk_right[0]
        else:
            self.anim_walk_right = []
            self.anim_walk_left = []
            self.image = pygame.Surface((largura, altura))
            self.image.fill(cor)

        base_rect = pygame.Rect(x, y, largura, altura)
        self.rect = self.image.get_rect()
        self.rect.midbottom = base_rect.midbottom

    def recortar_frames(self, caminho, quantidade_frames, altura_desejada):
        sheet = pygame.image.load(caminho).convert_alpha()
        frame_width = sheet.get_width() // quantidade_frames
        frame_height = sheet.get_height()
        frames = []

        for i in range(quantidade_frames):
            corte = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = sheet.subsurface(corte).copy()
            areas_visiveis = pygame.mask.from_surface(frame).get_bounding_rects()

            if areas_visiveis:
                frame = frame.subsurface(areas_visiveis[0]).copy()

            escala = altura_desejada / frame.get_height()
            tamanho = (int(frame.get_width() * escala), int(frame.get_height() * escala))
            frame = pygame.transform.smoothscale(frame, tamanho)
            frames.append(frame)

        return frames

    def update(self):
        self.rect.x += self.velocidade * self.direcao
        self._aplicar_limites()
        self.atualizar_animacao()
        self._aplicar_limites()

    def _aplicar_limites(self):
        if self.rect.left <= self.limite_esquerdo:
            self.rect.left = self.limite_esquerdo
            self.direcao = 1
        elif self.rect.right >= self.limite_direito:
            self.rect.right = self.limite_direito
            self.direcao = -1

    def atualizar_animacao(self):
        frames = self.anim_walk_left if self.direcao > 0 else self.anim_walk_right
        if not frames:
            return

        self.frame_index += self.animation_speed
        if self.frame_index >= len(frames):
            self.frame_index = 0

        bottom = self.rect.bottom
        centerx = self.rect.centerx
        self.image = frames[int(self.frame_index)]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.centerx = centerx

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
            settings.SPRITESHEET_INIMIGO_ANDANDO,
            settings.PLAYER_ALTURA_SPRITE,
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
            settings.SPRITESHEET_BOSS_ANDANDO,
            settings.PLAYER_ALTURA_SPRITE,
        )
