import pygame
import config
import Fases.fases as fases
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
            "FASE00" : fases.Fase00(config.LARGURA, config.ALTURA),
            "MENU"   : menu.Menu_principal(), 
            "CONFIG" : menu_config.Configuracao(),
            "FASES"  : menu.Fases(),
            "FASE01" : fases.Fase01(config.LARGURA, config.ALTURA),
            "FASE02" : fases.Fase02(config.LARGURA, config.ALTURA),


            }
        
        self.estado_atual = self.estados["MENU"]  # Estado inicial

    def esta_em_fase(self):
        
        return hasattr(self.estado_atual, 'impactar_forma') # detecta se estado atual é uma fase
    
   
    def mudar_estado(self, novo_estado):
        self.estado_atual = self.estados[novo_estado]
        
    def seleciona_estado(self):
        estado = self.estado_atual.processar_input(pygame.mouse.get_pos())
        if(estado != self.estado_atual):
            self.mudar_estado(estado)
    
    
    def atualizar(self, input_manager):
        self.estado_atual = self.estados[self.estado_atual.atualizar(input_manager)]
    
    def desenhar(self, tela):
        self.estado_atual.desenhar(tela)
        
    
    
    