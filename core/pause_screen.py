import pygame
 
import settings
 
 
class PauseScreen:
    """Overlay de pausa. Desenhado por cima do nível já renderizado (congelado)."""
 
    def __init__(self):
        self.continuar_solicitado = False
        self.sair_solicitado = False
        self.fonte_titulo = pygame.font.Font(None, settings.FONTE_TITULO_RESULTADO)
        self.fonte_texto = pygame.font.Font(None, settings.FONTE_TEXTO_RESULTADO)
 
    def processar_evento(self, evento):
        if evento.type != pygame.KEYDOWN:
            return
 
        tecla_pausar = pygame.key.key_code(settings.TECLA_PAUSAR)
 
        if evento.key == tecla_pausar:
            self.continuar_solicitado = True
        elif evento.key == pygame.K_ESCAPE:
            self.sair_solicitado = True
 
    def desenhar(self, tela):
        # Overlay escuro semi-transparente por cima do frame congelado do nível
        overlay = pygame.Surface((settings.LARGURA_TELA, settings.ALTURA_TELA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        tela.blit(overlay, (0, 0))
 
        titulo = self.fonte_titulo.render("Pausado", True, settings.WHITE)
        opcoes = self.fonte_texto.render(
            "[Esc] Continuar",
            True,
            settings.GRAY,
        )
 
        centro_x = settings.LARGURA_TELA // 2
        centro_y = settings.ALTURA_TELA // 2
 
        tela.blit(titulo, titulo.get_rect(center=(centro_x, centro_y - 40)))
        tela.blit(opcoes, opcoes.get_rect(center=(centro_x, centro_y + 40)))
