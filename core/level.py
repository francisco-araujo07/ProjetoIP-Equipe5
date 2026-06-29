import pygame

import settings
from classes.player import Player
from classes.plataforma import Plataforma, resolver_colisao_chao
from classes.coletavel import Pocao, FragmentoChave, Gema 
from core.game_state import GameState


class Level:
    FUNDO = None
    LAYOUT_PLATAFORMAS = []
    DIALOGOS = []

    def __init__(self, player_state=None):
        self.estado = GameState.PLAYING
        self.player_state = player_state
        self.player = Player(100, settings.ALTURA_TELA - 210, self.player_state)
        self.plataformas = pygame.sprite.Group()
        self.coletaveis = pygame.sprite.Group()
        self.grupo_inimigos = pygame.sprite.Group()

        self.layout_plataformas = self.LAYOUT_PLATAFORMAS
        self.dialogo_indice = 0
        self.dialogo_caracteres = 0
        self.ultimo_typewriter_ms = pygame.time.get_ticks()
        self.dialogo_ativo = len(self.DIALOGOS) > 0
        self.fonte_dialogo = pygame.font.Font(None, 32)
        self.fonte_hud = pygame.font.Font(None, 28)

        self.criar_plataformas()

        fundo = pygame.image.load(self.FUNDO).convert()
        self.fundo = pygame.transform.scale(fundo, (settings.LARGURA_TELA, settings.ALTURA_TELA))

    def criar_plataformas(self):
        for entrada in self.layout_plataformas:
            x, y, largura, altura = entrada[:4]
            caminho_imagem = entrada[4] if len(entrada) > 4 else None
            plataforma = Plataforma(x, y, largura, altura, caminho_imagem)
            self.plataformas.add(plataforma)

    def processar_evento(self, evento):
        if self.dialogo_ativo:
            self.processar_evento_dialogo(evento)
            return

        if evento.type != pygame.KEYDOWN:
            return

        tecla_ataque = pygame.key.key_code(settings.TECLA_ATAQUE_PLAYER)
        tecla_pulo = pygame.key.key_code(settings.TECLA_PULAR_PLAYER)

        if evento.key == tecla_ataque:
            self.player.atacar()
        elif evento.key in (tecla_pulo, pygame.K_UP):
            self.player.pular()

    def processar_evento_dialogo(self, evento):
        if evento.type != pygame.KEYDOWN:
            return

        texto_atual = self.DIALOGOS[self.dialogo_indice]
        if self.dialogo_caracteres < len(texto_atual):
            self.dialogo_caracteres = len(texto_atual)
            return

        self.dialogo_indice += 1
        self.dialogo_caracteres = 0
        self.ultimo_typewriter_ms = pygame.time.get_ticks()

        if self.dialogo_indice >= len(self.DIALOGOS):
            self.dialogo_ativo = False

    def atualizar(self):
        if self.dialogo_ativo:
            self.atualizar_dialogo()
            return

        self.player.update()
        self.grupo_inimigos.update()
        resolver_colisao_chao(self.player, self.plataformas)
        self.checar_colisao_coletaveis()
        self.leitura_ataque()
        self.leitura_dano()
        self.salvar_estado_jogador()

    def atualizar_dialogo(self):
        agora = pygame.time.get_ticks()
        intervalo = 1000 / settings.TYPEWRITER_LETRAS_POR_SEGUNDO

        while agora - self.ultimo_typewriter_ms >= intervalo:
            texto_atual = self.DIALOGOS[self.dialogo_indice]
            if self.dialogo_caracteres >= len(texto_atual):
                break

            self.dialogo_caracteres += 1
            self.ultimo_typewriter_ms += intervalo

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

        self.plataformas.draw(tela)
        self.grupo_inimigos.draw(tela)
        self.coletaveis.draw(tela)

        if not self.player.invencivel or (pygame.time.get_ticks() // 120) % 2 == 0:
            tela.blit(self.player.image, self.player.rect)

        hitbox = self.player.hitbox_ataque()
        if hitbox is not None:
            pygame.draw.rect(tela, settings.ORANGE, hitbox, 2)

        self.desenhar_hud(tela)

        if self.dialogo_ativo:
            self.desenhar_dialogo(tela)

    def desenhar_hud(self, tela):
        largura_barra = 180
        altura_barra = 18
        vida_ratio = max(0, self.player.vida) / self.player.vida_max

        pygame.draw.rect(tela, settings.GRAY, (20, 20, largura_barra, altura_barra))
        pygame.draw.rect(tela, settings.RED, (20, 20, int(largura_barra * vida_ratio), altura_barra))

        textos = [
            f"Vida: {self.player.vida}/{self.player.vida_max}",
            f"Fragmentos: {self.player.fragmentos_chave}/3",
            f"Espada: {'sim' if self.player.tem_espada else 'nao'}",
            f"Gema: {'sim' if self.player.tem_gema else 'nao'}",
        ]

        y = 44
        for texto in textos:
            superficie = self.fonte_hud.render(texto, True, settings.WHITE)
            tela.blit(superficie, (20, y))
            y += 24

    def desenhar_dialogo(self, tela):
        caixa = pygame.Rect(80, settings.ALTURA_TELA - 170, settings.LARGURA_TELA - 160, 110)
        pygame.draw.rect(tela, settings.BLACK, caixa)
        pygame.draw.rect(tela, settings.WHITE, caixa, 2)

        texto_atual = self.DIALOGOS[self.dialogo_indice]
        texto_visivel = texto_atual[:self.dialogo_caracteres]
        superficie = self.fonte_dialogo.render(texto_visivel, True, settings.WHITE)
        tela.blit(superficie, (caixa.x + 24, caixa.y + 28))
    def checar_colisao_coletaveis(self):                     # ← ADICIONADO
        """Detecta colisão entre o player e coletáveis"""
        coletados = pygame.sprite.spritecollide(
            self.player,
            self.coletaveis,
            False,
            pygame.sprite.collide_rect,
        )
        for item in coletados:
            item.coletar(self.player)

    def leitura_ataque(self):
        hitbox = self.player.hitbox_ataque()
        if hitbox is None:
            return

        for inimigo in self.grupo_inimigos:
            if id(inimigo) in self.player.inimigos_acertados:
                continue

            if hitbox.colliderect(inimigo.rect):
                inimigo.levar_dano(self.player.dano)
                self.player.inimigos_acertados.add(id(inimigo))

    def leitura_dano(self):
        tocados = pygame.sprite.spritecollide(self.player, self.grupo_inimigos, False)

        for inimigo in tocados:
            self.player.levar_dano(inimigo.dano)

        if not self.player.esta_vivo():
            self.estado = GameState.GAME_OVER

    def salvar_estado_jogador(self):
        if self.player_state is not None:
            self.player.salvar_estado(self.player_state)

    def terminou(self):
        return self.player.rect.right >= settings.LARGURA_TELA
