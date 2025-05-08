


class ConfigControle():
    """
    Representa o menu de configuração do controle.
    
    Esta classe é responsável por gerenciar a configuração inicial do controle,
    onde o jogador configura a origem, vel...
    """
    def __init__(self):
        a = 1 
        
    def atualizar(self):
        pass
    
    def desenhar(self, tela):
        pass
    
    def processar_input(self, pos):
        return "CONTROL"
    
   
        
class Configuracao():
    """
    Menu de configurações do jogo.
    
    Nele o jogador poderá personalizar o volume do jogo/musica...
    
    """
    def __init__(self):
        self.opcoes = ["Musica", "Som geral", "Velocidade do controle"]
        
