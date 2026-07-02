import math

import pygame

import settings
from classes.coletavel import FragmentoChave
from classes.enemy import Saqueador
from core.level import Level


class Fase2Tela3(Level):
    FUNDO = "assets/fase2/fase2-tela3.png"
    IMAGEM_FRAGMENTO = "assets/fase1/fragmento-chave.png.png"
    DIALOGOS = [
        "Dois guardas para um fragmento. Aurum esta levando meu trabalho a serio.",
        "Nao importa. Projetei cada corredor deste castelo. Eu sei como sair daqui.",
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)

        self.pedestal_rect = pygame.Rect(
            900 - 45,
            settings.ALTURA_TELA - 370,
            90,
            118,
        )
        self.fragmento = FragmentoChave(0, 0)
        self.fragmento.image = self._carregar_imagem_fragmento()
        self.fragmento_base_center = (self.pedestal_rect.centerx - 130, self.pedestal_rect.y + 26)
        self.fragmento_coletado = self.player.fragmentos_chave >= 2
        self.fonte_prompt = pygame.font.Font(None, 30)

        y_chao = settings.ALTURA_TELA - 152
        s1 = Saqueador(550, y_chao - 56, 500, 850)
        s2 = Saqueador(1000, y_chao - 56, 850, 1200)
        self.grupo_inimigos.add(s1, s2)

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
            self.fragmento.coletar(self.player)
            self.fragmento_coletado = True
            self.salvar_estado_jogador()
            return

        super().processar_evento(evento)

    def pode_coletar_fragmento(self):
        return (
            not self.fragmento_coletado
            and len(self.grupo_inimigos) == 0
            and self.player.rect.colliderect(self.pedestal_rect)
        )

    def desenhar(self, tela):
        super().desenhar(tela)

        if not self.fragmento_coletado:
            self._desenhar_fragmento_animado(tela)

        if self.pode_coletar_fragmento() and not self.dialogo_ativo:
            prompt = self.fonte_prompt.render("[E] Pegar fragmento", True, settings.WHITE)
            tela.blit(prompt, (self.pedestal_rect.x - 62, self.pedestal_rect.y - 42))

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

    def terminou(self):
        return super().terminou() and self.fragmento_coletado
