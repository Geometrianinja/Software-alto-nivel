import pygame
import random
import math
from typing import List, Tuple, Dict, Union
from enum import Enum, auto

pygame.init()

class InputType:
    MOUSE_CLICK = 0

'''
Função que coleta entradas do sistema, retorna uma lista de tuplas, onde o primeiro termo é o tipo de input e o segundo é as coordenadas do clique ou uma string indicando p fechamento do jogo
'''
def get_input() -> List[Tuple[InputType, Union[Tuple[int, int], str]]]:
    entradas = []
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            entradas.append((InputType.MOUSE_CLICK, "QUIT"))
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            entradas.append((InputType.MOUSE_CLICK, pygame.mouse.get_pos()))
    return entradas

''' 
Classe que gerencia as entradas 
'''
class InputManager:
    def __init__(self):
        self.entradas = []

    def update(self):
        self.entradas = get_input()

    def get_entradas(self):
        return self.entradas
    
'''
A classe Forma é resposável pela estetica das formas geometricas, sua trajetoria e saber se foi acertada
'''
class Forma:                                                                                    
    def __init__(self, tipo, largura, altura, x_inicial=None, y=None, tempo=0, velocidade=None):
        self.largura = largura
        self.altura = altura
        self.tipo = tipo
        #violeta,  violeta escuro, rosa escuro, rosa triste , azul escuro
        self.CORES = [(218, 112, 214), (148, 0, 211), (255, 105, 180), (216, 191, 216), (25, 25, 112)]
        self.cor = random.choice(self.CORES)
        self.raio = 30

        self.x_inicial = random.randint(150, self.largura - 150) 
        self.y = self.altura
        self.amplitude_y = self.altura - 100
        self.amplitude_x = 150
        self.tempo = tempo
        self.velocidade = random.uniform(0.0125, 0.025)

        self.impactada = False
        self.tempo_impacto = 0

    def atualizar(self):
        '''
        reposavel por atualizar a trajetoria do centro da forma 
        '''
        self.tempo += 1
        self.y = self.altura + (self.amplitude_y * math.sin(self.velocidade * self.tempo + 1.5))
        self.x = self.x_inicial + (self.amplitude_x * math.cos(0.01 * self.tempo))
        if self.impactada:
            self.tempo_impacto += 1

    def desenhar(self, tela):
        '''
        resposavel pelo desenho da forma e da sua sombra e pelos eveitos vizuaisdo clique
        para as fases será importante criar outros tipos de formas
        '''
        cor = (255, 255, 255) if self.impactada and self.tempo_impacto % 10 < 5 else self.cor
        cor_sombra = (50, 50, 50)
        deslocamento_sombra = 3.5

        if self.tipo == "Círculo":
            pygame.draw.circle(tela, cor_sombra, (int(self.x + deslocamento_sombra), int(self.y + deslocamento_sombra)), self.raio)
            pygame.draw.circle(tela, cor, (int(self.x), int(self.y)), self.raio)

        elif self.tipo == "Quadrado":
            pygame.draw.rect(tela, cor_sombra, (
                self.x - self.raio + deslocamento_sombra,
                int(self.y) - self.raio + deslocamento_sombra,
                self.raio * 2, self.raio * 2))
            pygame.draw.rect(tela, cor, (
                self.x - self.raio,
                int(self.y) - self.raio,
                self.raio * 2, self.raio * 2))

        elif self.tipo == "Triângulo":
            pontos = [(self.x, int(self.y) - self.raio),
                      (self.x - self.raio, int(self.y) + self.raio),
                      (self.x + self.raio, int(self.y) + self.raio)]
            pontos_sombra = [(x + deslocamento_sombra, y + deslocamento_sombra) for x, y in pontos]
            pygame.draw.polygon(tela, cor_sombra, pontos_sombra)
            pygame.draw.polygon(tela, cor, pontos)

   
    def foi_clicado(self, pos):
        '''
        a função hypot calcula a distancia entre dois pontos ele compara se a distancia do meio da forma até o corte é menor q o raio da forma se for a forma foi cortado 
        '''
        return math.hypot(self.x - pos[0], self.y - pos[1]) < self.raio
       
'''
A classe ControlaForma é resposavel por controlar a criação e exclusão das formas 
'''
class ControlaFormas:

    def __init__(self, largura, altura, qtd_circulos=2, qtd_quadrados=2, qtd_triangulos=2, limite_max_formas=10):
        self.largura = largura
        self.altura = altura
        self.formas = []
        self.T_excluir = 30
        self.limite_max_formas = limite_max_formas

        self.fila_formas = []
        self.delay_frames = 10
        self.contador_delay = 0

        self.contador_cortes = {
            "Círculo": 0,
            "Quadrado": 0,
            "Triângulo": 0
        }

        self.qtd_iniciais = {
            "Círculo": qtd_circulos,
            "Quadrado": qtd_quadrados,
            "Triângulo": qtd_triangulos
        }

        self.agendar_geracao_inicial()
    '''
    Arruma as gerações das formas se tem 3 triangulos ela os adiciona no fila fila_formas, q funciona como uma fila de espera
    '''
    def agendar_geracao_inicial(self):
        for tipo, qtd in self.qtd_iniciais.items():
            self.fila_formas.extend([tipo] * qtd)
    '''
    É chamada quando uma forma é cortada e gera uma forma do mesmo tipo da q foi cortada no final da fila
    '''
    def gerar_com_delay(self, tipo):
      self.fila_formas.append(tipo)
    '''
    Ela é chamada em cada frame, é reposnavel por gerar novas formas, atualizar a posição das formas e remover as formas q foram cortadas
    '''
    def atualizar_formas(self):
       
        self.contador_delay += 1
        if self.fila_formas and self.contador_delay >= self.delay_frames:

            if len(self.formas) < self.limite_max_formas:
                tipo = self.fila_formas.pop(0)
                self.formas.append(Forma(tipo, self.largura, self.altura))

            self.contador_delay = 0

        '''
        atualização de posição e exclusão das formas cortadas 
        tbm é possivel add aq a funcionalidade de excluir a forma caso ela saia da tela 
        '''
        novas = []
        for forma in self.formas:
            if forma.impactada and forma.tempo_impacto > self.T_excluir:
                continue  
            forma.atualizar()
            novas.append(forma)

        self.formas = novas

    def desenhar_formas(self, tela):
        for forma in self.formas:
            forma.desenhar(tela)
    '''
    confere se já foi clicada e se a posição do clique bate com a da forma, atualiza o contador da interface e coloca a forma do mesmo tipo na fila se o max n tiver sido atingido 
    '''
    def impactar_forma(self, pos):
        for forma in self.formas:
            if not forma.impactada and forma.foi_clicado(pos):
                forma.impactada = True
                self.contador_cortes[forma.tipo] += 1

                if len(self.formas) + len(self.fila_formas) < self.limite_max_formas:
                    self.gerar_com_delay(forma.tipo)
                break

'''
A classe jogo tem o looping principal e define o layout do jogo
'''
class Jogo:
    def __init__(self):

        self.LARGURA, self.ALTURA = 1000, 500

        self.tela = pygame.display.set_mode((self.LARGURA, self.ALTURA))
        pygame.display.set_caption("Geometria Ninja")

        self.fundo = pygame.image.load("fundo.gif").convert()
        self.fundo = pygame.transform.scale(self.fundo, (self.LARGURA, self.ALTURA))

        self.clock = pygame.time.Clock()
        self.controlador = ControlaFormas(self.LARGURA, self.ALTURA,
                                          qtd_circulos=2,
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

        self.input_manager = InputManager()
        
    '''
    ñ sei se durante o jogo mesmo deixamos o contador de formas cortadas ou não
    '''

    def desenhar_contador(self):
        y = 40
        for tipo, valor in self.controlador.contador_cortes.items():

            texto = self.fontecontador.render (f" {tipo.capitalize()}: {valor}", True,  (255, 105, 180))  
            self.tela.blit(texto, (40, y))
            y += 25
    '''
    Esse titulo meio piscando é só firula mas achei bonitinho
    '''
    def desenhar_titulo(self):
        
        self.contador_titulo += 1
        if self.contador_titulo >= self.intervalo_titulo:
            self.titulo_visivel = not self.titulo_visivel
            self.contador_titulo = 0

        '''
        Renderiza o texto 3 vezes com deslocamentos diferentes para criar o efeito
        '''
        texto_base = self.fontetitulo.render("GEOMETRIA NINJA", True, (255, 255, 255))
        texto_tremido1 = self.fontetitulo.render("GEOMETRIA NINJA", True, (218, 112, 214))
        texto_tremido2 = self.fontetitulo.render("GEOMETRIA NINJA", True, (216, 191, 216))

        x = self.LARGURA // 2
        y = 40

        base_rect = texto_base.get_rect(center=(x, y))

        offset_x = random.randint(-2, 2)
        offset_y = random.randint(-2, 2)

        self.tela.blit(texto_tremido2, base_rect.move(offset_x - 2, offset_y))
        self.tela.blit(texto_tremido1, base_rect.move(offset_x + 2, offset_y))
        self.tela.blit(texto_base, texto_base.get_rect(center=(x, y)))


    def rodar(self):
     
        while self.jogando:
            self.tela.blit(self.fundo, (0, 0))
            self.input_manager.update()

            for tipo, valor in self.input_manager.get_entradas():
                if tipo == InputType.MOUSE_CLICK:
                    if valor == "QUIT":
                        self.jogando = False
                    else:
                        self.controlador.impactar_forma(valor)

            self.controlador.atualizar_formas()
            self.controlador.desenhar_formas(self.tela)
            self.desenhar_contador()
            self.desenhar_titulo()

            pygame.display.flip()
            self.clock.tick(60)


        pygame.quit()

if __name__ == "__main__":
    Jogo().rodar()
