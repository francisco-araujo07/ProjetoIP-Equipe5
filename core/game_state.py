# core/game_state.py
"""Estados possíveis do fluxo do jogo."""

class GameState:
    # Tela/estado inicial de menu.
    MENU      = "menu"
    
    # Estado em que atualização e render jogável acontecem (Fases).
    PLAYING   = "playing"
    
    # Estado de pausa (congelamento de tela).
    PAUSED    = "paused"
    
    # Estado de derrota/fim de jogo (Silas sem corações).
    GAME_OVER = "game_over"
    
    # Estado de vitória (ao derrotar o Colosso Mecânico).
    WIN       = "win"