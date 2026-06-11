"""Estados possíveis do fluxo do jogo."""

class GameState:
    # Tela/estado inicial de menu.
    MENU      = "menu"
    # Estado em que atualização e render jogável acontecem.
    PLAYING   = "playing"
    # Estado de pausa.
    PAUSED    = "paused"
    # Estado de derrota/fim de jogo.
    GAME_OVER = "game_over"
    # Estado de vitória.
    WIN       = "win"