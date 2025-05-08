import pygame
import math
import random
import config
import util

from abc import ABC, abstractmethod

# ======================= Forma Base =======================
class Forma(ABC):
    def __init__(self, largura, altura, cor, x_inicial=None, y=None, tempo=0, velocidade=None):
        self.largura = int(largura)
        self.altura = int(altura)
        self.cor = cor  
        self.raio = 50

        self.x_inicial = random.randint(100, self.largura - 100)
        self.y = self.altura
        self.amplitude_y = self.altura - 100
        self.amplitude_x = 20
        self.tempo = tempo
        self.velocidade = random.uniform(0.0125, 0.025)

        self.impactada = False
        self.tempo_impacto = 0
        
        self.surf = pygame.Surface((50, 50), pygame.SRCALPHA)  # Exemplo de tamanho, pode ajustar
        self.rect = self.surf.get_rect(center=(self.x_inicial, self.y)) 

    #@abstractmethod
    def atualizar(self):
        self.tempo += 1
        self.y = self.altura + (self.amplitude_y * math.sin(self.velocidade * self.tempo + 1.5))
        self.x = self.x_inicial + (self.amplitude_x * math.cos(0.01 * self.tempo))
        
        self.rect.center = (self.x, self.y) #Adicionado por Artur
        
        if self.impactada:
            self.tempo_impacto += 1
            


    def foi_clicado(self, pos):
        return math.hypot(self.x - pos[0], self.y - pos[1]) < self.raio

    def desenhar(self, tela):
        cor = (255, 255, 255) if self.impactada and self.tempo_impacto % 10 < 5 else self.cor
        cor_sombra = (50, 50, 50)
        deslocamento_sombra = 3.5
        self.desenhar_com_sombra(tela, cor, cor_sombra, deslocamento_sombra)
        
        
        self.surf.fill((0, 0, 0, 0)) 
        tela.blit(self.surf, self.rect)
        

# ======================= Subclasses =======================
class Circulo(Forma):
    def __init__(self, largura, altura, cor, **kwargs):
        super().__init__(largura, altura, cor, **kwargs)
        self.tipo = "Círculo"

    def desenhar_com_sombra(self, tela, cor, cor_sombra, deslocamento_sombra):
        pygame.draw.circle(tela, cor_sombra, (int(self.x + deslocamento_sombra), int(self.y + deslocamento_sombra)), self.raio)
        pygame.draw.circle(tela, cor, (int(self.x), int(self.y)), self.raio)

class Quadrado(Forma):
    def __init__(self, largura, altura, cor, **kwargs):
        super().__init__(largura, altura, cor, **kwargs)
        self.tipo = "Quadrado"

    def desenhar_com_sombra(self, tela, cor, cor_sombra, deslocamento_sombra):
        pygame.draw.rect(tela, cor_sombra, (
            self.x - self.raio + deslocamento_sombra,
            int(self.y) - self.raio + deslocamento_sombra,
            self.raio * 2, self.raio * 2))
        pygame.draw.rect(tela, cor, (
            self.x - self.raio,
            int(self.y) - self.raio,
            self.raio * 2, self.raio * 2))

class Triangulo(Forma):
    def __init__(self, largura, altura, cor, **kwargs):
        super().__init__(largura, altura, cor, **kwargs)
        self.tipo = "Triângulo"

    def desenhar_com_sombra(self, tela, cor, cor_sombra, deslocamento_sombra):
        pontos = [(self.x, int(self.y) - self.raio),
                  (self.x - self.raio, int(self.y) + self.raio),
                  (self.x + self.raio, int(self.y) + self.raio)]
        pontos_sombra = [(x + deslocamento_sombra, y + deslocamento_sombra) for x, y in pontos]
        pygame.draw.polygon(tela, cor_sombra, pontos_sombra)
        pygame.draw.polygon(tela, cor, pontos)

class Retangulo(Forma):
    def __init__(self, largura, altura, cor, **kwargs):
        super().__init__(largura, altura, cor, **kwargs)
        self.tipo = "Retângulo"
        self.largura_ret = self.raio * 2.5  # Definindo largura do retângulo
        self.altura_ret = self.raio * 1  

    def desenhar_com_sombra(self, tela, cor, cor_sombra, deslocamento_sombra):
        pygame.draw.rect(tela, cor_sombra, (
            self.x - self.largura_ret // 2 + deslocamento_sombra,
            self.y - self.altura_ret // 2 + deslocamento_sombra,
            self.largura_ret, self.altura_ret))
        pygame.draw.rect(tela, cor, (
            self.x - self.largura_ret // 2,
            self.y - self.altura_ret // 2,
            self.largura_ret, self.altura_ret))

