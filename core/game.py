import pygame 
import settings
from core.level import Level


class Game:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((settings.LARGURA_TELA, settings.ALTURA_TELA))
        pygame.display.set_caption(settings.TITULO_TESTE)
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.nivel = Level()


    def processar_eventos(self):
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False

    def atualizar(self):
        self.nivel.atualizar()
    
    def desenhar(self):
        self.nivel.desenhar(self.tela)
        pygame.display.flip()


    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(settings.FPS)

        pygame.quit()