import pygame

import settings
from classes.armadilha import ArmadilhaEspinhos
from core.game_state import GameState
from core.level import Level


class Fase2Tela1(Level):
    FUNDO = "assets/fase2/fase2-tela1-ativada.png"
    FUNDO_ARMADILHA_DESATIVADA = "assets/fase2/fase2-tela1-desativada.png"
    DIALOGOS = [
        "As catacumbas ainda respiram como uma maquina velha.",
        "Pedra umida, ferro oxidado... e dentes sob o piso.",
        "Eu conheco esta armadilha. Desenhei cada espinho dela.",
        "Aurum manteve meu trabalho, mas nunca entendeu minhas travas de seguranca.",
        "Se eu chegar perto do mecanismo, um toque em E basta para calar esses dentes.",
    ]

    LAYOUT_PLATAFORMAS = [
        (0, settings.ALTURA_TELA - 152, settings.LARGURA_TELA, 152),
    ]

    def __init__(self, player_state=None):
        super().__init__(player_state)

        # guarda o fundo alternativo pra trocar quando a armadilha for desativada
        self.fundo_armadilha_desativada = self._carregar_fundo(self.FUNDO_ARMADILHA_DESATIVADA)
        self.armadilha = ArmadilhaEspinhos(settings.FASE2_TELA1_ESPINHOS_RECT)
        self.mecanismo_rect = pygame.Rect(settings.FASE2_TELA1_MECANISMO_RECT)  

        imagem_normal_recortada = self._recortar_alavanca(settings.SPRITE_ALAVANCA)
        imagem_pressionada_recortada = self._recortar_alavanca(settings.SPRITE_ALAVANCA_PRESSIONADA)

        escala_alavanca = settings.ALAVANCA_ALTURA / imagem_normal_recortada.get_height()

        self.alavanca_imagem_normal = self._escalar_alavanca(imagem_normal_recortada, escala_alavanca)
        self.alavanca_imagem_pressionada = self._escalar_alavanca(imagem_pressionada_recortada, escala_alavanca)
        self.alavanca_image = self.alavanca_imagem_normal
        self.alavanca_rect = self.alavanca_image.get_rect(midbottom=self.mecanismo_rect.midbottom)  

        self.fonte_prompt = pygame.font.Font(None, 30)
    def _carregar_fundo(self, caminho):
        fundo = pygame.image.load(caminho).convert()
        return pygame.transform.scale(fundo, (settings.LARGURA_TELA, settings.ALTURA_TELA))

    def _carregar_alavanca(self, caminho):
        imagem = pygame.image.load(caminho).convert_alpha()
        areas_visiveis = pygame.mask.from_surface(imagem).get_bounding_rects()

        if areas_visiveis:
            area = areas_visiveis[0].copy()
            for rect in areas_visiveis[1:]:
                area.union_ip(rect)
            imagem = imagem.subsurface(area).copy()

        escala = settings.ALAVANCA_ALTURA / imagem.get_height()
        tamanho = (int(imagem.get_width() * escala * 0.6), settings.ALAVANCA_ALTURA * 0.6)
        return pygame.transform.smoothscale(imagem, tamanho)
    
    def _recortar_alavanca(self, caminho):
        imagem = pygame.image.load(caminho).convert_alpha()
        areas_visiveis = pygame.mask.from_surface(imagem).get_bounding_rects()

        if areas_visiveis:
            area = areas_visiveis[0].copy()
            for rect in areas_visiveis[1:]:
                area.union_ip(rect)
            imagem = imagem.subsurface(area).copy()

        return imagem

    def _escalar_alavanca(self, imagem, escala):
        tamanho = (
            max(1, int(imagem.get_width() * escala * 0.6)),
            max(1, int(imagem.get_height() * escala * 0.6)),
        )
        return pygame.transform.smoothscale(imagem, tamanho)

    def processar_evento(self, evento):
        if self.dialogo_ativo:
            super().processar_evento(evento)
            return

        # aperta E perto do mecanismo pra desligar a armadilha e trocar o fundo/alavanca
        if (
            evento.type == pygame.KEYDOWN
            and evento.key == pygame.K_e
            and self.armadilha.ativa
            and self.player.rect.colliderect(self.mecanismo_rect)
        ):
            self.armadilha.desativar()
            self.fundo = self.fundo_armadilha_desativada
            self.alavanca_image = self.alavanca_imagem_pressionada
            self.alavanca_rect = self.alavanca_image.get_rect(midbottom=self.mecanismo_rect.midbottom)
            return

        super().processar_evento(evento)

    def atualizar(self):
        super().atualizar()

        if self.dialogo_ativo or self.estado != GameState.PLAYING:
            return

        self.armadilha.aplicar_dano(self.player)

        if not self.player.esta_vivo():
            self.estado = GameState.GAME_OVER
            return

        self.salvar_estado_jogador()

    def desenhar_mundo_extra(self, tela):
        tela.blit(self.alavanca_image, self.alavanca_rect)
        if self.pode_desativar_armadilha():
            prompt = self.fonte_prompt.render("[E] Desativar armadilha", True, settings.WHITE)
            prompt_rect = prompt.get_rect(center=(self.mecanismo_rect.centerx, self.mecanismo_rect.top - 24))
            tela.blit(prompt, prompt_rect)

    def pode_desativar_armadilha(self):
        return (
            not self.dialogo_ativo
            and self.armadilha.ativa
            and self.player.rect.colliderect(self.mecanismo_rect)
        )