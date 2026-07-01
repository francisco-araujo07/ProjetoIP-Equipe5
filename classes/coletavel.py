import pygame
import settings
 
 
class Coletavel(pygame.sprite.Sprite):
    
 
    def __init__(self, x, y, largura=28, altura=28):
        super().__init__()
        self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        self._desenhar()
 
    def _desenhar(self):
        """Subclasses sobrescreva para definir a aparência."""
        pass
 
    def coletar(self, player):
        """Aplica o efeito no player e remove o sprite do mundo."""
        self._aplicar_efeito(player)
        self.kill()
 
    def _aplicar_efeito(self, player):
        """Subclasses sobrescreva para definir o efeito ao ser coletado."""
        pass
 
 
# ---------------------------------------------------------------------------
# Poção — restaura vida
# ---------------------------------------------------------------------------
 
class Pocao(Coletavel):
    """Restaura vida ao player sem ultrapassar vida máxima."""
 
    def __init__(self, x, y, cura=settings.POCAO_CURA):
        self.cura = cura
        super().__init__(x, y, largura=48, altura=60)

    def _desenhar(self):
        imagem = pygame.image.load("assets/coletavel/pocao.png").convert_alpha()
        w, h = self.image.get_size()
        imagem = pygame.transform.smoothscale(imagem, (w, h))
        self.image.blit(imagem, (0, 0))


    def _aplicar_efeito(self, player):
        player.pocoes += 1
 
 
# ---------------------------------------------------------------------------
# Fragmento de Chave — acumula em player.fragmentos_chave (int)
# ---------------------------------------------------------------------------
 
class FragmentoChave(Coletavel):
    """Incrementa player.fragmentos_chave em 1."""
 
    def __init__(self, x, y):
        super().__init__(x, y, largura=28, altura=28)
 
    def _desenhar(self):
        w, h = self.image.get_size()
        cx, cy = w // 2, h // 2
        # Cabo (círculo dourado)
        pygame.draw.circle(self.image, (220, 170, 0), (cx - 4, cy - 3), 8)
        pygame.draw.circle(self.image, (255, 210, 60), (cx - 4, cy - 3), 8, 2)
        pygame.draw.circle(self.image, (255, 240, 160), (cx - 7, cy - 6), 3)  # brilho
        # Haste
        pygame.draw.rect(self.image, (220, 170, 0), (cx, cy - 2, 10, 4))
        # Dentes
        pygame.draw.rect(self.image, (220, 170, 0), (cx + 6, cy + 2, 3, 4))
        pygame.draw.rect(self.image, (220, 170, 0), (cx + 2, cy + 2, 3, 3))
 
    def _aplicar_efeito(self, player):
        player.fragmentos_chave += 1
 
 
# ---------------------------------------------------------------------------
# Gema — marca player.tem_gema = True
# ---------------------------------------------------------------------------
 
class Gema(Coletavel):
    """Concede a gema ao player (player.tem_gema = True)."""
 
    PALETAS = {
        "azul":     ((50, 100, 255),  (160, 200, 255)),
        "vermelha": ((210, 30,  30),  (255, 140, 140)),
        "verde":    ((30, 160,  50),  (140, 255, 170)),
        "amarela":  ((220, 190, 10),  (255, 235, 120)),
    }
 
    def __init__(self, x, y, cor="azul"):
        self.cor = cor
        super().__init__(x, y, largura=24, altura=24)
 
    def _desenhar(self):
        w, h = self.image.get_size()
        cx, cy = w // 2, h // 2
        base, brilho = self.PALETAS.get(self.cor, self.PALETAS["azul"])
 
        # Forma de diamante
        pontos = [(cx, 2), (w - 2, cy), (cx, h - 2), (2, cy)]
        pygame.draw.polygon(self.image, base, pontos)
        pygame.draw.polygon(self.image, brilho, pontos, 2)
 
        # Faceta interna (brilho)
        faceta = [(cx, 5), (cx + 5, cy - 2), (cx, cy - 1), (cx - 5, cy - 2)]
        pygame.draw.polygon(self.image, brilho, faceta)
 
    def _aplicar_efeito(self, player):
        if not player.tem_gema:   # evita dobrar o dano duas vezes se recarregar a tela
            player.dano *= 2
        player.tem_gema = True