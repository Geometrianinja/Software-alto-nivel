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
        self.tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
        pygame.display.set_caption("Shaolin Shapes")
        self.clock = pygame.time.Clock()
        self.jogando = True
        self.input_manager = InputManager()
        self.manager = GSM.Gerenciador(self.input_manager)
        self.cursor = Cursor(14, self.input_manager, [(255, 255, 255), (255,100, 100)], self.tela )

    def rodar(self):
        while self.jogando:
            self.input_manager.update()
            
            if self.manager.atualizar(self.input_manager):
                self.jogando = False
            self.manager.desenhar(self.tela)
            self.cursor.draw()

            pygame.display.flip()
            self.clock.tick(config.FPS)

        pygame.quit()
    

def main():
    Jogo().rodar()

if __name__ == "__main__":
    #cProfile.run('main()', 'profile_output.prof')
    main()
