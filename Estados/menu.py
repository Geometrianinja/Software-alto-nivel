import pygame
from os.path import join

import config
import Fases.fases as fases

class MenuBase():
    def __init__(self, estado_name, opcoes, background_path = None, usa_imagens = False):
        self.estado_name = estado_name
        self.opcoes = opcoes
        self.usa_imagens = usa_imagens
        
        self.surf = {}
        self.rect = {}
        
        self.background_path = background_path
        self.font = pygame.font.Font("PressStart2P.ttf", 24)
        
        self.gera_imagens()
        
    def gera_imagens(self):
        if self.background_path:
            self.surf["Background"] = pygame.image.load(self.background_path).convert_alpha()
            self.rect["Background"] = self.surf["Background"].get_rect(center=(config.LARGURA / 2, config.ALTURA / 2))

        for i, (nome, estado) in enumerate(self.opcoes):
            if self.usa_imagens:
                imagem_path = join('images', f'{nome}_button.png')
                imagem_original = pygame.image.load(imagem_path).convert_alpha()
                novo_tamanho = (200, 80)
                self.surf[nome] = pygame.transform.smoothscale(imagem_original, novo_tamanho)
                self.rect[nome] = self.surf[nome].get_rect(center=(config.LARGURA / 2, config.ALTURA / 2 + i * 100))
            else:
                cor = config.CORES["branco"]
                self.surf[nome] = self.font.render(nome, True, cor)
                self.rect[nome] = self.surf[nome].get_rect(topleft=(config.LARGURA // 2 - 100, 150 + i * 60))

    def atualizar(self, input_manager):
        for (nome, estado) in self.opcoes:
            if input_manager.mouse_left_just_pressed and self.rect[nome].collidepoint(input_manager.mouse_pos):
                return estado
        
        return self.estado_name
    
    def desenhar(self, tela):
        if "Background" in self.surf:
            tela.blit(self.surf["Background"], self.rect["Background"])
        else:
            tela.fill((20, 20, 20))

        for (nome, estado) in self.opcoes:
            tela.blit(self.surf[nome], self.rect[nome])
        
    
class MenuPrincipal(MenuBase):
    """
    Representa o menu principal do jogo.
    
    Exibe as opções iniciais como 'Jogar' e 'Configuração', e lida com a entrada
    do jogador para selecionar uma dessas opções.
    """
    
    def __init__(self):
        opcoes = [["Jogar", "FASES"], ["Configuracao", "CONFIG"]]
        background = join('images', 'dojo01.gif')
        super().__init__("MENU", opcoes, background, usa_imagens = True)
                

class Fases(MenuBase):
    """
    Menu de Fases.
    
    Menu responsável por informar quais fases o jogador por escolher.
    """
    def __init__(self):
        opcoes = [["Fase 0", "FASE00"], ["Fase 1", "FASE01"], ["Fase 2", "FASE02"],
                  ["Fase 3", "FASE03"], ["Fase 4", "FASE04"], ["Fase 5", "FASE05"]]
        super().__init__("FASES", opcoes)