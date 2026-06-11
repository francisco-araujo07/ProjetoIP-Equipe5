# 🗂️ Guia de Git — Time de Desenvolvimento

> Consulte este guia **sempre que for realizar qualquer tarefa**. Se tiver dúvida, pergunte antes de fazer.

---

## 📌 Conceitos Essenciais

| Termo | O que é |
|---|---|
| **Repositório (repo)** | A pasta do projeto hospedada no GitHub |
| **Branch** | Uma "cópia paralela" do código para trabalhar sem afetar os outros |
| **Commit** | Um "save" do seu progresso com uma mensagem descritiva |
| **Push** | Enviar seus commits para o GitHub |
| **Pull** | Baixar as atualizações do GitHub para sua máquina |
| **Merge** | Juntar o código de duas branches |
| **Conflito** | Quando duas pessoas editaram o mesmo trecho de código |
| **Pull Request (PR)** | Pedido formal para mergear sua branch em outra |

---

## 🌿 Estrutura de Branches

```
main          → código final, estável. Só recebe merge ao fim de cada sprint.
dev           → integração. Todo mundo manda seu código pra cá.
feature/X     → sua branch de trabalho. Criada a partir de dev.
```

> ⚠️ **Nunca commite direto em `main` ou `dev`.** Sempre trabalhe em uma `feature/`.

---

## 🔁 Fluxo Completo — Passo a Passo

### 1. Configuração inicial (só uma vez)

```bash
# Clone o repositório na sua máquina
git clone https://github.com/SEU-TIME/SEU-REPO.git

# Entre na pasta do projeto
cd SEU-REPO

# Configure seu nome e email (aparece nos commits)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

---

### 2. Antes de começar qualquer tarefa

```bash
# Vá para a branch dev
git checkout dev

# Baixe as atualizações mais recentes
git pull origin dev
```

> ✅ Sempre faça isso antes de criar sua branch. Garante que você parte do código mais atual.

---

### 3. Criar sua branch de trabalho

```bash
# Crie e já entre na branch
git checkout -b feature/nome-da-sua-tarefa
```

**Exemplos de nomes:**
```bash
git checkout -b feature/player-movimento
git checkout -b feature/enemy-colisao
git checkout -b feature/hud-pontuacao
```

> Use nomes curtos, em minúsculas, com hífens. Sem espaços ou acentos.

---

### 4. Trabalhar e salvar progresso (commits)

```bash
# Ver quais arquivos você modificou
git status

# Adicionar os arquivos que quer salvar
git add nome_do_arquivo.py

# Ou adicionar TUDO de uma vez
git add .

# Criar o commit com mensagem descritiva
git commit -m "add: Player.move() com velocidade constante"
```

**Padrão de mensagens de commit:**

| Prefixo | Quando usar |
|---|---|
| `add:` | Adicionou algo novo |
| `fix:` | Corrigiu um bug |
| `update:` | Melhorou algo existente |
| `remove:` | Removeu código/arquivo |
| `style:` | Só formatação, sem mudar lógica |

**Exemplos:**
```bash
git commit -m "add: classe Enemy com movimento básico"
git commit -m "fix: Player não parava ao colidir com parede"
git commit -m "update: aumentar velocidade de pulo do Player"
```

> ❌ Evite mensagens genéricas como `"update"`, `"ajuste"`, `"teste"`.

---

### 5. Antes de enviar — atualizar com o que mudou em `dev`

```bash
# Ainda na sua feature branch, baixe o que mudou em dev
git pull origin dev
```

Se aparecer **conflito**, veja a seção [Resolvendo Conflitos](#-resolvendo-conflitos) abaixo.

---

### 6. Enviar sua branch para o GitHub

```bash
git push origin feature/nome-da-sua-tarefa
```

---

### 7. Abrir Pull Request (PR)

1. Acesse o repositório no **GitHub**
2. Clique em **"Compare & pull request"** (aparece automaticamente após o push)
3. Confirme que o PR vai de `feature/sua-branch` → `dev`
4. Escreva um título claro: _"Adiciona movimento horizontal do Player"_
5. Clique em **"Create pull request"**
6. Aguarde **alguém do time que saiba mais de Git** revisar e aprovar

> ⚠️ Não faça o merge você mesmo. Peça para quem tiver mais experiência no Git fazer isso.

---

## ⚔️ Resolvendo Conflitos

Conflito acontece quando duas pessoas editaram o mesmo trecho do mesmo arquivo.

**Como identificar:**
```bash
git pull origin dev
# Aparece: CONFLICT (content): Merge conflict in Player.py
```

**O que você verá no arquivo:**
```python
<<<<<<< HEAD
    self.velocidade = 5   # seu código
=======
    self.velocidade = 7   # código que veio de dev
>>>>>>> dev
```

**Como resolver:**
1. Abra o arquivo no editor
2. Escolha qual versão manter (ou combine as duas)
3. **Apague** as linhas `<<<<<<<`, `=======` e `>>>>>>>`
4. Salve o arquivo
5. Finalize:

```bash
git add Player.py
git commit -m "fix: resolve conflito de velocidade no Player"
```

> 💡 Dica: chame alguém do time que saiba mais se não souber qual versão manter.

---

## 📋 Comandos de Consulta (só leitura, sem risco)

```bash
# Ver em qual branch você está
git branch

# Ver histórico de commits
git log --oneline

# Ver o que mudou nos arquivos (antes de commitar)
git diff

# Ver status dos arquivos
git status
```

---

## 🚨 Situações de Emergência

### "Commitei na branch errada"
```bash
# Se ainda não fez push, desfaz o último commit (mantém as alterações)
git reset --soft HEAD~1
```

### "Estraguei tudo e quero voltar ao último commit"
```bash
# ⚠️ CUIDADO: apaga tudo que não foi commitado
git checkout -- .
```

### "Preciso trocar de branch mas tenho mudanças não commitadas"
```bash
# Guarda temporariamente suas mudanças
git stash

# Troca de branch
git checkout dev

# Quando voltar, recupera as mudanças
git stash pop
```

---

## ✅ Checklist — Antes de Qualquer Tarefa

```
[ ] Estou na branch dev?           → git checkout dev
[ ] Dev está atualizado?           → git pull origin dev
[ ] Criei minha feature branch?    → git checkout -b feature/minha-tarefa
[ ] Estou na branch certa?         → git branch
```

## ✅ Checklist — Antes de Fazer Push

```
[ ] Salvei todos os arquivos no editor?
[ ] Rodei o jogo e não tem erro óbvio?
[ ] Atualizei com dev?             → git pull origin dev
[ ] Resolvi conflitos (se houver)?
[ ] Minha mensagem de commit é descritiva?
```

---

## 📞 Quando Pedir Ajuda

Chame **alguém do time que saiba mais de Git** quando:
- Aparecer conflito e você não souber resolver
- Fizer algo errado e não souber desfazer
- Seu push for rejeitado com mensagem de erro desconhecida
- Tiver dúvida se deve mergear ou não

> 🔑 Regra de ouro: **na dúvida, não faça. Pergunte primeiro.**