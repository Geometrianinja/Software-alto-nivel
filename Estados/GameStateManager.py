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
    def __init__(self):
        """Inicializa o gerenciador de estados do jogo.
        
        Cria as instâncias de todos os estados e define o estado inicial como MENU.
        """
        
        self.estados = {

            "CONTROL": menu_config.ConfigControle(),
            "INTRO0": introsetutoriais.Intro0(),
            "TUTORIAL0": introsetutoriais.Tutorial0(),
            "FASE00" : fases.Fase00(config.LARGURA, config.ALTURA),
            "POSFASE00": posfase.PosFase00(),  
            "MENU"   : menu.MenuPrincipal(), 
            "CONFIG" : menu_config.Configuracao(),
            "FASES"  : menu.Fases(),
            "INTRO1": introsetutoriais.Intro1(),
            "TUTORIAL1": introsetutoriais.Tutorial1(),
            "FASE01" : fases.Fase01(config.LARGURA, config.ALTURA),
            "POSFASE01": posfase.PosFase01(), 

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
        if input_manager.quit_just_pressed:
            return True

        estado_informado = self.estado_atual.atualizar(input_manager)
        # Verifica se o estado informado existe no dicionário de estados
        if estado_informado in self.estados:
            # Só executa o reset se realmente houve troca de estado
            # Isso evita que o método reset seja chamado a cada frame, o que impediria o avanço das imagens.
            if self.estado_atual != self.estados[estado_informado]:
                # Se o novo estado possui o método reset, chama-o para garantir que o estado comece "zerado"
                # Isso é importante para slides, tutoriais, fases e pós-fases, pois garante que ao entrar novamente
                # (por exemplo, após perder ou voltar do menu), o progresso interno (índices, erros, etc.) seja reiniciado.
                if hasattr(self.estados[estado_informado], "reset"):
                    self.estados[estado_informado].reset()
            # Atualiza o estado atual para o novo estado informado
            self.estado_atual = self.estados[estado_informado]
        return False
    
    def desenhar(self, tela):
        """Desenha o estado atual na tela.
        
        Chama o método de renderização do estado atual.
        
        Args:
            tela (pygame.Surface): Superfície onde o estado será desenhado.
        """
        self.estado_atual.desenhar(tela)



