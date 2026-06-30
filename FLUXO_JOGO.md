# Gilded Shadows — Fluxo Completo do Jogo

> **Como usar este documento:**
> Cada seção representa uma tela ou momento do jogo na ordem exata em que o jogador vai experienciá-los.
> Nada entra aqui sem confirmação da equipe.

---

## 1. Prólogo (Tela de Texto Estilo RPG)

- Fundo escuro, sem gameplay
- Texto aparece letra por letra (efeito typewriter, ~30 letras/s)
- Dividido em painéis; jogador pressiona qualquer tecla para avançar
- Se pressionar durante a animação → completa o texto instantaneamente
- Se pressionar com texto completo → vai para o próximo painel
- Após o último painel → transição para a Fase 1

**Painéis de texto — Tela 1 (floresta, ao longe do castelo):**
1. "Sete anos. É quanto tempo passei nessas masmorras."
2. "Não fui preso por ser fraco. Fui preso por saber demais."
3. "Cada corredor, cada alavanca, cada armadilha daquele castelo... projetei com minhas próprias mãos."
4. "O Rei Aurum me prometeu liberdade. Me deu correntes."
5. "Hoje, as correntes são dele."

---

## 2. Fase 1 — Os Jardins Suspensos

> Entrada do castelo tomada pela vegetação. Luz natural e ruínas de mármore.
> Dificuldade: Fácil. Introdução aos controles.

- **Tela 1:** Prólogo em texto estilo RPG (typewriter) → jogador fica livre para andar → chegar na borda direita avança para a Tela 2

  **Painéis de texto — Tela 1 (floresta, ao longe do castelo):**
  1. "Sete anos. É quanto tempo passei nessas masmorras."
  2. "Não fui preso por ser fraco. Fui preso por saber demais."
  3. "Cada corredor, cada alavanca, cada armadilha daquele castelo... projetei com minhas próprias mãos."
  4. "O Rei Aurum me prometeu liberdade. Me deu correntes."
  5. "Hoje, as correntes são dele."

- **Tela 2:** Segunda parte do prólogo em texto (sem espada ainda) → jogador livre para andar → borda direita avança para a Tela 3

  **Painéis de texto — Tela 2 (em frente ao portão do castelo):**
  1. "Lembro quando inaugurei este portão. O rei bateu no meu ombro e sorriu."
  2. "'Ninguém entra aqui sem minha permissão', ele disse."
  3. "Eu sorri de volta. Porque fui eu quem projetou a falha."
  4. "Esta noite eu levo tudo. O tesouro, a dignidade, a história."
  5. "— Silas atravessa o portão."

- **Tela 3:** Interior do castelo — jogador encontra a espada num pedestal no centro da tela

  **Painéis de texto — Tela 3 (interior, logo após entrar):**
  1. "Os corredores ainda cheiram a pedra úmida e tempo perdido."
  2. "Tudo exatamente como eu deixei. Cada detalhe, cada sombra."
  3. "Exceto isso."
  4. "Uma espada esquecida num pedestal de pedra. Simples. Direta."
  5. "Servirá."

  **Mecânica do pedestal:**
  - O pedestal com a espada faz parte do **background** da tela (não é um sprite separado)
  - Um `rect` invisível posicionado sobre o pedestal detecta a colisão com o player
  - Ao colidir com o rect: aparece o prompt `[E] Pegar espada` na tela
  - Jogador pressiona `E`:
    - O **sprite do player** troca para a versão com espada
    - O **background** troca para a versão sem a espada no pedestal
    - Ataque fica desbloqueado
  - A tela só termina (borda direita ativa) após a espada ser coletada

- **Tela 4:** Corredor interno do castelo com buraco no meio do chão — tutorial de pulo e primeiro combate

  **Layout:**
  - Chão contínuo à esquerda e à direita, com um buraco exatamente no centro
  - Uma plataforma pequena flutua acima do buraco com uma **Poção de Vida** em cima (coleta opcional, recompensa pulo preciso)
  - Um **Saqueador** patrulha o lado direito do buraco
  - Cair no buraco reinicia o jogador no início da tela

  **Progressão da tela:**
  1. Jogador chega ao buraco → precisa pular para atravessar
  2. Do outro lado encontra o primeiro Saqueador → primeiro combate com a espada
  3. Borda direita só ativa após o Saqueador ser derrotado

  **Assets necessários:**
  - Background atual (buraco no meio) + versão com plataforma pequena acima do buraco (ver prompt de imagem abaixo)
- **Tela 5:** Sala interna do castelo — derrota o inimigo e coleta o Fragmento 1 da Chave Mestra 🗝️

  **Painéis de texto — Tela 5 (ao entrar na sala):**
  1. "No fundo da sala, um brilho dourado pulsa lentamente."
  2. "Eu sabia que estava aqui. Projetei este esconderijo com as minhas mãos."
  3. "Um fragmento da Chave Mestra. O rei a dividiu em três partes e as espalhei pelo castelo."
  4. "Reúna os três fragmentos... e o cofre de Aurum se abrirá."
  5. "Mas primeiro — alguém está guardando."

  **Layout:**
  - Um Saqueador guarda a sala
  - O pedestal com o Fragmento 1 está visível ao fundo, mas só pode ser coletado após derrotar o inimigo

  **Mecânica do pedestal (igual à espada):**
  - Pedestal faz parte do background
  - `rect` invisível sobre o pedestal detecta colisão com o player
  - Prompt `[E] Pegar fragmento` aparece ao colidir
  - Ao pressionar `E`: fragmento coletado, background troca para versão sem o fragmento no pedestal

  **Fragmento como sprite animado (separado do background):**
  - O fragmento da chave é um sprite independente posicionado sobre o pedestal
  - **Oscilação vertical:** usa `math.sin(tempo)` para subir e descer suavemente (~4px de amplitude)
  - **Brilho oscilante:** um `pygame.Surface` com alpha desenhado em círculos concêntricos atrás do sprite; o alpha do brilho oscila junto com `math.sin(tempo)` entre transparente e visível
  - Este sistema de animação será o padrão para todos os fragmentos das fases 2 e 3

---

## 3. Fase 2 — As Catacumbas de Ferro

> Subsolo escuro do castelo, pedra bruta e grades.
> Dificuldade: Média. Espinhos no cenário, escalada.

- **Tela 1:** Entrada das Catacumbas — sala baixa de masmorra com uma armadilha de espinhos desativável

  **Ideia central:**
  - A tela apresenta as armadilhas da Fase 2 sem misturar inimigos no mesmo tutorial.
  - O ambiente deve parecer uma antiga ala de manutenção das masmorras: pedra escura, grades, ferrugem e um mecanismo lateral.
  - Há uma armadilha de espinhos no caminho principal.
  - Silas reconhece a armadilha como uma das que ele mesmo projetou para o Rei Aurum.
  - O jogador pode desativar a armadilha aproximando-se do mecanismo e pressionando `E`.

  **Painéis de texto — Tela 1 (primeira sala das catacumbas):**
  1. "As catacumbas ainda respiram como uma máquina velha."
  2. "Pedra úmida, ferro oxidado... e dentes sob o piso."
  3. "Eu conheço esta armadilha. Desenhei cada espinho dela."
  4. "Aurum manteve meu trabalho, mas nunca entendeu minhas travas de segurança."
  5. "Se eu chegar perto do mecanismo, um toque em E basta para calar esses dentes."

  **Layout:**
  - Chão contínuo em estilo masmorra.
  - Uma faixa de espinhos ocupa parte do caminho, idealmente no centro ou pouco antes da saída.
  - Um mecanismo/alavanca fica próximo da armadilha, em uma parede ou coluna lateral.
  - Não há inimigos nesta tela; o foco é ensinar leitura de armadilha e interação.

  **Mecânica da armadilha de espinhos:**
  - Enquanto ativa, a armadilha causa **20 de dano** sempre que o player tocar ou atravessar os espinhos.
  - O dano deve respeitar a mesma invencibilidade temporária usada no dano por inimigos, para evitar dezenas de danos em um único segundo.
  - Ao chegar perto do mecanismo, aparece o prompt `[E] Desativar armadilha`.
  - Ao pressionar `E`, a armadilha muda para estado desativado:
    - para de causar dano;
    - visualmente deve parecer recolhida, travada ou apagada;
    - a tela pode ser atravessada com segurança.
  - A borda direita pode encerrar a tela depois que o jogador cruzar a sala; a desativação não precisa ser obrigatória se o jogador aceitar o risco, mas deve ser o caminho recomendado pelo texto.

- **Tela 2:** Galeria das Correntes — corredor plano com duas patrulhas

  **Ideia central:**
  - Depois de reconhecer e superar a armadilha da Tela 1, Silas atravessa uma galeria simples das catacumbas.
  - A tela não tem plataformas elevadas, buracos, espinhos ou itens.
  - O foco é combate direto em chão plano contra dois Saqueadores.
  - O ambiente deve ser uma sala/corredor de masmorra cheio de grades, correntes, portas de cela e tochas, mantendo a mesma altura de plataforma da Tela 1.

  **Painéis de texto — Tela 2 (galeria das correntes):**
  1. "Dois inimigos?"
  2. "Essa deve ser a última câmara antes da segunda chave."

  **Layout:**
  - Plataforma/chão liso e contínuo, na mesma altura da Tela 1 da Fase 2.
  - Fundo com muitas grades, portas de cela, correntes penduradas, pedra úmida, musgo e tochas.
  - Dois Saqueadores posicionados no caminho principal, separados por distância suficiente para o jogador lidar com um por vez se avançar com cuidado.
  - Sem poção, sem fragmento, sem espinhos e sem mecânica extra.

  **Progressão da tela:**
  1. Jogador entra e vê os dois diálogos curtos.
  2. Enfrenta os dois Saqueadores no corredor.
  3. Borda direita só ativa após os dois inimigos serem derrotados.

- **Tela 3:** Câmara do Segundo Fragmento — sala de guarda com pedestal

  **Ideia central:**
  - A tela fecha a Fase 2 com o segundo fragmento da Chave Mestra.
  - O fragmento fica em um pedestal protegido por uma composição simples: posicionamento, espinhos e um Saqueador.
  - Silas entende que o rei não apenas espalhou os fragmentos, mas também reaproveitou os mecanismos dele para esconder as partes da chave.

  **Painéis de texto — Tela 3 (câmara do fragmento):**
  1. "Lá está. O segundo fragmento."
  2. "Aurum o trancou no lugar onde eu guardava os projetos das masmorras."
  3. "Irônico. Ele escondeu minha chave dentro da minha própria engenharia."
  4. "Dois fragmentos unidos já bastam para acordar os mecanismos do cofre."
  5. "Mas ainda falta o coração da máquina."

  **Layout:**
  - Sala mais fechada, com pedestal ao fundo ou no centro.
  - Um Saqueador guarda a câmara.
  - Uma pequena faixa de espinhos pode proteger o acesso direto ao pedestal, preferencialmente com caminho alternativo por plataforma.
  - O Fragmento 2 usa o mesmo padrão visual do Fragmento 1: sprite separado, oscilação vertical e brilho pulsante.

  **Mecânica do Fragmento 2:**
  - Prompt `[E] Pegar fragmento` aparece quando o jogador estiver próximo do pedestal.
  - O fragmento só pode ser coletado após o desafio principal da tela estar resolvido, preferencialmente após derrotar o Saqueador.
  - A fase só termina quando o Fragmento 2 for coletado.

---

## 4. Fase 3 — A Linha de Montagem de Ouro

> Coração mecânico da fortaleza, engrenagens de latão, plataformas móveis.
> Dificuldade: Difícil. Timing é essencial.

- **Tela 1:** A definir
- **Tela 2:** A definir
- **Tela 3:** A definir — contém o **Fragmento 3 da Chave Mestra** 🗝️ + **Gema de Atributo**

---

## 5. Fase 4 — O Cofre de Aurum

> Sala monumental com montanhas de moedas de ouro. Sem plataformas altas.
> Dificuldade: Extrema. Apenas o boss.

- **Tela única:** Arena do Colosso Mecânico
  - Boss se move tentando esmagar o jogador com marreta
  - Ponto fraco visível (engrenagem exposta)
  - Jogador precisa desviar e golpear o ponto fraco
  - Com a Gema coletada na Fase 3: dano dobrado, luta mais rápida

---

## Mecânica de Transição entre Telas

- O jogador avança de tela ao **chegar na borda direita** da tela
- No código: `terminou()` retorna `True` quando `player.rect.right >= LARGURA_TELA`
- O `Game` detecta isso e instancia a próxima tela da `SEQUENCIA_LEVELS`

---

## Telas Especiais

- **Game Over:** Exibida quando `player.vida <= 0` em qualquer fase
- **Tela de Vitória:** Exibida após o boss ser derrotado

---

## Itens Confirmados

| Item | Efeito |
|------|--------|
| Espada inicial | Dano padrão; mata saqueador com 1 golpe, autômato com 3 |
| Gema de Atributo | Dobra o dano da espada; efeito visual brilhante na espada |
| Poção de Vida | Recupera 1 coração no HUD |
| Fragmento da Chave | 1 por fase (fases 1–3); necessário para avançar de fase |
| Chave Mestra | Formada com os 3 fragmentos; abre a Fase 4 |

---

## Inimigos Confirmados

| Inimigo | Fases | Comportamento | Vida |
|---------|-------|---------------|------|
| Saqueador | 1 e 2 | Patrulha a plataforma (vai e volta) | 1 golpe |
| Autômato | 3 | Patrulha mais devagar, mais resistente | 3 golpes (ou menos com Gema) |
| Colosso Mecânico | 4 | Boss — marreta, ponto fraco exposto | Alta |
