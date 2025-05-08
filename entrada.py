import pygame
from typing import List, Tuple, Union

class InputType:
    MOUSE_CLICK = 0

def get_input() -> List[Tuple[int, Union[Tuple[int, int], str]]]:
    entradas = []
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            entradas.append((InputType.MOUSE_CLICK, "QUIT"))
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            entradas.append((InputType.MOUSE_CLICK, pygame.mouse.get_pos()))
    return entradas

class InputManager:
    def __init__(self):
        self.entradas = []

    def update(self):
        self.entradas = get_input()

    def get_entradas(self):
        return self.entradas
