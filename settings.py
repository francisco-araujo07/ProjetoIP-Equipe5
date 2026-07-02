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

# --- Assets ---
SPRITE_PLAYER_SEM_ESPADA = "assets/fase1/player-sem-espada.png"
SPRITE_PLAYER_COM_ESPADA = "assets/fase1/player-com-espada.png"
SPRITESHEET_PLAYER_PARADO = "assets/player/spritesheet-jogador-parado.png"
SPRITESHEET_PLAYER_CORRENDO = "assets/player/spritesheet-jogador-correndo.png"
SPRITE_PLAYER_ATACANDO = "assets/player/sprite-jogador-atacando.png"
SPRITESHEET_INIMIGO_ANDANDO = "assets/inimigos/spritesheet-inimigo-andando.png"
SPRITESHEET_BOSS_ANDANDO = "assets/inimigos/spritesheet-boss-andando.png"
SPRITESHEET_FRAMES = 7
PLAYER_LARGURA_BASE = 40
PLAYER_ALTURA_BASE = 56
PLAYER_ALTURA_SPRITE = 140
PLAYER_ANIMATION_SPEED = 0.09
INIMIGO_ANIMATION_SPEED = 0.05
IMAGEM_FRAGMENTO = "assets/coletavel/fragmento-chave.png.png"
FRAGMENTO_CHAVE_TAMANHO = 123
FRAGMENTO_CHAVE_ROTACAO = -45
SPRITE_ESPADA_COLETAVEL = "assets/coletavel/espada.png"
ESPADA_COLETAVEL_ALTURA = 150
ESPADA_COLETAVEL_ROTACAO = -60
SPRITE_ALAVANCA = "assets/fase2/alavanca.png"
ALAVANCA_ALTURA = 96
ICONE_HUD_CORACAO_CHEIO = "assets/hud/coracao.png"
ICONE_HUD_CORACAO_VAZIO = "assets/hud/coracaovazio.png"
ICONE_HUD_POCAO = "assets/coletavel/pocao.png"
ICONE_HUD_GEMA = "assets/coletavel/gema.png"
TAM_ICONE_CORACAO = 25
ESPACO_CORACAO_HUD     = 2    
Y_INICIO_CORACOES_HUD  = 20   
TAM_ICONE = 32
X_INICIO_HUD = 20  
TAM_SLOT_HUD          = 36    
ESPACO_SLOT_HUD       = 4    
Y_INICIO_SLOTS_HUD    = 46
TAM_ICONE_SLOT        = 32
ROTACAO_ICONE_SLOT    = -45



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
TECLA_PULAR_PLAYER = "space"
TECLA_USAR_POCAO = "q"
PLAYER_ATAQUE_ALCANCE = 90
PLAYER_ATAQUE_ALTURA = 70
PLAYER_ATAQUE_DURACAO_MS = 220
PLAYER_ATAQUE_COOLDOWN_MS = 400

# --- Dialogo ---
TYPEWRITER_LETRAS_POR_SEGUNDO = 30

# --- Telas de resultado ---
TECLA_REINICIAR_JOGO = "r"
TECLA_SAIR_JOGO = "escape"
FONTE_TITULO_RESULTADO = 96
FONTE_TEXTO_RESULTADO = 36

# --- Inimigos ---
SAQUEADOR_VIDA = 10
SAQUEADOR_DANO = 10
SAQUEADOR_VELOCIDADE = 2
AUTOMATO_VIDA = 30
AUTOMATO_DANO = 20
AUTOMATO_VELOCIDADE = 1

# --- Tipos de Coletável ---
POCAO_CURA = 50
TIPO_DANO       = "dano"
TIPO_VELOCIDADE = "velocidade"

# --- Armadilhas ---
ESPINHOS_DANO = 20
FASE2_TELA1_ESPINHOS_RECT = (675, ALTURA_TELA - 198, 225, 64)
FASE2_TELA1_MECANISMO_RECT = (595, ALTURA_TELA - 238, 95, 86)

# --- Valores de Upgrade(Caso necessário alterar) ---
UPGRADE_VIDA       = 20
UPGRADE_DANO       = 5
UPGRADE_VELOCIDADE = 1
