import pygame
import config
import Fases.fases as fases
import Estados.menu as menu
import Estados.menu_config as menu_config
import IntrosTutoriais.introsetutoriais as introsetutoriais
import Posfase.posfase as posfase  

class Gerenciador:
    """
    Gerenciador de estados do jogo.
    
    Esta classe é responsável por fazer a troca de estados, como por exemplo:
    sair do menu de fases para ir para a fase 01.
    
    """
    def __init__(self, input_manager):
        """Inicializa o gerenciador de estados do jogo.
        
        Cria as instâncias de todos os estados e define o estado inicial como MENU.
        """
        self.input_manager = input_manager
        
        self.estados = {

            "CONTROL": menu_config.ConfigControle(input_manager),
            "MENU"   : menu.MenuPrincipal(self.input_manager), 
            "CONFIG" : menu_config.Configuracao(),
            "FASES"  : menu.Fases(self.input_manager),
            
            "INTRO0": introsetutoriais.Intro0(input_manager),
            "TUTORIAL0": introsetutoriais.Tutorial0(input_manager),
            "FASE00_" : fases.Fase00_( self.input_manager),
            "TUTORIAL0_": introsetutoriais.Tutorial0_(input_manager),
            "FASE00_E0" : fases.Fase00_E0(self.input_manager),
            "POSFASE00": introsetutoriais.PosFase00(self.input_manager),  

            "INTRO1": introsetutoriais.Intro1(input_manager),
            "TUTORIAL1": introsetutoriais.Tutorial1(input_manager),
            "FASE01_E0" : fases.Fase01_E0(self.input_manager),
            "ENTREETAPAS01_E0": introsetutoriais.EntreEtapas01_E0(self.input_manager),
            "FASE01_E1" : fases.Fase01_E1(self.input_manager),
            "POSFASE01": introsetutoriais.PosFase01(self.input_manager),
            
            "FASE02" : fases.Fase02(self.input_manager),
            "FASE03" : fases.Fase03(self.input_manager),
            "FASE04" : fases.Fase04(self.input_manager),
            "FASE05" : fases.Fase05(self.input_manager),

            "ENTREETAPAS06_E0": fases.EntreEtapas06_E0(self.input_manager),
            "FASE06_E0" : fases.Fase06_E0(self.input_manager),
            "ENTREETAPAS06_E1": fases.EntreEtapas06_E1(self.input_manager),
            "FASE06_E1" : fases.Fase06_E1(self.input_manager),
            "ENTREETAPAS06_E2": fases.EntreEtapas06_E2(self.input_manager),
            "FASE06_E2" : fases.Fase06_E2(self.input_manager),

            "FASE07" : fases.Fase07(self.input_manager),
            }

        self.estado_atual = self.estados["CONTROL"]  # Estado inicial

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
        if(self.input_manager.quit_just_pressed):
            if(self.input_manager.using_controller):
                self.input_manager.controller.stop()
            return True

        estado_informado = self.estado_atual.atualizar()
        if estado_informado is not None:
            self.estado_atual = self.estados[estado_informado]
        return False
    
    def desenhar(self, tela):
        """Desenha o estado atual na tela.
        
        Chama o método de renderização do estado atual.
        
        Args:
            tela (pygame.Surface): Superfície onde o estado será desenhado.
        """
        self.estado_atual.desenhar(tela)
        

        