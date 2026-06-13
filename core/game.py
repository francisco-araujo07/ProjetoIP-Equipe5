import pygame 
import settings
from core.level import Level

# Classe principal do jogo, responsável por gerenciar o loop principal, eventos, atualizações e renderização.
class Game:
    
    def __init__(self): # Inicializa o jogo, configurando a tela, o FPS (clock) e o nível.
        # Inicialização do Pygame e configuração da tela
        pygame.init()
       
        # Configurações da tela
        self.tela = pygame.display.set_mode((settings.LARGURA_TELA, settings.ALTURA_TELA))
       
        # Configura o título da janela
        pygame.display.set_caption(settings.TITULO_TESTE)
        
        # Configura o relógio para controlar o FPS
        self.clock = pygame.time.Clock()
        
        # Inicializa o estado do jogo
        self.rodando = True

        # Inicializa o nível do jogo
        self.nivel = Level()

    # Processa os eventos do jogo, como fechar a janela.
    def processar_eventos(self):
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
    
    # Atualiza o estado do jogo.
    def atualizar(self):
        self.nivel.atualizar()
    
    # Desenha o estado atual do jogo na tela.
    def desenhar(self):
        self.nivel.desenhar(self.tela)
        pygame.display.flip()

    # Usa os outros métodos para rodar o loop principal do jogo, controlando o tempo para manter o FPS constante.
    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(settings.FPS)

        pygame.quit()