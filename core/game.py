import pygame
import settings
from levels.fase1.tela1 import Fase1Tela1
from levels.fase1.tela2 import Fase1Tela2
from levels.fase1.tela3 import Fase1Tela3
from levels.fase1.tela4 import Fase1Tela4
from levels.fase1.tela5 import Fase1Tela5

# Classe principal do jogo, responsável por gerenciar o loop principal, eventos, atualizações e renderização.
class Game:

    # Sequência de telas na ordem em que devem ser jogadas
    SEQUENCIA_LEVELS = [
        Fase1Tela1,
        Fase1Tela2,
        Fase1Tela3,
        Fase1Tela4,
        Fase1Tela5,
    ]

    def __init__(self):
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

        # Índice da tela atual dentro de SEQUENCIA_LEVELS
        self.nivel_atual = 0
        self.nivel = self.SEQUENCIA_LEVELS[0]()

    # Avança para a próxima tela; encerra o jogo se todas foram concluídas
    def _avancar_nivel(self):
        self.nivel_atual += 1
        if self.nivel_atual < len(self.SEQUENCIA_LEVELS):
            self.nivel = self.SEQUENCIA_LEVELS[self.nivel_atual]()
        else:
            self.rodando = False  # Todas as telas concluídas

    # Processa os eventos do jogo, como fechar a janela
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            self.nivel.processar_evento(evento)
    
    # Atualiza o estado do jogo.
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False

    # Atualiza o estado do jogo e verifica se deve avançar de tela
    def atualizar(self):
        self.nivel.atualizar()
        if self.nivel.terminou():
            self._avancar_nivel()

    # Desenha o estado atual do jogo na tela
    def desenhar(self):
        self.nivel.desenhar(self.tela)
        pygame.display.flip()

    # Usa os outros métodos para rodar o loop principal do jogo, controlando o tempo para manter o FPS constante
    def rodar(self):
        while self.rodando:
            self.processar_eventos()
            self.atualizar()
            self.desenhar()
            self.clock.tick(settings.FPS)

        pygame.quit()
