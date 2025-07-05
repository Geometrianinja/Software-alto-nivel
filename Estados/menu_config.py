import pygame
from os.path import join

import config
import Fases.fases_antigo as fases_antigo
import entrada
from controller import *
import threading
import time
import formas

class ConfigControle():
    """
    Representa o menu de configuração do controle.
    
    Esta classe é responsável por gerenciar a configuração inicial do controle,
    onde o jogador configura a origem, vel...
    """
    def __init__(self, input_manager):
        """Inicializa o menu de configuração do controle.
    
        Define os estados iniciais da tela, como plano de fundo, mensagens,
        variáveis de conexão, calibração, e renderiza os elementos visuais iniciais.
        """
        self.estado_name = "CONTROL"
        self.next_state = "MENU"
        self.background_path = join('images', 'FlorestaInicio.png')
        self.opcoes = [["Background", "Background"], ["Mensagem1", "Mensagem1"],
                       ["Mensagem2", "Mensagem2"]]
        
        self.surf = {}
        self.rect = {}
        self.calib_pairs = []
        self.largura, self.altura = config.LARGURA, config.ALTURA  # Obtém as dimensões da tela

        self.color = pygame.Color("white")
        self.trying_to_connect = False
        self.connected = False
        self.calibrated = False
        self.font = pygame.font.Font("PressStart2P.ttf", 18)
        self.gera_imagens()

        self.input_manager: entrada.InputManager = input_manager

    def gera_imagens(self):
        """Gera e posiciona os elementos visuais iniciais da tela.
    
        Carrega a imagem de fundo e renderiza mensagens iniciais
        informando o status de conexão do controle.
        """
        imagem = pygame.image.load(self.background_path).convert_alpha()
        imagem = pygame.transform.scale(imagem, (config.LARGURA, config.ALTURA))
        self.surf["Background"] = imagem
        self.rect["Background"] = self.surf["Background"].get_rect(topleft=(0, 0))
        
        
        mensagem1 = "Pressione qualquer botão do mouse para usar o mouse"
        texto1 = self.font.render(mensagem1, True, (255, 255, 255))
        self.surf["Mensagem1"] = texto1
        self.rect["Mensagem1"] = texto1.get_rect(center=(config.LARGURA // 2, config.ALTURA - 120))
    
        mensagem2 = "Pressione ENTER para tentar conectar controle"
        texto2 = self.font.render(mensagem2, True, (255, 255, 255))
        self.surf["Mensagem2"] = texto2
        self.rect["Mensagem2"] = texto2.get_rect(center=(config.LARGURA // 2, config.ALTURA - 90))
        
        
    def new_image(self):
        """Atualiza a interface após a conexão do controle.
    
        Remove mensagens iniciais e adiciona novos elementos visuais 
        para auxiliar na calibração do controle, como alvos para mirar.
        """
        self.opcoes.remove(["Mensagem1", "Mensagem1"])
        self.opcoes.remove(["Mensagem2", "Mensagem2"])
        
        mensagem1 = "Mire nos alvos"
        texto1 = self.font.render(mensagem1, True, self.color)
        self.surf["Mensagem3"] = texto1
        self.rect["Mensagem3"] = texto1.get_rect(center=(config.LARGURA // 2, config.ALTURA - 150))
        self.opcoes.append(["Mensagem3", "Mensagem3"])
        
        self.target1 = formas.Circulo(40, (255, 255, 255), 0)
        self.target1.posicao = pygame.Vector2(config.LARGURA * 7 / 8, config.ALTURA * 7 / 8)
        self.surf["Circle01"] = self.target1
        self.opcoes.append(["Circle01", "Circle01"])

        self.target2 = formas.Circulo(40, (255, 255, 255), 0)
        self.target2.posicao = pygame.Vector2(config.LARGURA / 8, config.ALTURA / 8)
        self.surf["Circle02"] = self.target2
        self.opcoes.append(["Circle02", "Circle02"])

    def try_connect(self):
        """Tenta estabelecer a conexão com o controle.
    
        Tenta conectar-se ao controle, e verifica se o jogador deseja utilizar o mouse.
        Se a conexão for bem-sucedida, inicia uma nova thread para o controle e
        altera o estado visual da tela. Alternativamente, permite o uso do mouse
        caso o jogador pressione ENTER.

        Returns:
            str: Nome do estado atual do jogo, que pode continuar sendo "CONTROL" ou passar para o próximo.
        """
        if not self.connected:
            if self.input_manager.controller.connect(): #Tentativa de se conectar com o controle
                controller_thread = threading.Thread(target=self.input_manager.controller.run)
                controller_thread.start()
                self.input_manager.using_controller = True   #Isso aqui é para ele entrar no while do update
                self.connected = True
                self.new_image()    #Isso aqui é para gerar a tela com os dois circulos :D
                return self.estado_name
            print("Trying to connect...")
            time.sleep(0.05)
            return self.estado_name
        
    def atualizar(self):
        """Atualiza o estado da configuração do controle.

        Processa a tentativa de conexão ou o processo de calibração baseado
        nas entradas do jogador. Ao completar a calibração, altera o estado do jogo.
    
        Returns:
            str: Nome do próximo estado do jogo. Pode ser o próprio estado ou o "MENU".
        """
        if not self.trying_to_connect:
            if(self.input_manager.mouse_left_just_pressed or self.input_manager.mouse_right_just_pressed):
                self.connected = True
                return self.next_state
            if(self.input_manager.Key_enter_pressed):
                self.trying_to_connect = True

        if(not self.connected and self.trying_to_connect):
            return self.try_connect()
        elif self.calibrated:
            return self.next_state
        elif self.input_manager.cont_select_just_pressed:
            if len(self.calib_pairs) == 0:
                self.calib_pairs.append((self.input_manager.gyro[0], self.input_manager.gyro[1]))
                self.calib_pairs.append((self.target2.posicao.x, self.target2.posicao.y))
            else:
                self.calib_pairs.append((self.input_manager.gyro[0], self.input_manager.gyro[1]))
                self.calib_pairs.append((self.target1.posicao.x, self.target1.posicao.y))
                print(self.calib_pairs)
                self.input_manager.set_calibration_data(self.calib_pairs[0], self.calib_pairs[1], 
                                                   self.calib_pairs[2], self.calib_pairs[3])
                self.calibrated = True
        return self.estado_name
                    
    
    def desenhar(self, tela):
        """Renderiza os elementos visuais na tela.
    
        Exibe os elementos gráficos, como plano de fundo, textos e alvos de calibração.
        Elementos específicos podem ser ocultados com base no progresso da calibração.
    
        Args:
            tela: Superfície onde os elementos serão desenhados (geralmente a tela principal do jogo).
        """
        for (nome, estado) in self.opcoes:
            # Antes da primeira calibração, só mostra o círculo de cima
            if len(self.calib_pairs) == 0 and nome == "Circle01":
                continue
            # Depois da primeira calibração, só mostra o círculo de baixo
            if len(self.calib_pairs) != 0 and nome == "Circle02":
                continue
            objeto = self.surf[nome]
            if isinstance(objeto, formas.Forma):
                objeto.atualizar(self.input_manager.dt)
                objeto.desenhar(tela)
            else:
                tela.blit(self.surf[nome], self.rect[nome])

        
class Configuracao():
    """
    Menu de configurações do jogo.
    
    Nele o jogador poderá personalizar o volume do jogo/musica...
    
    """
    def _init_(self):
        self.opcoes = ["Musica", "Som geral", "Velocidade do controle"]
    


            
   
       