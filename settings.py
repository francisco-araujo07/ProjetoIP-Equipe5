"""Constantes globais usadas por todo o projeto."""

# ============================================================
#  Settings.py — única fonte de constantes do projeto
#  Todos os outros arquivos importam daqui. Proibido número
#  mágico fora deste arquivo.
# ============================================================

# --- Display ---
LARGURA_TELA = 1280
ALTURA_TELA = 720
RENDER_WIDTH  = 0
RENDER_HEIGHT = 0
FPS           = 60
TITULO_TESTE = "Phyntom"



# --- Cores (R, G, B) ---
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (220, 50,  50)
GREEN  = (50,  200, 50)
BLUE   = (50,  100, 220)
YELLOW = (255, 220, 0)
GRAY   = (150, 150, 150)
ORANGE = (255, 120, 0)



# --- Física do Player ---
VELOCIDADE_PLAYER = 5
GRAVIDADE = 0.5
FORCA_PULO = 15
VELOCIDADE_MAX_QUEDA = 20
DURACAO_INVENCIBILIDADE = 2000


# --- Atributos do Player ---
PLAYER_VIDA_MAX = 100
PLAYER_DANO = 10

# --- Ataque melee do Player ---
TECLA_ATAQUE_PLAYER = "z"
PLAYER_ATAQUE_ALCANCE = 45
PLAYER_ATAQUE_ALTURA = 32
PLAYER_ATAQUE_DURACAO_MS = 120
PLAYER_ATAQUE_COOLDOWN_MS = 400

# --- Tipos de Coletável ---
TIPO_VIDA       = "vida"
TIPO_DANO       = "dano"
TIPO_VELOCIDADE = "velocidade"

# --- Valores de Upgrade(Caso necessário alterar) ---
UPGRADE_VIDA       = 20
UPGRADE_DANO       = 5
UPGRADE_VELOCIDADE = 1
