import pygame

import config
import fases

class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
        pygame.display.set_caption("Geometria Ninja")
        self.clock = pygame.time.Clock()
        self.jogando = True
        self.estado = "MENU"
        self.menu = fases.FaseMenu()
        self.fase = None

    def rodar(self):
        while self.jogando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.jogando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if self.estado == "MENU":
                        fase_num = self.menu.processar_input(pygame.mouse.get_pos())
                        if fase_num == 1:
                            self.fase = fases.Fase1()
                            self.estado = "JOGANDO"
                    elif self.estado == "JOGANDO":
                        self.fase.processar_input(pygame.mouse.get_pos())

            if self.estado == "MENU":
                self.menu.atualizar()
                self.menu.desenhar(self.tela)
            elif self.estado == "JOGANDO":
                self.fase.atualizar()
                self.fase.desenhar(self.tela)

            pygame.display.flip()
            self.clock.tick(config.FPS)

        pygame.quit()

if __name__ == "__main__":
    Jogo().rodar()
