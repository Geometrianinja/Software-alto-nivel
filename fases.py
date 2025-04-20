import pygame
import random

import entrada
import formas
import config
import formas
from abc import ABC

class FaseBase(ABC):
    def __init__(self):
        self.formas = [formas.Circulo(100, 100, config.CORES["rosa"])]  # Temporário para teste

    def atualizar(self):
        for forma in self.formas:
            forma.atualizar()

    def desenhar(self, tela):
        for forma in self.formas:
            forma.desenhar(tela)

    def processar_input(self, pos):
        for forma in self.formas:
            if not forma.impactada and forma.foi_clicado(pos):
                forma.impactada = True

class Fase00(FaseBase):
    """
    Fase de tutorial para o jogo
    
    Nesta fase o jogador será introduzido para o mundo do jogo, onde ele
    aprenderá a cortar os elementos, e afins.
    """
    def __init__(self):
        self.fundo = pygame.image.load("fundo.gif").convert()
        self.fundo = pygame.transform.scale(self.fundo, (config.LARGURA, config.ALTURA))

        self.clock = pygame.time.Clock()
        self.controlador = formas.ControlaFormas( qtd_circulos=2,
                                                  qtd_quadrados=2,
                                                  qtd_triangulos=2,
                                                  limite_max_formas=12)

        self.tempo_spawn = 0
        self.intervalo_spawn = 240
        self.jogando = True

        self.fontecontador = pygame.font.Font("PressStart2P.ttf", 16)
        self.fontetitulo = pygame.font.Font("PressStart2P.ttf", 32)
        self.contador_titulo = 0
        self.titulo_visivel = True
        self.intervalo_titulo = 30
        
        self.input_manager = entrada.InputManager()
        
    def desenhar(self, tela):
        self.rodar(tela)
        
    def desenhar_contador(self, tela):
        y = 40
        for tipo, valor in self.controlador.contador_cortes.items():

            texto = self.fontecontador.render (f" {tipo.capitalize()}: {valor}", True,  (255, 105, 180))  
            tela.blit(texto, (40, y))
            y += 25
            
    def desenhar_titulo(self, tela):
        
        self.contador_titulo += 1
        if self.contador_titulo >= self.intervalo_titulo:
            self.titulo_visivel = not self.titulo_visivel
            self.contador_titulo = 0

        '''
        Renderiza o texto 3 vezes com deslocamentos diferentes para criar o efeito
        '''
        texto_base = self.fontetitulo.render("SHAOLIN SHAPES", True, (255, 255, 255))
        texto_tremido1 = self.fontetitulo.render("SHAOLIN SHAPES", True, (218, 112, 214))
        texto_tremido2 = self.fontetitulo.render("SHAOLIN SHAPES", True, (216, 191, 216))

        x = config.LARGURA // 2
        y = 40

        base_rect = texto_base.get_rect(center=(x, y))

        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)

        tela.blit(texto_tremido2, base_rect.move(offset_x - 2, offset_y))
        tela.blit(texto_tremido1, base_rect.move(offset_x + 2, offset_y))
        tela.blit(texto_base, texto_base.get_rect(center=(x, y)))
        
    def atualizar(self):
        pass
        
    def rodar(self, tela):
        tela.blit(self.fundo, (0, 0))
        #self.input_manager.update()

        for tipo, valor in self.input_manager.get_entradas():
            if tipo == entrada.InputType.MOUSE_CLICK:
                if valor == "QUIT":
                    self.jogando = False
                else:
                    self.controlador.impactar_forma(valor)

        self.controlador.atualizar_formas()
        self.controlador.desenhar_formas(tela)
        self.desenhar_contador(tela)
        self.desenhar_titulo(tela)

        pygame.display.flip()
            
        



class Fase01(FaseBase):
    def __init__(self):
        self.input = entrada.InputManager()
        self.controlador = formas.ControlaFormas(qtd_circulos=2, qtd_quadrados=2, qtd_triangulos=2, limite_max_formas=10)

    def atualizar(self):
        self.input.update()
        for tipo, dado in self.input.get_entradas():
            if tipo == 0 and dado != "QUIT":
                self.controlador.impactar_forma(dado)
        self.controlador.atualizar_formas()

    def desenhar(self, tela):
        tela.fill((0, 0, 0))
        self.controlador.desenhar_formas(tela)

    def processar_input(self, pos):
        self.controlador.impactar_forma(pos)
        
        return "FASE01"
            
            
class FasesMenu:
    def __init__(self):
        self.font = pygame.font.Font("PressStart2P.ttf", 24)
        self.opcoes = ["Fase 1", "Fase 2", "Fase 3", "Fase 4", "Fase 5"]

    def atualizar(self):
        pass

    def desenhar(self, tela):
        tela.fill((20, 20, 20))
        for i, opcao in enumerate(self.opcoes):
            cor = config.CORES["branco"]
            texto = self.font.render(opcao, True, cor)
            tela.blit(texto, (config.LARGURA // 2 - 100, 150 + i * 60))

    def processar_input(self, pos):
        for i in range(len(self.opcoes)):
            y = 150 + i * 60
            if y <= pos[1] <= y + 40:
                return i + 1
        return None