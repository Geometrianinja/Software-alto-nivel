import pygame
from os.path import join, exists


import config
import Fases.fases_antigo as fases_antigo

class MenuBase():
    def __init__(self, estado_name, opcoes, input_manager, background_path = None, botoes_posicoes = None, botao_largura = 200, botao_altura = 80):
        self.estado_name = estado_name
        self.opcoes = opcoes
        self.input_manager = input_manager

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
            if nome.startswith("Fase "):
                
                numero = nome.replace("Fase ", "")
                imagem_path = join('images', f'IconeFase{numero}.png')
            else:
                # Usa o padrão Nome_button.png para outros botões
                imagem_path = join('images', f'{nome}_button.png')
                
            if exists(imagem_path):
                imagem_original = pygame.image.load(imagem_path).convert_alpha()
                novo_tamanho = (self.botao_largura, self.botao_altura)
                self.surf[nome] = pygame.transform.smoothscale(imagem_original, novo_tamanho)
            else:
                cor = config.Cores.BRANCO
                self.surf[nome] = self.font.render(nome, True, cor)
                
            x, y = self.botoes_posicoes[i]
            self.rect[nome] = self.surf[nome].get_rect(center=(x, y))


    def atualizar(self):
        """Atualiza o estado atual do jogo.
        
        Realiza a verificação se algum botão de mudança de estado foi precionado.
        
        Returns:
            String: Se o jogador deseja mudar de estado, ele retorna o futuro estado, caso contrário, ele retorna o próprio estado
        """
        
        
        
        for (nome, estado) in self.opcoes:
            if self.input_manager.mouse_left_just_pressed and self.rect[nome].collidepoint(self.input_manager.mouse_pos):
                return estado
        
        return self.estado_name
    
    def desenhar(self, tela):
        """Desenha os objetos na tela.
        
        Args:
            tela (pygame.Surface): Superfície onde o estado será desenhado.
        """
        if "Background" in self.surf:
            tela.blit(self.surf["Background"], self.rect["Background"])

        for (nome, estado) in self.opcoes:
            tela.blit(self.surf[nome], self.rect[nome])
        
    
class MenuPrincipal(MenuBase):
    """
    Representa o menu principal do jogo.
    Exibe as opções iniciais como 'Jogar' e 'Configuração', e lida com a entrada
    do jogador para selecionar uma dessas opções.
    """
    """def __init__(self, input_manager):
        opcoes = [["Jogar", "FASES"], ["Configuracao", "CONFIG"]]
        botoes_posicoes = [
            (config.LARGURA / 2, config.ALTURA / 2 - 50),
            (config.LARGURA / 2, config.ALTURA / 2 + 50),
        ]
        background = join('images', 'FlorestaInicio.png')
        super().__init__("MENU", opcoes, input_manager, background, botoes_posicoes=botoes_posicoes, botao_largura=200, botao_altura=80)"""
    def __init__(self, input_manager):
        opcoes = [["Jogar", "FASES"]]
        botoes_posicoes = [
            (config.LARGURA / 2, config.ALTURA / 2 - 50),
        ]
        background = join('images', 'FlorestaInicio.png')
        super().__init__("MENU", opcoes, input_manager, background, botoes_posicoes=botoes_posicoes, botao_largura=200, botao_altura=80)
                

class Fases(MenuBase):
    """
    Menu de Fases.
    
    Menu responsável por informar quais fases o jogador por escolher.
    """
    def __init__(self, input_manager):
        opcoes = [
            ["Fase 0", "INTRO0"],
            ["Fase 1", "INTRO1"],
            ["Fase 2", "FASE02"],
            ["Fase 3", "FASE03"],
            ["Fase 4", "FASE04"],
            ["Fase 5", "FASE05"],
            ["Fase 6", "ENTREETAPAS06_E0"],
            ["Fase 7", "FASE07"],
        ]
        botoes_posicoes = [
            (460, 124),
            (210, 244),
            (230, 404),
            (690, 414),
            (460, 374),
            (720, 234),
            (620, 34),
            (790, 479),
        ]
        botoes_posicoes = [(x * config.LARGURA / 1000, y * config.ALTURA / 500) for x, y in botoes_posicoes]
        background = join('images', 'MenuSemfases.png')
        super().__init__("FASES", opcoes, input_manager, background, botoes_posicoes=botoes_posicoes, botao_largura=120, botao_altura=48)