import pygame
import settings
from core.player_state import PlayerState
from levels.fase3.tela3 import Fase3Tela3

pygame.init()
tela = pygame.display.set_mode((settings.LARGURA_TELA, settings.ALTURA_TELA))
clock = pygame.time.Clock()
state = PlayerState(tem_espada=True, dano_atual=10)  # simula jogador com espada
nivel = Fase3Tela3(state)

rodando = True
while rodando:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            rodando = False
        nivel.processar_evento(ev)
    nivel.atualizar()
    nivel.desenhar(tela)
    pygame.display.flip()
    clock.tick(settings.FPS)

# Verificar após fechar:
print("tem_gema:", state.tem_gema)
print("dano_atual:", state.dano_atual)  # deve ser 20