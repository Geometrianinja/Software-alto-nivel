import pygame

import config
import Estados.GameStateManager as GSM

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
        pygame.display.set_caption("Shaolin Shapes")
        self.clock = pygame.time.Clock()
        self.jogando = True
        self.manager = GSM.Gerenciador()
        

    def rodar(self):
        while self.jogando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.jogando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.manager.esta_em_fase():
                        pos = pygame.mouse.get_pos()
                        self.manager.estado_atual.processar_input(pos)
                    else:
                        self.manager.seleciona_estado()


            self.manager.atualizar()
            self.manager.desenhar(self.tela)

            pygame.display.flip()
            self.clock.tick(config.FPS)

        pygame.quit()

if __name__ == "__main__":
    Jogo().rodar()
