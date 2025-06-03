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
    def __init__(
        self, state_name, restart_state, qtd_inicial, 
        titulo, cor_titulo, cor_contador, CoresFormas,
        contador_cortes, alvo, max_cortes=10,
        max_erros=0, background_path=None,
        next_state="FASES"
    ):
        # === Parâmetros da Fase ===
        self.state_name = state_name                                        # Nome do estado da fase
        self.restart_state = restart_state                                  # Nome do tutorial que a fase deve retornar
        self.next_state = next_state                                        # Estado seguinte após completar a fase
        self.background_path = background_path                              # Caminho da imagem de fundo (opcional)
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
        self.formas = []                                                    # Formas atualmente na tela
        self.fila_formas = []                                               # Formas agendadas para aparecer com delay
        self.qtd_formas = 0                                                 # Quantidade total de formas criadas
        self.limite_max_formas = 6                                          # Máximo de formas simultâneas na tela

        # === Controle de Tempo e Delay ===
        self.tempo_excluir = 30                                             # Tempo (em frames) até excluir uma forma após acerto
        self.delay_frames = 10                                              # Delay entre uma forma e outra (em frames)
        self.contador_delay = 0                                             # Contador que acumula os frames

        # === Métricas da Fase ===
        self.cortes_totais = 0                                              # Número total de formas cortadas (acertos)
        self.erros = 0                                                      # Número de erros cometidos (formas cortadas erradas)
        self.completou = False                                              # Indica se o objetivo da fase foi alcançado

        # === Inicialização de Recursos ===
        self.gerar_imagens()                                                # Gera imagens dos textos ou recursos visuais
        self.agendar_geracao_inicial()                                      # Agendamento inicial para gerar as formas


    def agendar_geracao_inicial(self):
        """
        Agenda a geração inicial das formas com base nas quantidades definidas em `qtd_inicial`.

        As formas são adicionadas à fila `fila_formas` e contabilizadas em `qtd_formas`.
        """
        for tipo, qtd in self.qtd_inicial.items():
            self.fila_formas.extend([tipo] * qtd)
            self.qtd_formas += qtd

    def gerar_com_delay(self, tipo):
        """
        Adiciona uma nova forma do tipo especificado à fila para ser gerada após um atraso (delay).

        Args:
            tipo (str): O tipo da forma a ser adicionada.
        """
        self.fila_formas.append(tipo)
        self.qtd_formas += 1

    def criar_forma(self, tipo, largura, altura):
        """
        Cria uma instância de forma com base no tipo fornecido.

        Args:
            tipo (str): Tipo da forma a ser criada (ex: "Círculo", "Quadrado").
            largura (int): Largura da tela (usada para posicionamento da forma).
            altura (int): Altura da tela (usada para posicionamento da forma).

        Returns:
            Forma: Uma instância da forma solicitada.

        Raises:
            ValueError: Se o tipo informado não for reconhecido.
        """
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

    def gerar_imagens(self):
        """
        Gera os elementos visuais da fase, como o background e os textos de título e contador.
        """
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

        for forma in self.formas:
            forma.desenhar(tela)

        for txt in self.textos:
            tela.blit(self.surf[txt], self.rect[txt])

    def atualizar_forma(self, input_manager):
        """
        Atualiza o estado das formas na tela, processando interações do jogador e removendo formas antigas.

        Args:
            input_manager: Objeto que armazena as entradas do jogador, como cliques do mouse.
        """
        novas = []
        for forma in self.formas:
            if input_manager.mouse_left_pressed and not forma.impactada and forma.rect.collidepoint(input_manager.mouse_pos):
                forma.impactada = True
                self.cortes_totais += 1
                self.contador_cortes[forma.tipo] += 1
                if forma.tipo not in self.alvo:
                    print(forma.tipo)
                    self.erros += 1

                if len(self.formas) + len(self.fila_formas) < self.limite_max_formas:
                    self.gerar_com_delay(forma.tipo)
            forma.atualizar()

            if forma.tempo_impacto > self.tempo_excluir:
                self.qtd_formas -= 1
                continue
            forma.atualizar()
            novas.append(forma)
        self.formas = novas

    def atualizar(self, input_manager):
        """
        Atualiza o estado da fase atual.

        Controla a criação de novas formas, verifica condições de erro ou de término da fase
        e processa as interações com as formas.

        Args:
            input_manager: Objeto que representa as entradas do jogador (ex: cliques e posição do mouse).

        Returns:
            str: Nome do próximo estado do jogo (ou o estado atual se continuar).
        """
        self.contador_delay += 1
        if self.fila_formas and self.contador_delay >= self.delay_frames:
            if len(self.formas) < self.limite_max_formas:
                tipo = self.fila_formas.pop(0)                      # O(n) isso aqui
                self.formas.append(self.criar_forma(tipo, self.largura, self.altura))
            self.contador_delay = 0

        self.atualizar_forma(input_manager)

        if self.erros >= self.max_erros:
            self.reset()
            return self.restart_state

        if self.max_cortes > 0 and self.cortes_totais >= self.max_cortes:
            self.completou = True
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
    def __init__(self, largura, altura):
        state_name = "FASE00"
        restart_state = "INTRO0"
        titulo = "Tutorial"
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

        alvo = ["Círculo", "Quadrado", "Triângulo", "Retângulo"]

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
            contador_cortes, alvo, max_cortes = 20, max_erros = 3,
            background_path=background, next_state= "POSFASE00"
        )

class Fase01(FaseBase):
    def __init__(self, largura, altura):
        state_name = "FASE01"
        restart_state = "TUTORIAL1"
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

        alvo = ["Triângulo"]

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
            state_name, restart_state, qtd_iniciais, titulo, 
            cor_titulo, cor_contador, CoresFormas,
            contador_cortes, alvo, max_cortes = 10, max_erros = 3,
            background_path=background, next_state= "POSFASE01"
        )
