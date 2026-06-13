import settings

class Level:
    def __init__(self):
        pass

    def atualizar(self):
        pass 

    def desenhar(self, tela):
        tela.fill(settings.BLUE)  # Limpa a tela com preto

    def terminou(self):
        return False 