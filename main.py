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
    def __init__(self, controller):
        pygame.init()
        self.tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
        pygame.display.set_caption("Shaolin Shapes")
        self.clock = pygame.time.Clock()
        self.jogando = True
        self.manager = GSM.Gerenciador()
        self.input_manager = InputManager()
        self.controller = controller
        

    def rodar(self):
        while self.jogando:
            self.input_manager.update()
            
            if self.manager.atualizar(self.input_manager):
                self.jogando = False
            self.manager.desenhar(self.tela)

            pygame.display.flip()
            self.clock.tick(config.FPS)

        pygame.quit()

def main():
    controller = receiver.Controller()
    """while(not controller.connect()):
        print("Trying to connect...")
        time.sleep(0.5)
        pass
    ble_thread = threading.Thread(target=controller.run)
    ble_thread.start()"""
    Jogo(controller).rodar()
    #controller.stop()

if __name__ == "__main__":
    main()
