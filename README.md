<div align="center">

<img src="assets/screenshots/tela_inicial.png" alt="Gilded Shadows" width="600"/>

# ⚔️ Gilded Shadows

<p>
  <img src="https://img.shields.io/badge/Python-3.13+-blue?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/pygame--ce-2.5+-green?logo=pygame&logoColor=white" alt="pygame-ce"/>
  <img src="https://img.shields.io/badge/status-conclu%C3%ADdo-success" alt="status"/>
</p>

Jogo 2D desenvolvido em Python + pygame-ce, projeto da disciplina de Introdução à Programação.

</div>

---

## 👥 Equipe

<table>
<tr><th>Membro</th><th>Responsabilidade</th></tr>
<tr><td><b>Francisco Estevão</b></td><td>Logística do <code>game.py</code> e estrutura dos levels</td></tr>
<tr><td><b>Francisco Gabriel</b></td><td>Sprites, funções iniciais/finais e suas telas</td></tr>
<tr><td><b>Pedro Augusto</b></td><td>Lore e mecânica dos coletáveis</td></tr>
<tr><td><b>Matheus Agra</b></td><td>Divisão de tasks; mecânica do player e inimigos</td></tr>
<tr><td><b>João Ricardo</b></td><td>Mecânicas de coletáveis e lógica interna das fases</td></tr>
<tr><td><b>Alam Menezes</b></td><td>Colisão e plataformas fixas/móveis</td></tr>
</table>

---

# Gilded Shadows

Platformer de ação 2D single-player em **Python + Pygame**. Projeto da disciplina de **Introdução à Programação (IP)** — Centro de Informática (CIn/UFPE), Equipe 5.

## Enredo

Você é **Silas**, arquiteto do castelo do Rei Aurum, preso sete anos por "saber demais". Ele retorna às masmorras que projetou para reunir os três fragmentos da **Chave Mestra**, abrir o **Cofre de Aurum** e enfrentar o guardião final. No caminho: guardas, armadilhas e um boss mecânico.

## Objetivo do projeto

Construir um platformer completo aplicando POO, modularização, game loop, máquina de estados e física de colisão — do menu à tela de vitória, com progressão encadeada por fases e persistência do estado do jogador entre telas.

---

## Como rodar

**Pré-requisitos:** Python 3.

```bash
# 1. ambiente virtual
python -m venv venv

# 2. ativar (Windows / PowerShell)
.\venv\Scripts\Activate.ps1
#   erro de permissão? rode antes:
#   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# 3. dependências
pip install -r requirements.txt

# 4. executar
python main.py
```

---

## Controles

**Jogo**
- Mover: `A`/`←` e `D`/`→`
- Pular: `SPACE`, `W` ou `↑`
- Atacar: `Z` ou clique esquerdo
- Usar poção: `Q`
- Interagir (pedestal/mecanismo): `E`

**Sistema**
- `ESC` — pausar
- `F11` — tela cheia
- Nas telas de fim de jogo: `R` reinicia · `ESC`/`Q` sai

---

## Mecânicas

**Combate**
- Melee com hitbox direcional, cooldown de 400ms e golpe de 220ms
- Cada inimigo recebe dano uma única vez por golpe
- Vida com corações no HUD; i-frames com efeito de piscar após dano
- Poções de cura no inventário

**Inimigos**
- **Saqueador** — patrulha rápida, pouca vida
- **Autômato** — tanque lento, muita vida
- **Colosso (boss)** — máquina de estados `Perseguindo → Telegrafando → Atacando → Vulnerável`; só recebe dano na janela de vulnerabilidade; barra de vida própria e morte com fade-out

**Plataforma e física**
- Colisão resolvida em X e Y separadamente
- Distinção entre contato lateral e topo/base por sobreposição
- Plataformas móveis (eixo X ou Y) que arrastam o jogador
- Gravidade com teto de queda; morte ao cair fora do mapa

**Coletáveis**
- **Poção** — guardada e usada com `Q`
- **Fragmento de Chave** — reunir 3 para progredir
- **Gema** — dobra o dano e adiciona brilho ao personagem
- Efeitos persistem entre telas; guarda contra aplicação dupla ao recarregar

**Outros sistemas**
- Armadilha de espinhos desativável por mecanismo (`E`), com troca de sprite/fundo
- Diálogos com efeito máquina de escrever (~30 letras/s), congelando o jogo
- HUD com corações e slots de inventário
- Menu inicial, pausa, game over e vitória

---

## Estrutura

```
ProjetoIP-Equipe5/
├── main.py               # ponto de entrada
├── settings.py           # constantes globais
├── requirements.txt
│
├── core/                 # motor e fluxo
│   ├── game.py           # loop principal + máquina de estados
│   ├── game_state.py     # enum de estados
│   ├── player_state.py   # dataclass de persistência entre fases
│   ├── level.py          # classe base Level (motor de fase)
│   ├── menu.py           # tela inicial
│   ├── pause_screen.py   # tela de pausa
│   └── result_screen.py  # game over / vitória
│
├── classes/              # entidades do mundo
│   ├── player.py         # física, animação, ataque
│   ├── enemy.py          # inimigos e boss
│   ├── plataforma.py     # plataformas + funções de colisão
│   ├── coletavel.py      # itens e efeitos
│   └── armadilha.py      # espinhos
│
├── levels/               # 12 telas encadeadas
│   ├── fase1/            # telas 1–5
│   ├── fase2/            # telas 1–3
│   ├── fase3/            # telas 1–3
│   └── fase4/            # tela 1 (boss)
│
└── assets/               # sprites, fundos e UI
    ├── player/  inimigos/  coletavel/  comum/
    ├── hud/  menu/  game_over/  vitoria/
    └── fase1/ … fase4/
```

**Progressão:** Menu → Fase 1 (5 telas) → Fase 2 (3) → Fase 3 (3) → Fase 4 (boss) → Vitória → reiniciar ou sair.

---

## Tecnologias

- **Python 3**
- **Pygame** — engine
- **Visual Studio Code**

---

## Conceitos aplicados

POO (herança, polimorfismo) · Template Method (base `Level` e coletáveis) · modularização e separação de responsabilidades · game loop · máquina de estados · colisão em dois eixos · manipulação de spritesheets · eventos em tempo real · física de plataforma · clean code.

---

## Roadmap

Efeitos sonoros e trilha · mais inimigos · animação de ataque multi-frame · checkpoints · balanceamento de dano/vida · novos itens.

---


## Licença

Projeto acadêmico, para fins educacionais.
