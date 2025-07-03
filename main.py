import pygame

import config
import Estados.GameStateManager as GSM

from entrada import InputManager
from Eletronica import receiver
from cursor import Cursor
from pygame import Vector2

import cProfile

class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        if config.LARGURA == 0 or config.ALTURA == 0:
            self.tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
            config.LARGURA, config.ALTURA = self.tela.get_size()
        else:
            self.tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
        config.UN = config.LARGURA / 1000
        pygame.display.set_caption("Shaolin Shapes")
        self.clock = pygame.time.Clock()
        self.jogando = True
        self.input_manager = InputManager()
        self.manager = GSM.Gerenciador(self.input_manager)
        self.cursor = Cursor(14, self.input_manager, [(255, 255, 255), (255, 100, 100)], self.tela)

    def rodar(self):
        while self.jogando:
            self.input_manager.update()
            
            if self.manager.atualizar(self.input_manager):
                self.jogando = False
            self.manager.desenhar(self.tela)
            self.cursor.draw()

            self.clock.tick(config.FPS)

            pygame.display.flip()

        pygame.quit()
    

def main():
    Jogo().rodar()

if __name__ == "__main__":
    #cProfile.run('main()', 'profile_output.prof')
    main()
