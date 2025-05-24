import pygame
from os.path import join
import os

import config
import Fases.fases as fases

class MenuBase():
    def __init__(self, estado_name, opcoes, background_path = None, usa_imagens = False, botoes_posicoes = None, botao_largura = 200, botao_altura = 80):
        self.estado_name = estado_name
        self.opcoes = opcoes
        self.usa_imagens = usa_imagens
        
        self.surf = {}
        self.rect = {}
        
        self.background_path = background_path
        self.font = pygame.font.Font("PressStart2P.ttf", 24)
        
        self.botoes_posicoes = botoes_posicoes
        self.botao_largura = botao_largura
        self.botao_altura = botao_altura
        
        self.gera_imagens()
        
    def gera_imagens(self):
        if self.background_path:
            # Carrega e redimensiona a imagem para o tamanho da tela
            imagem = pygame.image.load(self.background_path).convert_alpha()
            imagem = pygame.transform.scale(imagem, (config.LARGURA, config.ALTURA))
            self.surf["Background"] = imagem
            self.rect["Background"] = self.surf["Background"].get_rect(topleft=(0, 0))

        for i, (nome, estado) in enumerate(self.opcoes):
            if self.usa_imagens and nome.startswith("Fase "):
                
                numero = nome.replace("Fase ", "")
                imagem_path = join('images', f'IconeFase{numero}.png')
                if os.path.exists(imagem_path):
                    imagem_original = pygame.image.load(imagem_path).convert_alpha()
                    novo_tamanho = (self.botao_largura, self.botao_altura)
                    self.surf[nome] = pygame.transform.smoothscale(imagem_original, novo_tamanho)
                    x, y = self.botoes_posicoes[i]
                    self.rect[nome] = self.surf[nome].get_rect(topleft=(x, y))
                else:
                    # Fallback para texto se a imagem não existir
                    cor = config.CORES["branco"]
                    self.surf[nome] = self.font.render(nome, True, cor)
                    x, y = self.botoes_posicoes[i]
                    self.rect[nome] = self.surf[nome].get_rect(topleft=(x, y))
            elif self.usa_imagens:
                # Usa o padrão Nome_button.png para outros botões
                imagem_path = join('images', f'{nome}_button.png')
                if os.path.exists(imagem_path):
                    imagem_original = pygame.image.load(imagem_path).convert_alpha()
                    novo_tamanho = (self.botao_largura, self.botao_altura)
                    self.surf[nome] = pygame.transform.smoothscale(imagem_original, novo_tamanho)
                    self.rect[nome] = self.surf[nome].get_rect(center=(config.LARGURA / 2, config.ALTURA / 2 + i * 100))
                else:
                    cor = config.CORES["branco"]
                    self.surf[nome] = self.font.render(nome, True, cor)
                    self.rect[nome] = self.surf[nome].get_rect(topleft=(config.LARGURA // 2 - 100, 150 + i * 60))
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
        background = join('images', 'FlorestaInicio.png')
        super().__init__("MENU", opcoes, background, usa_imagens=True)

class Fases(MenuBase):
    """
    Menu de Fases.
    
    Menu responsável por informar quais fases o jogador por escolher.
    """
    def __init__(self):
        opcoes = [
            ["Fase 0", "INTRO0"],
            ["Fase 1", "INTRO1"],
            ["Fase 2", "FASE02"],
            ["Fase 3", "FASE03"],
            ["Fase 4", "FASE04"],
            ["Fase 5", "FASE05"],
            ["Fase 6", "FASE06"],
            ["Fase 7", "FASE07"],
        ]
        botoes_posicoes = [
            (400, 100),
            (150, 220),
            (170, 380),
            (630, 390),
            (400, 350),
            (660, 210),
            (560, 10),
            (730, 455),
        ]
        background = join('images', 'MenuSemfases.png')
        super().__init__("FASES", opcoes, background, usa_imagens=True, botoes_posicoes=botoes_posicoes, botao_largura=120, botao_altura=48)

    
