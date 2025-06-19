import pygame
import random
from os.path import join

import util
import entrada
import formas
import config
from formas import *
from abc import ABC, abstractmethod
from typing import Optional
from pygame.math import Vector2
from math import atan2

class FaseBase(ABC):
    def __init__(
        self, state_name, restart_state, qtd_inicial, 
        titulo, cor_titulo, cor_contador, CoresFormas,
        contador_cortes, alvo, input_manager, max_cortes=10,
        max_erros=0, background_path: Optional[str]=None,
        next_state="FASES"
    ):
        # === Parâmetros da Fase ===
        self.state_name = state_name                                        # Nome do estado da fase
        self.restart_state = restart_state                                  # Nome do tutorial que a fase deve retornar
        self.next_state = next_state                                        # Estado seguinte após completar a fase
        self.background_path: Optional[str] = background_path               # Caminho da imagem de fundo (opcional)
        self.titulo = titulo                                                # Texto do título exibido na tela
        self.cor_titulo = cor_titulo                                        # Cor do título
        self.cor_contador = cor_contador                                    # Cor do contador
        self.CoresFormas = CoresFormas                                      # Dicionário de cores das formas
        self.qtd_inicial = qtd_inicial                                      # Quantidade inicial de formas por tipo
        self.contador_cortes = contador_cortes                              # Dicionário de cortes realizados por tipo
        self.max_cortes = max_cortes                                        # Número máximo de cortes para passar de nível
        self.max_erros = max_erros                                          # Número máximo de erros permitidos
        self.alvo = alvo                                                    # Lista de tipos de formas que são o "alvo" correto

        # === Elementos visuais e gráficos ===
        self.surf = {}                                                      # Superfícies para elementos gráficos (ex: textos, botões)
        self.rect = {}                                                      # Retângulos associados às superfícies (posições na tela)
        self.textos = []                                                    # Lista de textos a serem desenhados
        self.font = pygame.font.Font("PressStart2P.ttf", 24)                # Fonte do título
        self.fonte_contador = pygame.font.Font("PressStart2P.ttf", 20)      # Fonte do contador

        # === Dimensões da Tela ===
        self.largura = config.LARGURA                                       # Largura da tela
        self.altura = config.ALTURA                                         # Altura da tela

        # === Controle de Formas ===
        self.formas: list[formas.Forma] = []                                # Formas atualmente na tela
        self.fila_formas: list[tuple[float, formas.Forma]] = []             # Formas agendadas para aparecer com delay
        self.formas_cortadas: list[formas.Forma] = []                       # Formas que foram cortadas
        self.limite_max_formas = 6                                          # Máximo de formas simultâneas na tela
        self.gravidade = 150                                                # Gravidade aplicada às formas

        # === Controle de Tempo e Delay ===
        self.tempo_excluir: float = 0.5                                     # Tempo (em segundos) até excluir uma forma após acerto
        self.delay_forma: float = 4                                         # Delay entre uma forma e outra (em segundos)
        self.contador_delay: float = 0                                      # Contador que acumula os segundos

        # === Métricas da Fase ===
        self.cortes_totais = 0                                              # Número total de formas cortadas (acertos)
        self.erros = 0                                                      # Número de erros cometidos (formas cortadas erradas)
        self.completou = False                                              # Indica se o objetivo da fase foi alcançado

        self.input_manager = input_manager                                  # Gerenciador de entradas do jogador
        # === Inicialização de Recursos ===
        self.gerar_imagens()                                                # Gera imagens dos textos ou recursos visuais



    def agendar_geracao_inicial(self):
        """
        Agenda a geração inicial das formas com base nas quantidades definidas em `qtd_inicial`.

        As formas são adicionadas à fila `fila_formas` e contabilizadas em `qtd_formas`.
        """
        tempo = 0
        for tipo, qtd in self.qtd_inicial.items():
            for _ in range(qtd):
                self.agendar_forma(tipo, tempo)
                tempo += 1.5

    def agendar_forma(self, tipo, tempo):
        """
        Agenda a criação de uma nova forma após um atraso (delay).

        Args:
            tipo (str): O tipo da forma a ser criada.
            tempo (float): O tempo de atraso antes da criação da forma.
        """
        self.fila_formas.append((self.input_manager.time + tempo, tipo))
    
    def get_qtd_formas(self) -> int:
        """
        Retorna a quantidade total de formas, incluindo as que estão na fila

        Returns:
            int: Número total de formas.
        """
        return len(self.formas) + len(self.fila_formas)

    def criar_forma(self, tipo):
        """
        Cria uma instância de forma com base no tipo fornecido.

        Args:
            tipo (str): Tipo da forma a ser criada (ex: "Círculo", "Quadrado").

        Returns:
            Forma: Uma instância da forma solicitada.

        Raises:
            ValueError: Se o tipo informado não for reconhecido.
        """
        velocidade = Vector2(random.uniform(-100, 100), random.uniform(-400, -250))
        posicao = Vector2(self.largura // 2 - velocidade.x*3, self.altura + 60)
        vel_rotacao = random.uniform(-180, 180)

        cor = random.choice(self.CoresFormas)
        if tipo == "Círculo":
            forma = Circulo(50, cor, self.gravidade)
        elif tipo == "Retângulo":
            forma = Retangulo(110, 70, cor, self.gravidade)
        elif tipo == "Quadrado":
            forma = Quadrado(100, cor, self.gravidade)
        elif tipo == "Triângulo Equilátero":
            forma = TrianguloEquilatero(100, cor, self.gravidade)
        elif tipo == "Estrela":
            forma = Estrela(80, cor, self.gravidade)
        elif tipo == "Ângulo":
            forma = Angulo(70, 30, random.uniform(30, 180), cor, self.gravidade)
        else:
            raise ValueError(f"Tipo de forma desconhecido: {tipo}")
        
        forma.posicao = posicao
        forma.velocidade = velocidade
        forma.velocidade_rotacao = vel_rotacao
        return forma


    def gerar_imagens(self):
        """
        Gera os elementos visuais da fase, como o background e os textos de título e contador.
        """
        if self.background_path:
            self.surf["Background"] = pygame.image.load(self.background_path).convert_alpha()
            self.surf["Background"] = pygame.transform.scale(self.surf["Background"], (self.largura, self.altura))
            self.rect["Background"] = self.surf["Background"].get_rect(center=(self.largura // 2, self.altura // 2))

        texto = self.font.render(self.titulo, True, self.cor_titulo)
        self.surf["Titulo"] = texto
        self.rect["Titulo"] = texto.get_rect(center = (self.largura // 2, 40))
        self.textos.append("Titulo")

        for tipo, valor in self.contador_cortes.items():
            self.textos.append(tipo)
        self.gerar_contador()

    def gerar_contador(self):
        """
        Atualiza a exibição dos contadores de formas cortadas na tela.
        """
        y = 20
        for tipo, valor in self.contador_cortes.items():
            texto = self.fonte_contador.render(f"{tipo}: {valor}", True, (255, 255, 255))
            self.surf[tipo] = texto
            self.rect[tipo] = texto.get_rect(topleft = (20, y))
            y += 25
        
    def desenhar(self, tela):
        """
        Desenha os elementos da fase na tela: background, formas e textos.

        Args:
            tela (Surface): Superfície (tela) onde os elementos serão desenhados.
        """
        tela.blit(self.surf["Background"], self.rect["Background"])

        for forma_list in [self.formas_cortadas, self.formas]:
            for forma in forma_list:
                forma.desenhar_com_sombra(tela)

        for txt in self.textos:
            tela.blit(self.surf[txt], self.rect[txt])

    def atualizar_formas(self):
        """
        Atualiza o estado das formas na tela, processando interações do jogador e removendo formas antigas.
        """
        mouse_vel_vector = Vector2(self.input_manager.mouse_diff)/self.input_manager.dt
        for idx in range(len(self.formas)-1, -1, -1):
            forma = self.formas[idx]
            if self.input_manager.mouse_left_pressed and forma.colide_com_segmento(self.input_manager.mouse_pos, self.input_manager.mouse_diff):
                self.cortes_totais += 1
                self.contador_cortes[forma.tipo] += 1
                if forma.tipo not in self.alvo:
                    print(forma.tipo)
                    self.erros += 1

                cortes = forma.cortar(self.input_manager.mouse_pos,  mouse_vel_vector)
                self.formas_cortadas.extend(cortes)  # Adiciona as formas cortadas à lista de cortadas
                self.formas.pop(idx)  # Remove a forma cortada da lista

                self.agendar_forma(forma.tipo, self.delay_forma)

        """
        for idx in range(len(self.formas_cortadas)-1, -1, -1):
            forma = self.formas_cortadas[idx]
            if self.input_manager.mouse_left_pressed and forma.colide_com_segmento(self.input_manager.mouse_pos, self.input_manager.mouse_diff):
                cortes = forma.cortar(self.input_manager.mouse_pos, mouse_vel_vector)
                self.formas_cortadas.pop(idx)  # Remove a forma cortada da lista
                self.formas_cortadas.extend(cortes)  # Adiciona as novas formas cortadas
        """

        for idx_lista, forma_list in enumerate([self.formas, self.formas_cortadas]):
            for idx in range(len(forma_list)-1, -1, -1):
                forma = forma_list[idx]
                forma.atualizar(self.input_manager.dt)
                if forma.posicao.y > self.altura + 100:  # Remove formas abaixo da tela
                    forma_list.pop(idx)

                    if idx_lista == 0:
                        self.agendar_forma(forma.tipo, self.delay_forma)

    def atualizar(self) -> str:
        """
        Atualiza o estado da fase atual.

        Controla a criação de novas formas, verifica condições de erro ou de término da fase
        e processa as interações com as formas.

        Returns:
            str: Nome do próximo estado do jogo (ou o estado atual se continuar).
        """
        if self.get_qtd_formas() == 0:
            self.agendar_geracao_inicial()

        for idx in range(len(self.fila_formas)-1, -1, -1):
            tempo, tipo = self.fila_formas[idx]
            if tempo < self.input_manager.time:
                self.formas.append(self.criar_forma(tipo))
                self.fila_formas.pop(idx)
                
        self.atualizar_formas()

        if self.erros >= self.max_erros:
            self.reset()
            return self.restart_state

        if self.max_cortes > 0 and self.cortes_totais >= self.max_cortes:
            self.completou = True
            self.reset()
            return self.next_state
        self.gerar_contador()
        return self.state_name

    def reset(self):
        """
        Reinicia o estado da fase para os valores iniciais.
        Limpa as formas e fila, zera contadores e atualiza as imagens.
        """
        self.formas = []
        self.fila_formas = []
        self.contador_cortes = {k: 0 for k in self.contador_cortes}
        self.cortes_totais = 0
        self.erros = 0
        self.completou = False
        self.gerar_imagens()
        self.agendar_geracao_inicial()


class Fase00(FaseBase):
    def __init__(self, largura, altura, input_manager: entrada.InputManager):
        state_name = "FASE00"
        restart_state = "INTRO0"
        titulo = "Tutorial"
        background = join('images', 'FASE0jogo.png')
        cor_titulo = pygame.Color("black")
        cor_contador = pygame.Color("black")

        qtd_iniciais = {
            "Círculo": 1,
            "Quadrado": 3,
            "Triângulo Equilátero": 2,
            "Retângulo": 1,
            "Estrela": 2,
            "Ângulo": 1
        }

        contador_cortes = {
            "Círculo": 0,
            "Quadrado": 0,
            "Triângulo Equilátero": 0,
            "Retângulo": 0,
            "Estrela": 0,
            "Ângulo": 0
        }

        alvo = ["Círculo", "Quadrado", "Triângulo Equilátero", "Retângulo", "Estrela", "Ângulo"]

        CoresFormas = [
            pygame.Color("darkolivegreen3"),
            pygame.Color("darkorchid1"),
            pygame.Color("yellow"),
            pygame.Color("steelblue1"),
            pygame.Color("orange1"),
        ]

        super().__init__(
            state_name, restart_state, qtd_iniciais, titulo, 
            cor_titulo, cor_contador, CoresFormas,
            contador_cortes, alvo, input_manager, max_cortes = 52, max_erros = 3,
            background_path=background, next_state= "POSFASE00"
        )

class Fase01(FaseBase):
    def __init__(self, largura, altura, input_manager: entrada.InputManager):
        state_name = "FASE01"
        restart_state = "TUTORIAL1"
        titulo = " "
        background = join('images', 'FASE1jogo.png')
        cor_titulo = pygame.Color("black")
        cor_contador = pygame.Color("black")

        qtd_iniciais = {
            "Círculo": 1,
            "Quadrado": 1,
            "Triângulo Equilátero": 1,
            "Retângulo": 0
        }

        alvo = ["Triângulo Equilátero"]

        contador_cortes = {
            "Círculo": 0,
            "Quadrado": 0,
            "Triângulo Equilátero": 0,
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
            state_name, restart_state, qtd_iniciais, titulo, 
            cor_titulo, cor_contador, CoresFormas,
            contador_cortes, alvo, input_manager, max_cortes=10, max_erros=3,
            background_path=background, next_state="POSFASE01"
        )


class Fase00_(FaseBase):
    def __init__(self, largura, altura, input_manager: entrada.InputManager):
        state_name = "FASE00_"
        restart_state = "TUTORIAL0"
        titulo = "Tutorial"
        background = join('images', 'FASE0jogo.png')
        cor_titulo = pygame.Color("black")
        cor_contador = pygame.Color("black")

        qtd_iniciais = {
            "Círculo": 1,
        }

        contador_cortes = {
            "Círculo": 0,
            "Triângulo Equilátero": 0,
            "Ângulo": 0
        }

        alvo = ["Círculo"]

        CoresFormas = [
            pygame.Color("darkolivegreen3"),
            pygame.Color("darkorchid1"),
            pygame.Color("yellow"),
            pygame.Color("steelblue1"),
            pygame.Color("orange1"),
        ]

        super().__init__(
            state_name, restart_state, qtd_iniciais, titulo, 
            cor_titulo, cor_contador, CoresFormas,
            contador_cortes, alvo, input_manager, max_cortes = 1, max_erros = 3,
            background_path=background, next_state= "TUTORIAL0_"
        )