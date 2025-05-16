import pygame
import random
from os.path import join

import util
import entrada
import formas
import config
from formas import Circulo, Quadrado, Triangulo, Retangulo
from abc import ABC, abstractmethod

class FaseBase(ABC):

    def __init__(self, estado_name, largura, altura, qtd_iniciais, contador_cortes, cor_contador,
                 titulo, cor_titulo, CoresFormas, background_path = None, usa_imagens = False):
        
        # Informações gerais da fase
        self.estado_name = estado_name
        self.largura = config.LARGURA
        self.altura = config.ALTURA
        self.background_path = background_path
        self.usa_imagens = usa_imagens
        
        
        # Elementos gráficos e configuração visual
        self.surf = {}
        self.rect = {}
        self.font = pygame.font.Font("PressStart2P.ttf", 24)
        self.fonte_titulo = pygame.font.Font("PressStart2P.ttf", 24)
        self.fonte_contador = pygame.font.Font("PressStart2P.ttf", 20)
        self.titulo = titulo
        self.cor_titulo = cor_titulo
        self.cor_contador = cor_contador        
        
        # Formas e controle de jogo
        self.formas = []
        self.qtd_iniciais = qtd_iniciais
        self.contador_cortes = contador_cortes
        self.CoresFormas = CoresFormas
        self.limite_max_formas = 12
        self.T_excluir = 30
        
        # Controle de geração
        self.fila_formas = []
        self.delay_frames = 10
        self.contador_delay = 0
        
        self.gera_imagens()
        self.agendar_geracao_inicial()

    def atualizar(self, input_manager):
        for forma in self.formas:
            if (not forma.impactada) and input_manager.mouse_left_pressed and forma.foi_clicado(input_manager.mouse_pos):
                forma.impactada = True
                self.contador_cortes[forma.tipo] += 1
                if len(self.formas) + len(self.fila_formas) < self.limite_max_formas:
                     self.gerar_com_delay(forma.tipo)
            forma.atualizar()
    
        self.contador_delay += 1
        if self.fila_formas and self.contador_delay >= self.delay_frames:
            if len(self.formas) < self.limite_max_formas:
                tipo = self.fila_formas.pop(0)
                self.formas.append(self.criar_forma(tipo, self.largura, self.altura))
            self.contador_delay = 0

        novas = []
        for forma in self.formas:
            if forma.tempo_impacto > self.T_excluir:
                continue
            forma.atualizar()
            novas.append(forma)
        self.formas = novas
        
        return self.estado_name

        """
        for forma in self.formas:
            if input_manager.mouse_left_pressed and not forma.impactada and self.rect[forma].collidepoint(input_manager.mouse_pos):
                forma.impactada = True
            forma.atualizar()
        """
    def impactar_forma(self, pos):
        for forma in self.formas:
            if not forma.impactada and forma.foi_clicado(pos):
                forma.impactada = True
                self.contador_cortes[forma.tipo] += 1
                if len(self.formas) + len(self.fila_formas) < self.limite_max_formas:
                    self.gerar_com_delay(forma.tipo)
                return True
        return False
    
    
    def agendar_geracao_inicial(self):
        for tipo, qtd in self.qtd_iniciais.items():
            self.fila_formas.extend([tipo] * qtd)
            
    def gerar_com_delay(self, tipo):
        self.fila_formas.append(tipo)

        
    def gera_imagens(self):
        if self.background_path:
            self.surf["Background"] = pygame.image.load(self.background_path).convert_alpha()
            self.rect["Background"] = self.surf["Background"].get_rect(center=(config.LARGURA / 2, config.ALTURA / 2))

        """for i, (nome, estado) in enumerate(self.opcoes):
            if self.usa_imagens:
                imagem_path = join('images', f'{nome}_button.png')
                imagem_original = pygame.image.load(imagem_path).convert_alpha()
                novo_tamanho = (200, 80)
                self.surf[nome] = pygame.transform.smoothscale(imagem_original, novo_tamanho)
                self.rect[nome] = self.surf[nome].get_rect(center=(config.LARGURA / 2, config.ALTURA / 2 + i * 100))
            else:
                cor = config.CORES["branco"]
                self.surf[nome] = self.font.render(nome, True, cor)
                self.rect[nome] = self.surf[nome].get_rect(topleft=(config.LARGURA // 2 - 100, 150 + i * 60))"""

    
    def desenhar(self, tela):
        if "Background" in self.surf:
            tela.blit(self.surf["Background"], self.rect["Background"])
        else:
            tela.fill((20, 20, 20))
            
        for forma in self.formas:
            forma.desenhar(tela)    
            
        self.desenhar_titulo(tela)
        self.desenhar_contador(tela)
        
    def desenhar_titulo(self, tela):
            
            texto = self.fonte_titulo.render(self.titulo, True, self.cor_titulo)
            rect = texto.get_rect(center=(self.largura // 2, 40))
            tela.blit(texto, rect)
            
    def desenhar_contador(self, tela):
        y = 40
        for tipo, valor in self.contador_cortes.items():
            texto = self.fonte_contador.render(f"{tipo}: {valor}", True, (255, 255, 255))
            tela.blit(texto, (20, y))
            y += 25
           
    def criar_forma(self, tipo, largura, altura):
        cor = random.choice(self.CoresFormas)
        if tipo == "Círculo":
            return Circulo(largura, altura, cor)
        if tipo == "Retângulo":
            return Retangulo(largura, altura, cor)
        elif tipo == "Quadrado":
            return Quadrado(largura, altura, cor)
        elif tipo == "Triângulo":
            return Triangulo(largura, altura, cor)
        else:
            raise ValueError(f"Tipo de forma desconhecido: {tipo}")


class Fase00(FaseBase):
    def __init__(self, largura, altura):
        estado_name = "FASE00"
        titulo = "Fase 0"
        background = join('images', 'dojo01.gif')
        cor_titulo = pygame.Color("darkgoldenrod")
        cor_contador = pygame.Color("darkgoldenrod")

        qtd_iniciais = {
            "Círculo": 0,
            "Quadrado": 3,
            "Triângulo": 2,
            "Retângulo": 0
        }

        contador_cortes = {
            "Círculo": 0,
            "Quadrado": 0,
            "Triângulo": 0,
            "Retângulo": 0
        }

        CoresFormas = [
            pygame.Color("darkgoldenrod"),
            pygame.Color("tan"),
            pygame.Color("peachpuff"),
            pygame.Color("saddlebrown"),
        ]

        super().__init__(
            estado_name, largura, altura, qtd_iniciais, contador_cortes,
            cor_contador, titulo, cor_titulo, CoresFormas,
            background_path=background, usa_imagens=True
        )


class Fase01(FaseBase):
    def __init__(self, largura, altura):
        self.largura = config.LARGURA
        self.altura = config.ALTURA

        self.cor_contador = pygame.Color("darkgoldenrod")

        self.titulo = "Fase 1"
        self.cor_titulo = pygame.Color("darkgoldenrod")
        self.CoresFormas = [
            pygame.Color("darkgoldenrod"),
            pygame.Color("tan"),
            pygame.Color("peachpuff"),
            pygame.Color("saddlebrown"),
        ]

        self.plano_de_fundo = pygame.image.load(join('images', 'dojo.jpg')).convert_alpha()
        self.plano_de_fundo = pygame.transform.scale(self.plano_de_fundo, (largura, altura))

        self.formas = []
        self.T_excluir = 30
        self.limite_max_formas = 12

        self.fila_formas = []
        self.delay_frames = 10
        self.contador_delay = 0

        self.contador_cortes = {
            "Círculo": 0,
            "Quadrado": 0,
            "Triângulo": 0,
            "Retângulo": 0
        }

        self.qtd_iniciais = {
            "Círculo": 0,
            "Quadrado": 3,
            "Triângulo": 2,
            "Retângulo": 0
        }

        self.agendar_geracao_inicial()

        self.fonte_titulo = pygame.font.Font("PressStart2P.ttf", 24)
        self.fonte_contador = pygame.font.Font("PressStart2P.ttf", 20)


    def desenhar_titulo(self, tela):
        texto = self.fonte_titulo.render(self.titulo, True, self.cor_titulo)
        rect = texto.get_rect(center=(self.largura // 2, 40))
        tela.blit(texto, rect)

    def agendar_geracao_inicial(self):
        for tipo, qtd in self.qtd_iniciais.items():
            self.fila_formas.extend([tipo] * qtd)

    def criar_forma(self, tipo, largura, altura):
        cor = random.choice(self.CoresFormas)
        if tipo == "Círculo":
            return Circulo(largura, altura, cor)
        if tipo == "Retângulo":
            return Retangulo(largura, altura, cor)
        elif tipo == "Quadrado":
            return Quadrado(largura, altura, cor)
        elif tipo == "Triângulo":
            return Triangulo(largura, altura, cor)
        else:
            raise ValueError(f"Tipo de forma desconhecido: {tipo}")

    def gerar_com_delay(self, tipo):
        self.fila_formas.append(tipo)

    def atualizar(self):
        self.contador_delay += 1
        if self.fila_formas and self.contador_delay >= self.delay_frames:
            if len(self.formas) < self.limite_max_formas:
                tipo = self.fila_formas.pop(0)
                self.formas.append(self.criar_forma(tipo, self.largura, self.altura))
            self.contador_delay = 0

        novas = []
        for forma in self.formas:
            if forma.tempo_impacto > self.T_excluir:
                continue
            forma.atualizar()
            novas.append(forma)
        self.formas = novas

    def desenhar(self, tela):
        tela.blit(self.plano_de_fundo, (0, 0))
        for forma in self.formas:
            forma.desenhar(tela)

        # Desenha o contador de cortes na tela
        y = 40
        for tipo, valor in self.contador_cortes.items():
            texto = self.fonte_contador.render(f"{tipo}: {valor}", True, (255, 255, 255))
            tela.blit(texto, (20, y))
            y += 25

    def impactar_forma(self, pos):
        for forma in self.formas:
            if not forma.impactada and forma.foi_clicado(pos):
                forma.impactada = True
                self.contador_cortes[forma.tipo] += 1
                if len(self.formas) + len(self.fila_formas) < self.limite_max_formas:
                    self.gerar_com_delay(forma.tipo)
                return True
        return False

    def processar_input(self, pos):
        return self.impactar_forma(pos)

class Fase02(FaseBase):
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self.cor_contador = pygame.Color("darkgoldenrod")

        self.titulo = "Fase 2"
        self.cor_titulo = pygame.Color("darkgoldenrod")
        self.CoresFormas = [
            pygame.Color("darkgoldenrod"),
            pygame.Color("tan"),
            pygame.Color("peachpuff"),
            pygame.Color("saddlebrown"),
        ]

        self.surf = {}
        self.rect = {}
        self.surf["Background"] = pygame.image.load(join('images', 'dojo01.gif')).convert_alpha()
        self.rect["Background"] = self.surf["Background"].get_rect(center=(config.LARGURA / 2, config.ALTURA / 2))

        self.formas = []
        self.T_excluir = 30
        self.limite_max_formas = 12

        self.fila_formas = []
        self.delay_frames = 10
        self.contador_delay = 0

        self.contador_cortes = {
            "Círculo": 0,
            "Quadrado": 0,
            "Triângulo": 0,
            "Retângulo": 0
        }

        self.qtd_iniciais = {
            "Círculo": 0,
            "Quadrado": 3,
            "Triângulo": 2,
            "Retângulo": 0
        }

        self.agendar_geracao_inicial()
        self.pontos = 3  # Pontos do jogador, diminuem ao clicar errado
        self.max_cortes = 5  # Cortes corretos para passar para o próximo nível
        self.cortes_corretos = 0  # Contador de cortes corretos
        self.fonte_titulo = pygame.font.Font("PressStart2P.ttf", 24)
        self.fonte_contador = pygame.font.Font("PressStart2P.ttf", 20)

    def agendar_geracao_inicial(self):
        for tipo, qtd in self.qtd_iniciais.items():
            self.fila_formas.extend([tipo] * qtd)

    def criar_forma(self, tipo, largura, altura):
        cor = random.choice(self.CoresFormas)
        if tipo == "Círculo":
            return Circulo(largura, altura, cor)
        if tipo == "Retângulo":
            return Retangulo(largura, altura, cor)
        elif tipo == "Quadrado":
            return Quadrado(largura, altura, cor)
        elif tipo == "Triângulo":
            return Triangulo(largura, altura, cor)
        else:
            raise ValueError(f"Tipo de forma desconhecido: {tipo}")

    def gerar_com_delay(self, tipo):
        self.fila_formas.append(tipo)

    def atualizar(self):
        self.contador_delay += 1
        if self.fila_formas and self.contador_delay >= self.delay_frames:
            if len(self.formas) < self.limite_max_formas:
                tipo = self.fila_formas.pop(0)
                self.formas.append(self.criar_forma(tipo, self.largura, self.altura))
            self.contador_delay = 0

        novas = []
        for forma in self.formas:
            if forma.tempo_impacto > self.T_excluir:
                continue
            forma.atualizar()
            novas.append(forma)
        self.formas = novas

    def desenhar(self, tela):
        tela.blit(self.surf["Background"], self.rect["Background"])
        for forma in self.formas:
            forma.desenhar(tela)

        # Desenha o contador de cortes na tela
        y = 40
        for tipo, valor in self.contador_cortes.items():
            texto = self.fonte_contador.render(f"{tipo}: {valor}", True, (255, 255, 255))
            tela.blit(texto, (20, y))
            y += 25

        # Desenha o contador de pontos
        texto_pontos = self.fonte_contador.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        tela.blit(texto_pontos, (20, y))

    def impactar_forma(self, pos):
        for forma in self.formas:
            if not forma.impactada and forma.foi_clicado(pos):
                forma.impactada = True
                if forma.tipo == "Triângulo":  # Se clicar no Triângulo, perde 1 ponto
                    self.pontos -= 1
                    if self.pontos == 0:
                        return "game_over"
                if forma.tipo == "Quadrado": # Se clicar no Quadrado, ganha 1 ponto
                    self.contador_cortes[forma.tipo] += 1
                    self.cortes_corretos += 1
                    if self.cortes_corretos >= self.max_cortes:
                        return "proximo_nivel"
                if len(self.formas) + len(self.fila_formas) < self.limite_max_formas:
                    self.gerar_com_delay(forma.tipo)
                return True
        return False
    
    def reiniciar(self):
        self.formas.clear()
        self.fila_formas.clear()
        self.agendar_geracao_inicial()
        self.contador_cortes = {k: 0 for k in self.contador_cortes}
        self.pontos = 3
        self.cortes_corretos = 0
        self.contador_delay = 0
        
    def processar_input(self, pos):
        resultado = self.impactar_forma(pos)
        if resultado in ["game_over", "proximo_nivel"]:
            self.reiniciar()
            return "MENU"
