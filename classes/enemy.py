import math

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


class Colosso(Enemy):
    """Boss final. Persegue o player e ataca em ciclo: telegrafa a marretada,
    golpeia numa hitbox propria (fora do leitura_dano/leitura_ataque genericos),
    e so fica vulneravel a dano por uma janela curta depois do golpe."""

    PERSEGUINDO = "perseguindo"
    TELEGRAFANDO = "telegrafando"
    ATACANDO = "atacando"
    VULNERAVEL = "vulneravel"

    def __init__(self, x, y, limite_esquerdo, limite_direito, player):
        super().__init__(
            x,
            y,
            90,
            140,
            settings.COLOSSO_VIDA,
            settings.COLOSSO_DANO_TOQUE,
            settings.COLOSSO_VELOCIDADE,
            limite_esquerdo,
            limite_direito,
            settings.YELLOW,
            settings.SPRITESHEET_BOSS_ANDANDO,
            settings.COLOSSO_ALTURA_SPRITE,
        )
        self._player = player

        self.sprite_ataque_right = self._carregar_sprite_estatico(
            settings.SPRITE_BOSS_ATACANDO, settings.COLOSSO_ALTURA_SPRITE
        )
        self.sprite_ataque_left = pygame.transform.flip(self.sprite_ataque_right, True, False)

        self.estado = self.PERSEGUINDO
        self.tempo_estado = pygame.time.get_ticks()
        self.vulneravel = False
        self._hitbox_marreta = None

        self.morrendo = False
        self.tempo_morte = 0

    def _carregar_sprite_estatico(self, caminho, altura_desejada):
        imagem = pygame.image.load(caminho).convert_alpha()
        areas_visiveis = pygame.mask.from_surface(imagem).get_bounding_rects()

        if areas_visiveis:
            area = areas_visiveis[0].copy()
            for rect in areas_visiveis[1:]:
                area.union_ip(rect)
            imagem = imagem.subsurface(area).copy()

        escala = altura_desejada / imagem.get_height()
        tamanho = (int(imagem.get_width() * escala), int(imagem.get_height() * escala))
        return pygame.transform.smoothscale(imagem, tamanho)

    def update(self, *args):
        if self.morrendo:
            self._atualizar_morte()
            return

        agora = pygame.time.get_ticks()
        decorrido = agora - self.tempo_estado

        if self.estado == self.PERSEGUINDO:
            self._perseguir()
            self.atualizar_animacao()
            if abs(self._player.rect.centerx - self.rect.centerx) <= settings.COLOSSO_DISTANCIA_GATILHO:
                self._mudar_estado(self.TELEGRAFANDO)
        elif self.estado == self.TELEGRAFANDO:
            if decorrido >= settings.COLOSSO_TELEGRAFANDO_MS:
                self._mudar_estado(self.ATACANDO)
        elif self.estado == self.ATACANDO:
            self._aplicar_sprite_ataque()
            if decorrido >= settings.COLOSSO_ATACANDO_MS:
                self._mudar_estado(self.VULNERAVEL)
        elif self.estado == self.VULNERAVEL:
            if decorrido >= settings.COLOSSO_VULNERAVEL_MS:
                self._mudar_estado(self.PERSEGUINDO)

    def _perseguir(self):
        if self._player.rect.centerx > self.rect.centerx:
            self.direcao = 1
        elif self._player.rect.centerx < self.rect.centerx:
            self.direcao = -1

        self.rect.x += self.velocidade * self.direcao

        if self.rect.left < self.limite_esquerdo:
            self.rect.left = self.limite_esquerdo
        elif self.rect.right > self.limite_direito:
            self.rect.right = self.limite_direito

    def _mudar_estado(self, novo_estado):
        self.estado = novo_estado
        self.tempo_estado = pygame.time.get_ticks()
        self.vulneravel = novo_estado == self.VULNERAVEL
        self._hitbox_marreta = self._criar_hitbox_marreta() if novo_estado == self.ATACANDO else None

    def _criar_hitbox_marreta(self):
        hitbox = pygame.Rect(0, 0, settings.COLOSSO_MARRETA_LARGURA, settings.COLOSSO_MARRETA_ALTURA)
        hitbox.centery = self.rect.centery

        if self.direcao > 0:
            hitbox.left = self.rect.right
        else:
            hitbox.right = self.rect.left

        return hitbox

    def hitbox_marreta(self):
        return self._hitbox_marreta

    def _aplicar_sprite_ataque(self):
        bottom = self.rect.bottom
        centerx = self.rect.centerx
        self.image = self.sprite_ataque_right if self.direcao > 0 else self.sprite_ataque_left
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.centerx = centerx

    def levar_dano(self, valor):
        if not self.vulneravel or self.morrendo:
            return

        self.vida -= valor
        if self.vida <= 0:
            self.vida = 0
            self._iniciar_morte()

    def _iniciar_morte(self):
        self.morrendo = True
        self.vulneravel = False
        self._hitbox_marreta = None
        self.tempo_morte = pygame.time.get_ticks()

    def _atualizar_morte(self):
        decorrido = pygame.time.get_ticks() - self.tempo_morte
        progresso = min(1.0, decorrido / settings.COLOSSO_MORTE_FADE_MS)
        self.image.set_alpha(int(255 * (1 - progresso)))

        if progresso >= 1.0:
            self.kill()

    def desenhar_efeito_estado(self, tela):
        if self.morrendo:
            return

        agora = pygame.time.get_ticks()
        decorrido = agora - self.tempo_estado

        if self.estado == self.TELEGRAFANDO:
            progresso = min(1.0, decorrido / settings.COLOSSO_TELEGRAFANDO_MS)
            self._desenhar_glow(tela, (255, 60, 40), int(200 * progresso))
        elif self.estado == self.VULNERAVEL:
            pulso = math.sin(agora / 150)
            self._desenhar_glow(tela, (255, 210, 70), int(140 + pulso * 80))

    def _desenhar_glow(self, tela, cor, alpha):
        margem = 20
        largura = self.rect.width + margem * 2
        altura = self.rect.height + margem * 2
        superficie = pygame.Surface((largura, altura), pygame.SRCALPHA)

        for fator_tamanho, fator_alpha in ((1.0, 0.3), (0.7, 0.5), (0.4, 0.8)):
            rect_elipse = pygame.Rect(0, 0, int(largura * fator_tamanho), int(altura * fator_tamanho))
            rect_elipse.center = (largura // 2, altura // 2)
            pygame.draw.ellipse(superficie, (*cor, max(0, int(alpha * fator_alpha))), rect_elipse)

        tela.blit(superficie, (self.rect.x - margem, self.rect.y - margem))
