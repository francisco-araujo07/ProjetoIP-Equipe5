from dataclasses import dataclass

import settings


@dataclass
class PlayerState:
    # guarda os dados do player que passam de uma fase pra outra
    tem_espada: bool = False
    fragmentos_chave: int = 0
    tem_gema: bool = False
    vida_atual: int = settings.PLAYER_VIDA_MAX
    dano_atual: int = settings.PLAYER_DANO
    pocoes: int = 0
