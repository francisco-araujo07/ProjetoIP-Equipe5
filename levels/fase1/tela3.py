import math

import pygame

import settings
from core.level import Level


class Fase1Tela3(Level):
    FUNDO = "assets/fase1/fase1-bg3-comespada.png"
    DIALOGOS = [
        "Os corredores ainda cheiram a pedra umida e tempo perdido.",
        "Tudo exatamente como eu deixei. Cada detalhe, cada sombra.",
        "Exceto isso.",
        "Uma espada esquecida num pedestal de pedra. Simples. Direta.",
        "Servira.",
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)

        # carrega a espada e ja calcula onde ela fica na tela
        self.espada_image = self._carregar_imagem_espada()
        self.espada_base_center = (
            settings.LARGURA_TELA // 2,
            settings.ALTURA_TELA - 205,
        )
        self.espada_rect = self.espada_image.get_rect(center=self.espada_base_center)
        self.fonte_prompt = pygame.font.Font(None, 30)

    def _carregar_imagem_espada(self):
        imagem = pygame.image.load(settings.SPRITE_ESPADA_COLETAVEL).convert_alpha()
        areas_visiveis = pygame.mask.from_surface(imagem).get_bounding_rects()

        # corta o espaco vazio em volta da espada na imagem
        if areas_visiveis:
            area = areas_visiveis[0].copy()
            for rect in areas_visiveis[1:]:
                area.union_ip(rect)
            imagem = imagem.subsurface(area).copy()

        escala = settings.ESPADA_COLETAVEL_ALTURA / imagem.get_height()
        tamanho = (int(imagem.get_width() * escala), int(imagem.get_height() * escala))
        imagem = pygame.transform.smoothscale(imagem, tamanho)
        return pygame.transform.rotate(imagem, settings.ESPADA_COLETAVEL_ROTACAO)

    def processar_evento(self, evento):
        if self.dialogo_ativo:
            super().processar_evento(evento)
            return

        # aperta E perto da espada pra pegar ela
        if (
            evento.type == pygame.KEYDOWN
            and evento.key == pygame.K_e
            and not self.player.tem_espada
            and self.player.rect.colliderect(self.espada_rect)
        ):
            self.player.tem_espada = True
            self.player.dano = settings.PLAYER_DANO
            self.player.atualizar_visual()
            self.salvar_estado_jogador()
            return

        super().processar_evento(evento)

    def desenhar(self, tela):
        super().desenhar(tela)

        if not self.player.tem_espada:
            self._desenhar_espada_animada(tela)

        if (
            not self.player.tem_espada
            and self.player.rect.colliderect(self.espada_rect)
            and not self.dialogo_ativo
        ):
            prompt = self.fonte_prompt.render("[E] Pegar espada", True, settings.WHITE)
            prompt_rect = prompt.get_rect(center=(self.espada_rect.centerx, self.espada_rect.top - 24))
            tela.blit(prompt, prompt_rect)

    def _desenhar_espada_animada(self, tela):
        # usa seno pra espada subir e descer e o brilho piscar, tipo flutuando
        tempo = pygame.time.get_ticks() / 300
        pulso = math.sin(tempo)
        deslocamento_y = int(pulso * 4)
        alpha = int(80 + ((pulso + 1) / 2) * 110)

        centro_x, centro_y = self.espada_base_center
        centro_y += deslocamento_y
        self.espada_rect = self.espada_image.get_rect(center=(centro_x, centro_y))
        self._desenhar_brilho_espada(tela, centro_x, centro_y, alpha)
        tela.blit(self.espada_image, self.espada_rect)

    def _desenhar_brilho_espada(self, tela, centro_x, centro_y, alpha):
        largura = self.espada_image.get_width() + 36
        altura = self.espada_image.get_height() + 36
        brilho = pygame.Surface((largura, altura), pygame.SRCALPHA)
        centro = (largura // 2, altura // 2)

        # desenha varios ovais um dentro do outro pra fazer o brilho ao redor da espada
        for escala, fator_alpha in ((0.52, 0.25), (0.38, 0.45), (0.24, 0.75)):
            rect = pygame.Rect(0, 0, int(largura * escala), int(altura * escala))
            rect.center = centro
            cor = (255, 220, 90, int(alpha * fator_alpha))
            pygame.draw.ellipse(brilho, cor, rect)

        tela.blit(brilho, (centro_x - largura // 2, centro_y - altura // 2))

    def terminou(self):
        return super().terminou() and self.player.tem_espada
