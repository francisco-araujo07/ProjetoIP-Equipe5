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
 
 
# pocao: restaura vida
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
 
 
# fragmento de chave: soma 1 em player.fragmentos_chave
class FragmentoChave(Coletavel):
    """Incrementa player.fragmentos_chave em 1."""
 
    def __init__(self, x, y):
        super().__init__(x, y, largura=28, altura=28)
 
    def _aplicar_efeito(self, player):
        player.fragmentos_chave += 1
 
 
# gema: da player.tem_gema = True e dobra o dano
class Gema(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, largura=32, altura=32)
 
    def _desenhar(self):
        imagem = pygame.image.load("assets/coletavel/gema.png").convert_alpha()
        w, h = self.image.get_size()
        imagem = pygame.transform.smoothscale(imagem, (w, h))
        self.image.blit(imagem, (0, 0))
 
    def _aplicar_efeito(self, player):
        if not player.tem_gema:   # evita dobrar o dano duas vezes se recarregar a tela
            player.dano *= 2
        player.tem_gema = True