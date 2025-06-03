# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 19:09:52 2025

@author: artur
"""
import pygame
        
def desenhar_cursor(input_manager, tela):
    if input_manager.using_controller and input_manager.cont_screen_pos:
        """print(f"Controller position: {input_manager.cont_screen_pos}")"""
        pygame.draw.circle(
            tela,
            (255, 0, 0),
            input_manager.cont_screen_pos,
            10
        )
    else:
        pygame.draw.circle(
            tela,
            (255, 0, 0),
            input_manager.mouse_pos,
            10
        )