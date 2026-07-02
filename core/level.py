import pygame

import settings
from classes.player import Player
from classes.plataforma import Plataforma, PlataformaMovel
from classes.coletavel import Pocao, FragmentoChave, Gema 
from core.game_state import GameState


class Level:
    FUNDO = None
    LAYOUT_PLATAFORMAS = []
    LAYOUT_PLATAFORMAS_MOVEIS = []
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
        
        self.icone_coracao_cheio = pygame.transform.scale(
        pygame.image.load(settings.ICONE_HUD_CORACAO_CHEIO).convert_alpha(),
       (settings.TAM_ICONE_CORACAO, settings.TAM_ICONE_CORACAO),
       )
        self.icone_coracao_vazio = pygame.transform.scale(
       pygame.image.load(settings.ICONE_HUD_CORACAO_VAZIO).convert_alpha(),
       (settings.TAM_ICONE_CORACAO, settings.TAM_ICONE_CORACAO),
        )
        self.icone_espada = pygame.transform.rotate(
       pygame.transform.scale(
               pygame.image.load(settings.SPRITE_ESPADA_COLETAVEL).convert_alpha(),
               (settings.TAM_ICONE_SLOT, settings.TAM_ICONE_SLOT),
           ),
           settings.ROTACAO_ICONE_SLOT,
        )
        self.icone_chave = pygame.transform.rotate(
           pygame.transform.scale(
               pygame.image.load(settings.IMAGEM_FRAGMENTO).convert_alpha(),
               (settings.TAM_ICONE_SLOT, settings.TAM_ICONE_SLOT),
           ),
           settings.ROTACAO_ICONE_SLOT,
        )
        self.fonte_slot = pygame.font.Font(None, 18)

        self.icone_pocao = pygame.transform.scale(
            pygame.image.load(settings.ICONE_HUD_POCAO).convert_alpha(),
            (settings.TAM_ICONE_SLOT, settings.TAM_ICONE_SLOT),
        )
        self.icone_gema = pygame.transform.scale(
        pygame.image.load(settings.ICONE_HUD_GEMA).convert_alpha(),
        (settings.TAM_ICONE_SLOT, settings.TAM_ICONE_SLOT),
        )

        self.criar_plataformas()

        fundo = pygame.image.load(self.FUNDO).convert()
        self.fundo = pygame.transform.scale(fundo, (settings.LARGURA_TELA, settings.ALTURA_TELA))

    def criar_plataformas(self):
        for entrada in self.layout_plataformas:
            x, y, largura, altura = entrada[:4]
            caminho_imagem = entrada[4] if len(entrada) > 4 else None
            plataforma = Plataforma(x, y, largura, altura, caminho_imagem)
            self.plataformas.add(plataforma)

        for entrada in self.LAYOUT_PLATAFORMAS_MOVEIS:  
            x, y, largura, altura, destino, velocidade = entrada[:6]
            eixo = entrada[6] if len(entrada) > 6 else "x"
            caminho_imagem = entrada[7] if len(entrada) > 7 else None
            self.plataformas.add(PlataformaMovel(x, y, largura, altura, destino, velocidade, eixo, caminho_imagem))

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
        elif evento.key == pygame.key.key_code(settings.TECLA_USAR_POCAO):
            self.player.usar_pocao()

    def processar_evento_dialogo(self, evento):
        if evento.type != pygame.KEYDOWN:
            return

        texto_atual = self.DIALOGOS[self.dialogo_indice]
        # se o texto ainda ta aparecendo, o primeiro toque so completa ele
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

        self.plataformas.update()
        self.player.update(self.plataformas)
        self.grupo_inimigos.update()
        self.checar_colisao_coletaveis()
        self.leitura_ataque()
        self.leitura_dano()
        self.checar_queda()
        self.salvar_estado_jogador()

    def atualizar_dialogo(self):
        # efeito de maquina de escrever: vai revelando uma letra por vez
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

 
    def _desenhar_coracoes(self, tela):
        # desenha os coracoes de vida (cada coracao = 10 de vida)
        TAMANHO   = settings.TAM_ICONE_CORACAO
        ESPACO    = settings.ESPACO_CORACAO_HUD
        X_INICIO  = settings.X_INICIO_HUD
        Y_INICIO  = settings.Y_INICIO_CORACOES_HUD
 
        total_coracoes = max(1, round(self.player.vida_max / 10))
        cheios = round((max(0, self.player.vida) / self.player.vida_max) * total_coracoes)
 
        for i in range(total_coracoes):
            x = X_INICIO + i * (TAMANHO + ESPACO)
            icone = self.icone_coracao_cheio if i < cheios else self.icone_coracao_vazio
            tela.blit(icone, (x, Y_INICIO))
 
        # Número de vida ao lado
        texto = self.fonte_hud.render(
            f"{self.player.vida}/{self.player.vida_max}", True, settings.WHITE
        )
        tela.blit(texto, (X_INICIO + total_coracoes * (TAMANHO + ESPACO) + 6, Y_INICIO + 2))
 
    def _desenhar_slots(self, tela):
        #slots do inventário: espada, poção, gema, chave.
        SLOT_TAM = settings.TAM_SLOT_HUD
        SLOT_GAP = settings.ESPACO_SLOT_HUD
        X_INICIO = settings.X_INICIO_HUD
        Y_INICIO = settings.Y_INICIO_SLOTS_HUD
 
        slots = [
            ("espada", self.player.tem_espada),
            ("pocao",  self.player.pocoes > 0),
            ("gema",   self.player.tem_gema),
            ("chave",  self.player.fragmentos_chave > 0),
        ]
 
        for i, (tipo, ativo) in enumerate(slots):
            x = X_INICIO + i * (SLOT_TAM + SLOT_GAP)
            y = Y_INICIO
            self._desenhar_slot_base(tela, x, y, SLOT_TAM, ativo)
            self._desenhar_icone_slot(tela, tipo, x, y, SLOT_TAM)
 
    def _desenhar_slot_base(self, tela, x, y, tamanho, ativo):
        # Fundo + borda de um slot.
        cor_fundo = (70, 70, 70) if ativo else (40, 40, 40)
        cor_clara = (140, 140, 140) if ativo else (90, 90, 90)
        cor_escura = (20, 20, 20)
 
        pygame.draw.rect(tela, cor_fundo, (x, y, tamanho, tamanho))
        pygame.draw.line(tela, cor_clara,  (x, y), (x + tamanho - 1, y), 2)
        pygame.draw.line(tela, cor_clara,  (x, y), (x, y + tamanho - 1), 2)
        pygame.draw.line(tela, cor_escura, (x, y + tamanho - 1), (x + tamanho, y + tamanho - 1), 2)
        pygame.draw.line(tela, cor_escura, (x + tamanho - 1, y), (x + tamanho - 1, y + tamanho), 2)
 
    def _desenhar_icone_slot(self, tela, tipo, x, y, tamanho):
        # Desenha o conteúdo do slot.
 
        if tipo == "espada" and self.player.tem_espada:
            icone_rect = self.icone_espada.get_rect(
                center=(x + tamanho // 2, y + tamanho // 2)
            )
            tela.blit(self.icone_espada, icone_rect)
        
        elif tipo == "pocao" and self.player.pocoes > 0:
            icone_rect = self.icone_pocao.get_rect(
                center=(x + tamanho // 2, y + tamanho // 2)
            )
            tela.blit(self.icone_pocao, icone_rect)
 
            # Contador de poções
            self._desenhar_contador_slot(tela, str(self.player.pocoes), x, y, tamanho)
 
            # Tecla "Q" abaixo do slot, indicando o botão de uso
            texto_tecla = self.fonte_slot.render("Q", True, settings.WHITE)
            tela.blit(
                texto_tecla,
                (x + tamanho // 2 - texto_tecla.get_width() // 2, y + tamanho + 2),
            )
 
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
        
        elif tipo == "gema" and self.player.tem_gema:
            icone_rect = self.icone_gema.get_rect(
                center=(x + tamanho // 2, y + tamanho // 2)
            )
            tela.blit(self.icone_gema, icone_rect)
    def _desenhar_contador_slot(self, tela, texto, x, y, tamanho):
        # desenha um numero no canto do slot, com sombra
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
    
    def checar_colisao_coletaveis(self):
        # Detecta colisão entre o player e coletáveis
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
            # cada inimigo so pode ser acertado uma vez por ataque
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
    
    def checar_queda(self):
        if self.estado != GameState.PLAYING:
            return
        
        if self.player.rect.top > settings.ALTURA_TELA:
            self.player.morrer_queda()
            self.estado = GameState.GAME_OVER

    def salvar_estado_jogador(self):
        if self.player_state is not None:
            self.player.salvar_estado(self.player_state)

    def terminou(self):
        return self.estado == GameState.PLAYING and self.player.rect.right >= settings.LARGURA_TELA
