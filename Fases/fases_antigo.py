import pygame
import random
from os.path import join
from abc import ABC

import config
from formas import Circulo, Quadrado, Triangulo, Retangulo
from abc import ABC, abstractmethod

class FaseBase(ABC):
    def __init__(self, estado_name, largura, altura, qtd_iniciais, contador_cortes, cor_contador,
                 titulo, cor_titulo, CoresFormas, background_path=None, usa_imagens=False, fonte_titulo_tam=30,
                 max_cortes=10, proximo_estado="FASES"):
        self.estado_name = estado_name
        self.largura = largura        
        self.altura = altura  
        self.background_path = background_path
        self.usa_imagens = usa_imagens

        # Elementos gráficos e configuração visual
        self.surf = {}
        self.rect = {}
        self.font = pygame.font.Font("PressStart2P.ttf", 24)
        self.fonte_titulo = pygame.font.Font("PressStart2P.ttf", fonte_titulo_tam)
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

        # Contadores gerais
        self.cortes_totais = 0
        self.max_cortes = max_cortes
        self.proximo_estado = proximo_estado

        self.gera_imagens()
        self.agendar_geracao_inicial()

    def atualizar(self, input_manager=None):
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

        # Se input_manager for passado, processa clique
        if input_manager:
            for forma in self.formas:
                if (not forma.impactada) and input_manager.mouse_left_pressed and forma.foi_clicado(input_manager.mouse_pos):
                    self.impactar_forma(input_manager.mouse_pos)

        # Checa condição de vitória padrão
        if self.max_cortes > 0 and self.cortes_totais >= self.max_cortes:
            return self.proximo_estado

        return self.estado_name

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
        rect = texto.get_rect(center=(self.largura // 2, 40 if self.fonte_titulo.get_height() < 40 else 50))
        tela.blit(texto, rect)

    def desenhar_contador(self, tela):
        y = 40
        for tipo, valor in self.contador_cortes.items():
            texto = self.fonte_contador.render(f"{tipo}: {valor}", True, (255, 255, 255))
            tela.blit(texto, (20, y))
            y += 25

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

    def impactar_forma(self, pos):
        for forma in self.formas:
            if not forma.impactada and forma.foi_clicado(pos):
                forma.impactada = True
                self.contador_cortes[forma.tipo] += 1
                self.cortes_totais += 1
                if len(self.formas) + len(self.fila_formas) < self.limite_max_formas:
                    self.gerar_com_delay(forma.tipo)
                return True
        return False

    def processar_input(self, pos):
        return self.impactar_forma(pos)

    def gera_imagens(self):
        if self.background_path:
            self.surf["Background"] = pygame.image.load(self.background_path).convert_alpha()
            self.surf["Background"] = pygame.transform.scale(self.surf["Background"], (self.largura, self.altura))
            self.rect["Background"] = self.surf["Background"].get_rect(center=(self.largura // 2, self.altura // 2))


class Fase00(FaseBase):
    def __init__(self, largura, altura):
        estado_name = "FASE00"
        titulo = "Fase 0"
        background = join('images', 'FASE0jogo.png')
        cor_titulo = pygame.Color("black")
        cor_contador = pygame.Color("black")

        qtd_iniciais = {
            "Círculo": 1,
            "Quadrado": 3,
            "Triângulo": 2,
            "Retângulo": 1
        }

        contador_cortes = {
            "Círculo": 0,
            "Quadrado": 0,
            "Triângulo": 0,
            "Retângulo": 0
        }

        CoresFormas = [
            pygame.Color("darkolivegreen3"),
            pygame.Color("darkorchid1"),
            pygame.Color("yellow"),
            pygame.Color("steelblue1"),
            pygame.Color("orange1"),
        ]

        super().__init__(
            estado_name, largura, altura, qtd_iniciais, contador_cortes,
            cor_contador, titulo, cor_titulo, CoresFormas,
            background_path=background, usa_imagens=True,
            max_cortes=10, proximo_estado="POSFASE00"
        )

    def reset(self):
        self.formas = []
        self.fila_formas = []
        self.contador_cortes = {k: 0 for k in self.contador_cortes}
        self.cortes_totais = 0
        self.agendar_geracao_inicial()


class Fase01(FaseBase):
    def __init__(self, largura, altura):
        estado_name = "FASE01"
        titulo = " "
        background = join('images', 'FASE1jogo.png')
        cor_titulo = pygame.Color("black")
        cor_contador = pygame.Color("black")

        qtd_iniciais = {
            "Círculo": 1,
            "Quadrado": 1,
            "Triângulo": 1,
            "Retângulo": 0
        }

        contador_cortes = {
            "Círculo": 0,
            "Quadrado": 0,
            "Triângulo": 0,
            "Retângulo": 0
        }

        CoresFormas = [
            pygame.Color("darkolivegreen3"),
            pygame.Color("darkorchid1"),
            pygame.Color("yellow"),
            pygame.Color("steelblue1"),
            pygame.Color("orange1"),
        ]

        super().__init__(
            estado_name, largura, altura, qtd_iniciais, contador_cortes,
            cor_contador, titulo, cor_titulo, CoresFormas,
            background_path=background, usa_imagens=True, fonte_titulo_tam=50,
            max_cortes=10, proximo_estado="POSFASE01"
        )
        self.max_erros = 3
        self.erros = 0
        self.completou = False

    def reset(self):
        self.formas = []
        self.fila_formas = []
        self.contador_cortes = {k: 0 for k in self.contador_cortes}
        self.cortes_totais = 0
        self.erros = 0
        self.completou = False
        self.agendar_geracao_inicial()
##o atualizar é o mesmo da fase 0, mas com a condição de erro por isso não usa o da fase base
    def atualizar(self, input_manager=None):
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

        # Processa input
        if input_manager:
            for forma in self.formas:
                if (not forma.impactada) and input_manager.mouse_left_pressed and forma.foi_clicado(input_manager.mouse_pos):
                    # Se o tipo da forma NÃO for "Quadrado", conta como erro
                    # (Neste exemplo, só é permitido cortar Quadrados, cortar outros tipos é erro)
                    if forma.tipo != "Quadrado":
                        self.erros += 1  # Incrementa o contador de erros
                    # Marca a forma como impactada (cortada) e atualiza os contadores de cortes
                    self.impactar_forma(input_manager.mouse_pos)

        # Checa condição de erro
        if self.erros >= self.max_erros:
            return "TUTORIAL1"  # Volta para o tutorial da fase 1

        # Checa condição de vitória padrão
        if self.cortes_totais >= self.max_cortes:
            return self.proximo_estado

        return self.estado_name