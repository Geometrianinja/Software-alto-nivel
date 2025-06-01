import pygame

import config
import Estados.GameStateManager as GSM

import serial
import struct
import asyncio
import threading
import time
import os
import sys
import win32api

from entrada import InputManager
from Eletronica import receiver


class Jogo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
        pygame.display.set_caption("Shaolin Shapes")
        self.clock = pygame.time.Clock()
        self.jogando = True
        self.manager = GSM.Gerenciador()
        self.input_manager = InputManager()

    def rodar(self):
        while self.jogando:
            self.input_manager.update()
            
            if self.manager.atualizar(self.input_manager):
                self.jogando = False
            self.manager.desenhar(self.tela, self.input_manager)

            pygame.display.flip()
            self.clock.tick(config.FPS)

        pygame.quit()

def main():
    Jogo().rodar()

if __name__ == "__main__":
    main()
