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

## 🏗️ Arquitetura

<details>
<summary><b>Ver estrutura de pastas</b></summary>

```
PROJETOIP-EQUIPE5/
├── assets/                  # Sprites, sons e imagens
├── classes/                 # Entidades (POO)
│   ├── armadilha.py
│   ├── coletavel.py
│   ├── enemy.py
│   ├── plataforma.py
│   └── player.py
├── core/                    # Engine / estado do jogo
│   ├── game.py               # Loop principal
│   ├── game_state.py         # Estado geral da partida
│   ├── level.py               # Lógica das fases
│   ├── menu.py                 # Tela inicial
│   ├── player_state.py         # Estado do player (HP, itens)
│   └── result_screen.py        # Telas de vitória/derrota
├── guia/                    # Planejamento técnico interno
├── levels/                  # Dados/configuração das fases
├── main.py                  # Entry point
├── settings.py               # Configurações globais
├── requirements.txt
├── FLUXO_JOGO.md             # Fluxograma de planejamento
└── README.md
```

</details>

**Separação de responsabilidades:** `classes/` = entidades (dados + comportamento); `core/` = engine (loop, estados, transições). `guia/` e `FLUXO_JOGO.md` documentam o planejamento adotado após o replanejamento do projeto.

> `main_teste.py` e `teste.plataforma_movel.py` — scripts de debug, sem função no build final.

---

## 🛠️ Stack

<table>
<tr><th>Tecnologia</th><th>Justificativa</th></tr>
<tr><td><b>Python</b></td><td>Linguagem base da disciplina</td></tr>
<tr><td><b>pygame-ce</b></td><td>Fork ativo do pygame; usado por incompatibilidade do pygame original com Python 3.13+</td></tr>
<tr><td><b>os</b></td><td>Manipulação de caminhos de arquivos de áudio e imagem</td></tr>
</table>

---

## 🖼️ Galeria

<div align="center">
<table>
<tr>
<td><img src="assets/screenshots/tela_inicial.png" width="400"/><br/><sub>Tela inicial</sub></td>
<td><img src="assets/screenshots/assalto_falhou.png" width="400"/><br/><sub>Derrota</sub></td>
</tr>
<tr>
<td><img src="assets/screenshots/gameplay_sala_chave.png" width="400"/><br/><sub>Gameplay: sala da chave</sub></td>
<td><img src="assets/screenshots/gameplay_santuario.png" width="400"/><br/><sub>Gameplay: santuário</sub></td>
</tr>
<tr>
<td colspan="2" align="center"><img src="assets/screenshots/vitoria.png" width="400"/><br/><sub>Vitória</sub></td>
</tr>
</table>
</div>

---

## 📚 Conceitos da Disciplina Aplicados

<table>
<tr><th>Conceito</th><th>Onde foi usado</th></tr>
<tr><td><b>Laços de repetição</b></td><td><code>core/game.py</code> — loop principal, atualiza entidades a cada frame</td></tr>
<tr><td><b>Condicionais</b></td><td>Colisão/movimento em <code>classes/player.py</code>, <code>enemy.py</code>, <code>plataforma.py</code>; verificação de HP/itens em <code>core/player_state.py</code></td></tr>
<tr><td><b>Funções</b></td><td>Modularização — um comportamento por arquivo em <code>classes/</code> e <code>core/</code></td></tr>
<tr><td><b>POO</b></td><td><code>classes/player.py</code> (Player), <code>enemy.py</code> (Enemy), <code>coletavel.py</code> (Coletável), <code>armadilha.py</code> (Armadilha), <code>plataforma.py</code> (Plataforma)</td></tr>
</table>

---

## 🧩 Desafios e Lições Aprendidas

<details>
<summary><b>Maior erro cometido</b></summary>
<br/>
Começar a codar antes de finalizar o planejamento visual do jogo e das fases. Solução: descarte do código inicial e reinício com planejamento prévio (documentado em <code>guia/</code> e <code>FLUXO_JOGO.md</code>).
</details>

<details>
<summary><b>Maior desafio enfrentado</b></summary>
<br/>
Trabalho em equipe com 6 pessoas em módulos interdependentes. Resolvido com comunicação mais clara e divisão de tasks.
</details>

<details>
<summary><b>Lições aprendidas</b></summary>
<br/>

- Planejamento pré-desenvolvimento é essencial para alinhamento do objetivo final.
- Gestão de tempo e divisão de tasks evita sobrecarga individual.

</details>