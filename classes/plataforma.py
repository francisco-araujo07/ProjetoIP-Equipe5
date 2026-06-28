import pygame

class Plataforma(pygame.sprite.Sprite):

    # Representa uma plataforma sólida.
    def __init__(self, x, y, largura, altura, caminho_imagem=None):

        super().__init__()

        # self.image é o visual do sprite.
        # Se caminho_imagem for None, a plataforma fica invisível (só colisão).
        if caminho_imagem:
            self.image = pygame.image.load(caminho_imagem).convert_alpha()
            self.image = pygame.transform.scale(self.image, (largura, altura))  # Redimensiona para o tamanho da plataforma
        else:
            self.image = pygame.Surface((largura, altura), pygame.SRCALPHA)  # Superfície transparente

        # self.rect define a posição e o tamanho do sprite no mundo.
        # get_rect() pega o retângulo da imagem
        # topleft=(x, y) já posiciona esse retângulo no lugar certo.
        self.rect = self.image.get_rect(topleft=(x, y))

def resolver_colisao_chao(player, grupo_plataformas):

    # spritecollide() retorna uma lista com todos os sprites do grupo que estão colidindo com o player nesse momento.
    # O terceiro argumento (False) significa: não destruir as plataformas ao colidir.
    colisoes = pygame.sprite.spritecollide(player, grupo_plataformas, False)

    if colisoes:

        for plat in colisoes:

            # Caso o jogagador esteja caindo
            if player.velocidade_y > 0:

                # Gruda o pé do Player no topo do chão
                player.rect.bottom = plat.rect.top

                # Faz ele parar de cair
                player.velocidade_y = 0

                # Marca que o Player está no chão, liberando ele pular novamente
                player.no_chao = True
    else:
        # Se não há colisão, o player está no ar.
        player.no_chao = False