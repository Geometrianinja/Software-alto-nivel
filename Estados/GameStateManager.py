import pygame
import config
import Fases.fases as fases
import Estados.menu as menu
import Estados.menu_config as menu_config

class Gerenciador:
    """
    Gerenciador de estados do jogo.
    
    Esta classe é responsável por fazer a troca de estados, como por exemplo:
    sair do menu de fases para ir para a fase 01.
    
    """
    def __init__(self):
        """Inicializa o gerenciador de estados do jogo.
        
        Cria as instâncias de todos os estados e define o estado inicial como MENU.
        """
        
        self.estados = {

            "CONTROL": menu_config.ConfigControle(),
            "FASE00" : fases.Fase00(config.LARGURA, config.ALTURA),
            "MENU"   : menu.MenuPrincipal(), 
            "CONFIG" : menu_config.Configuracao(),
            "FASES"  : menu.Fases(),
            "FASE01" : fases.Fase01(config.LARGURA, config.ALTURA),
            "FASE02" : fases.Fase02(config.LARGURA, config.ALTURA),


            }
        
        self.estado_atual = self.estados["MENU"]  # Estado inicial

    def esta_em_fase(self):
        """Verifica se o estado atual é uma fase jogável.
    
        Returns:
            bool: Retorna True se o estado atual for uma fase (possuir o método 'impactar_forma'),
            caso contrário, retorna False.
        """
        return hasattr(self.estado_atual, 'impactar_forma')
    
    
    def atualizar(self, input_manager):
        """Atualiza o estado atual do jogo.
        
        Processa as lógicas de atualização do estado atual e altera o estado com o estado_informado,
        do qual pode ser o próprio estado.
        
        Args:
            input_manager: Variavel responsável por armazenar as entradas do jogador, como a posição do mouse.
            
        Returns:
            bool: Retorna True se o jogador deseja sair do jogo, caso contrário, retorna False.
        """
        if(input_manager.quit_just_pressed):
            return True
        
        estado_informado = self.estado_atual.atualizar(input_manager)
        self.estado_atual = self.estados[estado_informado]
        return False
    
    def desenhar(self, tela):
        """Desenha o estado atual na tela.
        
        Chama o método de renderização do estado atual.
        
        Args:
            tela (pygame.Surface): Superfície onde o estado será desenhado.
        """
        self.estado_atual.desenhar(tela)
        
    
    
    