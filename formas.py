import pygame
import math

import config
import util

from abc import ABC, abstractmethod

# ======================= Forma Base =======================
class Forma(ABC):
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.cor = cor
        self.impactada = False
        self.tempo_impacto = 0
        self.raio = 30

    @abstractmethod
    def desenhar(self, tela):
        pass

    def atualizar(self):
        self.tempo_impacto += 1 if self.impactada else 0

    def foi_clicado(self, pos):
        return math.hypot(self.x - pos[0], self.y - pos[1]) < self.raio

# ======================= Subclasses =======================
class Circulo(Forma):
    def desenhar(self, tela):
        pygame.draw.circle(tela, config.CORES["sombra"], (int(self.x + 3), int(self.y + 3)), self.raio)
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)

class Quadrado(Forma):
    def desenhar(self, tela):
        pygame.draw.rect(tela, config.CORES["sombra"], (self.x - self.raio + 3, self.y - self.raio + 3, self.raio*2, self.raio*2))
        pygame.draw.rect(tela, self.cor, (self.x - self.raio, self.y - self.raio, self.raio*2, self.raio*2))

class Triangulo(Forma):
    def desenhar(self, tela):
        pontos = [(self.x, self.y - self.raio),
                  (self.x - self.raio, self.y + self.raio),
                  (self.x + self.raio, self.y + self.raio)]
        sombra = [(x + 3, y + 3) for x, y in pontos]
        pygame.draw.polygon(tela, config.CORES["sombra"], sombra)
        pygame.draw.polygon(tela, self.cor, pontos)

# ======================= Controlador =======================
class ControlaFormas:
    def __init__(self, qtd_circulos=1, qtd_quadrados=1, qtd_triangulos=1, limite_max_formas=5):
        self.qtd_circulos = qtd_circulos
        self.qtd_quadrados = qtd_quadrados
        self.qtd_triangulos = qtd_triangulos
        self.limite_max_formas = limite_max_formas
        self.formas = []
        self.relogio = 0
        self.intervalo = 60
        
        self.contador_cortes = {
            "Círculo": 0,
            "Quadrado": 0,
            "Triângulo": 0
        }

    def gerar_formas(self):
        if len(self.formas) >= self.limite_max_formas:
            return

        for _ in range(self.qtd_circulos):
            x, y = util.gerar_posicao()
            self.formas.append(Circulo(x, y, util.gerar_cor()))

        for _ in range(self.qtd_quadrados):
            x, y = util.gerar_posicao()
            self.formas.append(Quadrado(x, y, util.gerar_cor()))

        for _ in range(self.qtd_triangulos):
            x, y = util.gerar_posicao()
            self.formas.append(Triangulo(x, y, util.gerar_cor()))

        self.formas = self.formas[:self.limite_max_formas]

    def atualizar_formas(self):
        self.relogio += 1
        if self.relogio >= self.intervalo:
            self.relogio = 0
            self.gerar_formas()

        for forma in self.formas:
            forma.atualizar()

    def desenhar_formas(self, tela):
        for forma in self.formas:
            forma.desenhar(tela)

    def impactar_forma(self, posicao):
        for forma in self.formas:
            if forma.foi_clicado(posicao) and not forma.impactada:
                forma.impactada = True
