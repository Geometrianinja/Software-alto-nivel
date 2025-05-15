# -*- coding: utf-8 -*-
"""
Created on Thu May 15 11:16:56 2025

@author: artur
"""
import pygame as pg

pg.init()
tela = pg.display.set_mode((600, 400))

running = True
while(running):
    for event in pg.event.get():
        print(event)
            
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                
    pg.display.flip()
    
pg.quit()