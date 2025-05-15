import pygame
from os.path import join

import config
import Fases.fases as fases
        
    
class Menu_principal():
    """
    Representa o menu principal do jogo.
    
    Exibe as opções iniciais como 'Jogar' e 'Configuração', e lida com a entrada
    do jogador para selecionar uma dessas opções.
    """
    
    def __init__(self):
        self.opcoes = [["Jogar", "FASES"], ["Configuracao", "CONFIG"]]
        self.estado_name = "MENU"
        self.surf = {}
        self.rect = {}
        self.imagens()
        
    def imagens(self):
        
        self.surf["Background"] = pygame.image.load(join('images', 'dojo01.gif')).convert_alpha()
        self.rect["Background"] = self.surf["Background"].get_rect(center = (config.LARGURA / 2, config.ALTURA / 2))
        
        imagem_original = pygame.image.load(join('images', 'Jogar_button.png')).convert_alpha()
        novo_tamanho = (200, 80)
        self.surf["Jogar"] = pygame.transform.smoothscale(imagem_original, novo_tamanho) 
        self.rect["Jogar"] = self.surf["Jogar"].get_rect(center = (config.LARGURA / 2, config.ALTURA / 2))
        
    def atualizar(self, input_manager):
        for button in self.opcoes:
            if input_manager.mouse_left_just_pressed and self.rect[button[0]].collidepoint(input_manager.mouse_pos):
                return button[1]
        
        return self.estado_name
    
    def desenhar(self, tela):
        tela.blit(self.surf["Background"], self.rect["Background"])
        tela.blit(self.surf["Jogar"], self.rect["Jogar"])

    
class Fases():
    """
    Menu de Fases.
    
    Menu responsável por informar quais fases o jogador por escolher.
    """
    def __init__(self):
        self.estado_name = "FASES"
        self.font = pygame.font.Font("PressStart2P.ttf", 24)
        self.opcoes = [["Fase 1", "FASE01"], ["Fase 2", "FASE02"], ["Fase 3", "FASE03"],
                       ["Fase 4", "FASE04"], ["Fase 5", "FASE05"]]
        self.surf = {}
        self.rect = {}

    def atualizar(self, input_manager):
        """for button in self.opcoes:
            if input_manager.mouse_left_just_pressed and self.rect[button[0]].collidepoint(input_manager.mouse_pos):
                return button[1]"""
        for i in range(len(self.opcoes)):
            y = 150 + i * 60
            if input_manager.mouse_left_just_pressed and y <= input_manager.mouse_pos[1] <= y + 40:
                    return f"FASE0{i + 1}"
        
        return self.estado_name
        

    def desenhar(self, tela):
        tela.fill((20, 20, 20))
        for i, opcao in enumerate(self.opcoes):
            cor = config.CORES["branco"]
            texto = self.font.render(opcao[0], True, cor)
            tela.blit(texto, (config.LARGURA // 2 - 100, 150 + i * 60))
