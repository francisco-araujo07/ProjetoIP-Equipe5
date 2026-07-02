import math

import pygame
import settings


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, estado=None):
        super().__init__()

        self.frame_index = 0
        self.animation_speed = settings.PLAYER_ANIMATION_SPEED
        self.anim_idle_right = self.recortar_frames(
            settings.SPRITESHEET_PLAYER_PARADO,
            settings.SPRITESHEET_FRAMES,
            settings.PLAYER_ALTURA_SPRITE,
        )
        self.anim_idle_left = [pygame.transform.flip(frame, True, False) for frame in self.anim_idle_right]
        self.anim_run_right = self.recortar_frames(
            settings.SPRITESHEET_PLAYER_CORRENDO,
            settings.SPRITESHEET_FRAMES,
            settings.PLAYER_ALTURA_SPRITE,
        )
        self.anim_run_left = [pygame.transform.flip(frame, True, False) for frame in self.anim_run_right]
        ataque_right = self.carregar_frame(settings.SPRITE_PLAYER_ATACANDO, settings.PLAYER_ALTURA_SPRITE)
        self.anim_attack_right = [ataque_right]
        self.anim_attack_left = [pygame.transform.flip(ataque_right, True, False)]

        self.image = self.anim_idle_right[0]
        base_rect = pygame.Rect(x, y, settings.PLAYER_LARGURA_BASE, settings.PLAYER_ALTURA_BASE)
        self.rect = self.image.get_rect()
        self.rect.midbottom = base_rect.midbottom
        self.direcao = 1
        self.movendo = False
        self.ultimo_ataque_ms = -settings.PLAYER_ATAQUE_COOLDOWN_MS
        self.inicio_ataque_ms = 0
        self._hitbox_ataque = None
        self.inimigos_acertados = set()

        self.velocidade_y = 0
        self.velocidade_x = 0
        self.no_chao = False
        self.plataforma_atual = None
        self.velocidade = settings.VELOCIDADE_PLAYER
        self.vida_max = settings.PLAYER_VIDA_MAX
        self.tem_espada = False
        self.fragmentos_chave = 0
        self.tem_gema = False
        self.vida = self.vida_max
        self.dano = settings.PLAYER_DANO
        self.pocoes = 0

        if estado is not None:
            self.carregar_estado(estado)

        self.invencivel = False
        self.tempo_dano = 0

        self.atualizar_visual()

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

    def carregar_frame(self, caminho, altura_desejada):
        frame = pygame.image.load(caminho).convert_alpha()
        areas_visiveis = pygame.mask.from_surface(frame).get_bounding_rects()

        if areas_visiveis:
            area = areas_visiveis[0].copy()
            for rect in areas_visiveis[1:]:
                area.union_ip(rect)
            frame = frame.subsurface(area).copy()

        escala = altura_desejada / frame.get_height()
        tamanho = (int(frame.get_width() * escala), int(frame.get_height() * escala))
        return pygame.transform.smoothscale(frame, tamanho)

    def aplicar_gravidade(self):
        self.velocidade_y += settings.GRAVIDADE
        if self.velocidade_y > settings.VELOCIDADE_MAX_QUEDA:
            self.velocidade_y = settings.VELOCIDADE_MAX_QUEDA

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
        self.frame_index = 0
        self.atualizar_visual()
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
            self.atualizar_visual()

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

    def update(self, grupo_plataformas):
        from classes.plataforma import resolver_colisao_x, resolver_colisao_y, PlataformaMovel
        teclas = pygame.key.get_pressed()
        movendo = False
        self.velocidade_x = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.velocidade_x = -self.velocidade
            self.direcao = -1
            movendo = True
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.velocidade_x = self.velocidade
            self.direcao = 1
            movendo = True

        self.movendo = movendo
        self.atualizar_animacao()

        self.rect.x += self.velocidade_x
        resolver_colisao_x(self, grupo_plataformas)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.LARGURA_TELA:
            self.rect.right = settings.LARGURA_TELA

        self.aplicar_gravidade()
        self.rect.y += self.velocidade_y
        resolver_colisao_y(self, grupo_plataformas)

        if isinstance(self.plataforma_atual, PlataformaMovel): 
            self.rect.x += self.plataforma_atual.velocidade_x
            self.rect.y += self.plataforma_atual.velocidade_y
        
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

    def atualizar_animacao(self):
        self.frame_index += self.animation_speed
        frames = self._frames_atuais()

        if self.frame_index >= len(frames):
            self.frame_index = 0

        self._aplicar_frame(frames[int(self.frame_index)])

    def _frames_atuais(self):
        if self._hitbox_ataque is not None:
            return self.anim_attack_right if self.direcao > 0 else self.anim_attack_left
        if self.movendo:
            return self.anim_run_right if self.direcao > 0 else self.anim_run_left
        return self.anim_idle_right if self.direcao > 0 else self.anim_idle_left

    def _aplicar_frame(self, frame):
        bottom = self.rect.bottom
        centerx = self.rect.centerx
        self.image = frame
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.centerx = centerx

    def atualizar_visual(self):
        frames = self._frames_atuais()
        self.frame_index %= len(frames)
        self._aplicar_frame(frames[int(self.frame_index)])

    def usar_pocao(self):
        if self.pocoes > 0 and self.vida < self.vida_max:
            self.pocoes -= 1
            self.vida = min(self.vida + settings.POCAO_CURA, self.vida_max)

    def carregar_estado(self, estado):
        self.tem_espada = estado.tem_espada
        self.fragmentos_chave = estado.fragmentos_chave
        self.tem_gema = estado.tem_gema
        self.vida = min(estado.vida_atual, self.vida_max)
        self.dano = estado.dano_atual
        self.pocoes = estado.pocoes
        self.atualizar_visual()

    def salvar_estado(self, estado):
        estado.tem_espada = self.tem_espada
        estado.fragmentos_chave = self.fragmentos_chave
        estado.tem_gema = self.tem_gema
        estado.vida_atual = self.vida
        estado.dano_atual = self.dano
        estado.pocoes = self.pocoes

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
