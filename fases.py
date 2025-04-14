import pygame

import entrada
import formas
import config
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

class FaseMenu:
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

class Fase1(FaseBase):
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
