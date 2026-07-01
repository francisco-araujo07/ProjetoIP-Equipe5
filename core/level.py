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
        TAM_ICONE = 26
        self.icone_espada = pygame.transform.scale(
            pygame.image.load(settings.SPRITE_ESPADA_COLETAVEL).convert_alpha(),
            (TAM_ICONE, TAM_ICONE),
        )
        self.icone_chave = pygame.transform.scale(
            pygame.image.load(settings.IMAGEM_FRAGMENTO).convert_alpha(),
            (TAM_ICONE, TAM_ICONE),
        )
        self.fonte_slot = pygame.font.Font(None, 18)

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

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                self.player.atacar()

        if evento.type != pygame.KEYDOWN:
            return

        tecla_ataque = pygame.key.key_code(settings.TECLA_ATAQUE_PLAYER)
        tecla_pulo = pygame.key.key_code(settings.TECLA_PULAR_PLAYER)

        if evento.key == tecla_ataque:
            self.player.atacar()
        elif evento.key in (tecla_pulo, pygame.K_UP, pygame.K_w):
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

        self.player.desenhar_efeito_gema(tela)

        if not self.player.invencivel or (pygame.time.get_ticks() // 120) % 2 == 0:
            tela.blit(self.player.image, self.player.rect)

        self.desenhar_hud(tela)

        if self.dialogo_ativo:
            self.desenhar_dialogo(tela)

     
    def desenhar_hud(self, tela):
        self._desenhar_coracoes(tela)
        self._desenhar_slots(tela)
 
    # -----------------------------------------------------------------------
 
    def _desenhar_coracoes(self, tela):
        """Linha de corações pixel-art no canto superior esquerdo."""
        TOTAL_CORACOES  = 10
        TAMANHO         = 18          # px de cada coração
        ESPACO          = 2           # px entre corações
        X_INICIO        = 20
        Y_INICIO        = 20
 
        vida_ratio      = max(0, self.player.vida) / self.player.vida_max
        cheios          = round(vida_ratio * TOTAL_CORACOES)
 
        for i in range(TOTAL_CORACOES):
            x = X_INICIO + i * (TAMANHO + ESPACO)
            preenchido = i < cheios
            self._desenhar_coracao(tela, x, Y_INICIO, TAMANHO, preenchido)
 
        # Número de vida ao lado
        texto = self.fonte_hud.render(
            f"{self.player.vida}/{self.player.vida_max}", True, settings.WHITE
        )
        tela.blit(texto, (X_INICIO + TOTAL_CORACOES * (TAMANHO + ESPACO) + 6, Y_INICIO + 2))
 
    def _desenhar_coracao(self, tela, x, y, tamanho, preenchido):
        """Desenha um coração pixel-art num retângulo de 'tamanho x tamanho'."""
        cor_cheia   = (232, 54,  54)
        cor_brilho  = (255, 107, 107)
        cor_sombra  = (192, 32,  32)
        cor_vazia   = (80,  80,  80)
        cor_contorno = (0,   0,   0)
 
        # Grade 9×8 (colunas × linhas) mapeada para o tamanho real
        grade = [
            "0110 1100",   # linha 0
            "1111 1111",   # linha 1  (brilho nas cols 1-2 e 5-6)
            "1111 1111",   # linha 2
            "1111 1111",   # linha 3
            "0111 1110",   # linha 4
            "0011 1100",   # linha 5
            "0001 1000",   # linha 6
            "0000 0000",   # linha 7  (ponta — 1 pixel)
        ]
        # Mapa pixel correto (sem espaço, usando string contínua)
        pixels = [
            "011011000",
            "111111110",
            "111111110",
            "111111110",
            "011111100",
            "001111000",
            "000110000",
            "000010000",
        ]
 
        linhas = len(pixels)
        colunas = len(pixels[0])
        pw = tamanho / colunas   # largura de 1 pixel lógico
        ph = tamanho / linhas
 
        for row, linha in enumerate(pixels):
            for col, bit in enumerate(linha):
                if bit == "0":
                    continue
                rx = int(x + col * pw)
                ry = int(y + row * ph)
                rw = max(1, int(pw))
                rh = max(1, int(ph))
 
                if preenchido:
                    if row == 1 and col in (1, 2, 5, 6):
                        cor = cor_brilho
                    elif row >= 5:
                        cor = cor_sombra
                    else:
                        cor = cor_cheia
                else:
                    cor = cor_vazia
 
                pygame.draw.rect(tela, cor, (rx, ry, rw, rh))
 
    def _desenhar_slots(self, tela):
        """4 slots de inventário: espada, poção, gema, chave (sem rótulo)."""
        SLOT_TAM = 36
        SLOT_GAP = 4
        X_INICIO = 20
        Y_INICIO = 46
 
        slots = [
            ("espada", self.player.tem_espada),
            ("pocao",  False),   # sem asset ainda — fica sempre vazio
            ("gema",   self.player.tem_gema),
            ("chave",  self.player.fragmentos_chave > 0),
        ]
 
        for i, (tipo, ativo) in enumerate(slots):
            x = X_INICIO + i * (SLOT_TAM + SLOT_GAP)
            y = Y_INICIO
            self._desenhar_slot_base(tela, x, y, SLOT_TAM, ativo)
            self._desenhar_icone_slot(tela, tipo, x, y, SLOT_TAM)
 
    def _desenhar_slot_base(self, tela, x, y, tamanho, ativo):
        """Fundo + borda estilo Minecraft de um slot."""
        cor_fundo = (70, 70, 70) if ativo else (40, 40, 40)
        cor_clara = (140, 140, 140) if ativo else (90, 90, 90)
        cor_escura = (20, 20, 20)
 
        pygame.draw.rect(tela, cor_fundo, (x, y, tamanho, tamanho))
        pygame.draw.line(tela, cor_clara,  (x, y), (x + tamanho - 1, y), 2)
        pygame.draw.line(tela, cor_clara,  (x, y), (x, y + tamanho - 1), 2)
        pygame.draw.line(tela, cor_escura, (x, y + tamanho - 1), (x + tamanho, y + tamanho - 1), 2)
        pygame.draw.line(tela, cor_escura, (x + tamanho - 1, y), (x + tamanho - 1, y + tamanho), 2)
 
    def _desenhar_icone_slot(self, tela, tipo, x, y, tamanho):
        """Desenha o conteúdo do slot: PNG (espada/chave) ou nada (poção/gema)."""
 
        if tipo == "espada" and self.player.tem_espada:
            icone_rect = self.icone_espada.get_rect(
                center=(x + tamanho // 2, y + tamanho // 2)
            )
            tela.blit(self.icone_espada, icone_rect)
 
        elif tipo == "chave" and self.player.fragmentos_chave > 0:
            icone_rect = self.icone_chave.get_rect(
                center=(x + tamanho // 2, y + tamanho // 2)
            )
            tela.blit(self.icone_chave, icone_rect)
 
            # Contador "x/3" no canto inferior direito do slot
            texto = f"{self.player.fragmentos_chave}/3"
            superficie = self.fonte_slot.render(texto, True, settings.WHITE)
            sombra = self.fonte_slot.render(texto, True, (0, 0, 0))
            pos_x = x + tamanho - superficie.get_width() - 2
            pos_y = y + tamanho - superficie.get_height() - 1
            tela.blit(sombra, (pos_x + 1, pos_y + 1))
            tela.blit(superficie, (pos_x, pos_y))

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
        return self.estado == GameState.PLAYING and self.player.rect.right >= settings.LARGURA_TELA
