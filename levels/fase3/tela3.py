import math

import pygame

import settings
from classes.coletavel import FragmentoChave, Pocao
from classes.enemy import Automato
from core.level import Level


class Fase3Tela3(Level):
    FUNDO = "assets/fase3/fase3-tela3-porta_fechada.png"
    FUNDO_PORTA_ABERTA = "assets/fase3/fase3-tela3-porta_aberta.png"

    DIALOGOS = [
        "O ultimo fragmento esta preso ao pistao central.",
        "Tres partes. Tres mentiras de Aurum. Agora, todas de volta ao arquiteto.",
        "Sinto a Chave Mestra se moldando no meu bolso. Os dentes do cofre estao prestes a ceder.",
        "Basta passar por este ultimo guarda e o rei sabera o que e o verdadeiro medo.",
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 90, settings.LARGURA_TELA, 90),
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)

        self.fundo_porta_aberta = self._carregar_fundo(self.FUNDO_PORTA_ABERTA)

        self.pedestal_rect = pygame.Rect(
            settings.LARGURA_TELA // 2 - 45,
            settings.ALTURA_TELA - 370,
            90,
            118,
        )
        self.fragmento = FragmentoChave(0, 0)
        self.fragmento.image = self._carregar_imagem_fragmento()
        self.fragmento_base_center = (self.pedestal_rect.centerx, self.pedestal_rect.y + 30)
        self.fragmento_coletado = self.player.fragmentos_chave >= 3
        self.fonte_prompt = pygame.font.Font(None, 30)

        # se ja pegou o fragmento, a porta ja comeca aberta
        if self.fragmento_coletado:
            self.fundo = self.fundo_porta_aberta

        self.mensagem_ativa = False
        self.inicio_mensagem_ms = 0
        self.fonte_mensagem = pygame.font.Font(None, 64)

        y_chao = settings.ALTURA_TELA - 90
        automato = Automato(
            self.pedestal_rect.centerx,
            y_chao - 64,
            self.pedestal_rect.left - 150,
            self.pedestal_rect.right + 150,
        )
        self.grupo_inimigos.add(automato)
        pocao = Pocao(300, y_chao - 32)
        self.coletaveis.add(pocao)

    def _carregar_fundo(self, caminho):
        fundo = pygame.image.load(caminho).convert()
        return pygame.transform.scale(fundo, (settings.LARGURA_TELA, settings.ALTURA_TELA))

    def _carregar_imagem_fragmento(self):
        imagem = pygame.image.load(settings.IMAGEM_FRAGMENTO).convert_alpha()
        tamanho = (settings.FRAGMENTO_CHAVE_TAMANHO, settings.FRAGMENTO_CHAVE_TAMANHO)
        imagem = pygame.transform.smoothscale(imagem, tamanho)
        return pygame.transform.rotate(imagem, settings.FRAGMENTO_CHAVE_ROTACAO)

    def processar_evento(self, evento):
        if self.dialogo_ativo:
            super().processar_evento(evento)
            return

        if (
            evento.type == pygame.KEYDOWN
            and evento.key == pygame.K_e
            and self.pode_coletar_fragmento()
        ):
            # pegou o fragmento: troca o fundo pra porta aberta e mostra a mensagem
            self.fragmento.coletar(self.player)
            self.fragmento_coletado = True
            self.fundo = self.fundo_porta_aberta
            self.mensagem_ativa = True
            self.inicio_mensagem_ms = pygame.time.get_ticks()
            self.salvar_estado_jogador()
            return

        super().processar_evento(evento)

    def pode_coletar_fragmento(self):
        return (
            not self.fragmento_coletado
            and len(self.grupo_inimigos) == 0
            and self.player.rect.colliderect(self.pedestal_rect)
        )

    def atualizar(self):
        super().atualizar()

        if self.mensagem_ativa:
            agora = pygame.time.get_ticks()
            if agora - self.inicio_mensagem_ms >= settings.DURACAO_MENSAGEM_CONCLUSAO_MS:
                self.mensagem_ativa = False

    def desenhar(self, tela):
        super().desenhar(tela)

        if not self.fragmento_coletado:
            self._desenhar_fragmento_animado(tela)

        if self.pode_coletar_fragmento() and not self.dialogo_ativo:
            prompt = self.fonte_prompt.render("[E] Pegar fragmento", True, settings.WHITE)
            tela.blit(prompt, (self.pedestal_rect.x - 62, self.pedestal_rect.y - 42))

        if self.mensagem_ativa:
            self._desenhar_banner_conclusao(tela)

    def _desenhar_fragmento_animado(self, tela):
        tempo = pygame.time.get_ticks() / 300
        pulso = math.sin(tempo)
        deslocamento_y = int(pulso * 4)
        alpha = int(80 + ((pulso + 1) / 2) * 110)

        centro_x, centro_y = self.fragmento_base_center
        centro_y += deslocamento_y
        self._desenhar_brilho_fragmento(tela, centro_x, centro_y, alpha)

        rect = self.fragmento.image.get_rect(center=(centro_x, centro_y))
        tela.blit(self.fragmento.image, rect)

    def _desenhar_brilho_fragmento(self, tela, centro_x, centro_y, alpha):
        brilho = pygame.Surface((96, 96), pygame.SRCALPHA)
        centro = (48, 48)

        for raio, fator_alpha in ((42, 0.25), (30, 0.45), (18, 0.75)):
            cor = (255, 210, 70, int(alpha * fator_alpha))
            pygame.draw.circle(brilho, cor, centro, raio)

        tela.blit(brilho, (centro_x - 48, centro_y - 48))

    def _desenhar_banner_conclusao(self, tela):
        # mostra o aviso de "Chave Mestra Concluida" na tela
        texto = self.fonte_mensagem.render("Chave Mestra Concluida!", True, settings.YELLOW)
        centro_x = settings.LARGURA_TELA // 2
        centro_y = 110

        caixa = pygame.Surface((texto.get_width() + 48, texto.get_height() + 24), pygame.SRCALPHA)
        caixa.fill((0, 0, 0, 170))
        tela.blit(caixa, caixa.get_rect(center=(centro_x, centro_y)))
        tela.blit(texto, texto.get_rect(center=(centro_x, centro_y)))

    def terminou(self):
        return super().terminou() and self.fragmento_coletado
