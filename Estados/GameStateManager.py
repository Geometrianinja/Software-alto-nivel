import pygame

import fases
import Estados.menu as menu
import Estados.menu_config as menu_config

class Gerenciador:
    """
    Gerenciador de estados do jogo.
    
    Esta classe é responsável por fazer a troca de estados, como por exemplo:
    sair do menu de fases para ir para a fase 01.
    
    """
    def __init__(self):
        self.estados = {
            "CONTROL": menu_config.ConfigControle(),
            "FASE00" : fases.Fase00(),
            "MENU"   : menu.Menu_principal(), 
            "CONFIG" : menu_config.Configuracao(),
            "FASES"  : menu.Fases(),
            "FASE01" : fases.Fase01()
        }
        self.estado_atual = self.estados["MENU"]
        
    def mudar_estado(self, novo_estado):
        self.estado_atual = self.estados[novo_estado]
        
    def seleciona_estado(self):
        estado = self.estado_atual.processar_input(pygame.mouse.get_pos())
        if(estado != self.estado_atual):
            self.mudar_estado(estado)
        
    def atualizar(self):
        self.estado_atual.atualizar()
    
    def desenhar(self, tela):
        self.estado_atual.desenhar(tela)
    
    