import pygame
import config
from formas import *

class SlideShowBase:
    def __init__(self, estado_name, imagens, proximo_estado, estado_anterior, input_manager, legendas, x, y, largura_maxima, formas):
        self.estado_name = estado_name
        self.imagens = [pygame.image.load(img).convert_alpha() for img in imagens]
        self.index = 0
        self.proximo_estado = proximo_estado
        self.estado_anterior = estado_anterior
        self.input_manager = input_manager

        self.pos_x = x
        self.pos_y = y
        self.largura_maxima = largura_maxima
        self.fonte = pygame.font.Font("PressStart2P.ttf", 18 * round(config.UN)) 
        self.texto_mostrado = ""        
        self.texto_index = 0            
        self.tempo_ultima_letra = 0     
        self.velocidade_texto = 35      
        self.legendas = self.carregar_legendas_em_blocos(legendas)
        
        self.formas = formas

    def carregar_legendas_em_blocos(self, caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.read().split('\n\n')
            return [bloco.replace('\n', ' ') for bloco in linhas if bloco.strip()]

    def reset(self):
        self.index = 0
        self.texto_index = 0
        self.texto_mostrado = ""  
        self.tempo_ultima_letra = 0     

    def atualizar(self):

        if (self.input_manager.mouse_right_just_pressed or self.input_manager.cont_back_just_pressed):
            self.reset()
            return self.estado_anterior
                
        tempo = pygame.time.get_ticks()
        legenda_atual = self.legendas[self.index] if self.index < len(self.legendas) else ""

        if self.texto_index < len(legenda_atual):
            if tempo - self.tempo_ultima_letra > self.velocidade_texto:
                self.texto_mostrado += legenda_atual[self.texto_index]
                self.texto_index += 1
                self.tempo_ultima_letra = tempo

        avancar = self.input_manager.mouse_left_just_pressed or self.input_manager.cont_select_just_pressed
        if avancar:
            if self.texto_index < len(legenda_atual):
                
                self.texto_mostrado = legenda_atual
                self.texto_index = len(legenda_atual)
            elif self.index < len(self.imagens) - 1:
                self.index += 1
                self.texto_mostrado = ""
                self.texto_index = 0
                self.tempo_ultima_letra = tempo
            else:
                self.reset()
                return self.proximo_estado

        if self.input_manager.cont_back_just_pressed:
            self.reset()
            return "MENU"
        return self.estado_name
    
    def quebrar_texto(self):
        palavras = self.texto_mostrado.split()
        linhas = []
        linha_atual = ""

        for palavra in palavras:
            test_linha = linha_atual + palavra + " "
            if self.fonte.size(test_linha)[0] <= self.largura_maxima:
                linha_atual = test_linha
            else:
                linhas.append(linha_atual)
                linha_atual = palavra + " "
        if linha_atual:
            linhas.append(linha_atual)
        return linhas
    
    def desenhar(self, tela):
        tela.fill((0, 0, 0))
        if self.index < len(self.imagens):
            img = pygame.transform.scale(self.imagens[self.index], tela.get_size())
            tela.blit(img, (0, 0))

            linhas = self.quebrar_texto()

            for i, linha in enumerate(linhas):
                superficie = self.fonte.render(linha, True, (0, 0, 0))  
                tela.blit(superficie, (self.pos_x, self.pos_y + i * 28 * config.UN))  

        if self.index < len(self.formas):
            for forma in self.formas[self.index]:
                forma.desenhar(tela)

                

class Intro0(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE0intro.png" for _ in range(2)
        ]
        legendas = "IntrosTutoriais/Introducoes/Introducao_0.txt"
        pos_x = 250*config.LARGURA //1000
        pos_y = 50*config.ALTURA //1000
        largura_max = 400*config.LARGURA //1000
        formas = [[] for _ in range(2)]
        super().__init__("INTRO0", imagens, "TUTORIAL0", "FASES",input_manager, legendas, pos_x, pos_y, largura_max, formas)

class Tutorial0(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE0tutorial.png" for _ in range(6)
        ]
        legendas = "IntrosTutoriais/Tutoriais/Tutorial_0.txt"
        pos_x = 150*config.LARGURA //1000
        pos_y = 90*config.ALTURA //1000
        largura_max = 740*config.LARGURA //1000

        circulo_branco = Circulo(27, config.Cores.BRANCO, 0)
        circulo_branco.posicao = Vector2(config.LARGURA * (0.5), config.ALTURA *(0.5 - 198/500))

        circulo_vermelho = Circulo(27, config.Cores.VERMELHO, 0)
        circulo_vermelho.posicao = Vector2(config.LARGURA * (0.5 + 40/1000), config.ALTURA *(0.5 - 198/500))

        circulo_vermelho1 = Circulo(27, config.Cores.VERMELHO, 0)
        circulo_vermelho1.posicao = Vector2(config.LARGURA * (0.5 + 270/1000), config.ALTURA *(0.5 - 198/500))

        formas = [[] for _ in range(6)]
        formas[1] = [circulo_branco]
        formas[2] = [circulo_vermelho]
        formas[5] = [circulo_vermelho1]


        super().__init__("TUTORIAL0", imagens,  "FASE00_", "INTRO0" , input_manager, legendas, pos_x, pos_y, largura_max, formas)

class Tutorial0_(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE0tutorial.png" for _ in range(3)
        ]
        legendas = "IntrosTutoriais/Tutoriais/Tutorial_0_.txt"
        pos_x = 150*config.LARGURA //1000
        pos_y = 90*config.ALTURA //1000
        largura_max = 740*config.LARGURA //1000

        formas = [[] for _ in range(2)]
 
        super().__init__("TUTORIAL0_", imagens, "FASE00_E0", "TUTORIAL0",input_manager, legendas, pos_x, pos_y, largura_max, formas)

class PosFase00(SlideShowBase):
    def __init__(self, input_manager):
        imagens = ["images/pos1FASE0jogo.png"] + ["images/pos2FASE0jogo.png" for _ in range(4)]
        legendas = "Posfase/Posfase_0.txt"
        pos_x = 455*config.LARGURA //1000
        pos_y = 180*config.ALTURA //1000
        largura_max = 380*config.LARGURA //1000
        formas = [[] for _ in range(5)]
        super().__init__("POSFASE00", imagens, "FASES", "TUTORIAL0_",input_manager, legendas, pos_x, pos_y, largura_max, formas)

class Intro1(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE1intro.png" for _ in range(7)
        ]
        legendas = "IntrosTutoriais/Introducoes/Introducao_1.txt"
        pos_x = 490*config.LARGURA //1000
        pos_y = 90*config.ALTURA //1000
        largura_max = 400*config.LARGURA //1000
        formas = [[] for _ in range(4)]
        super().__init__("INTRO1", imagens, "TUTORIAL1", "FASES",input_manager, legendas, pos_x, pos_y, largura_max, formas)

class Tutorial1(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE1tutorial.png" for _ in range(5)
        ]
        legendas = "IntrosTutoriais/Tutoriais/Tutorial_1.txt"
        pos_x = 200*config.LARGURA //1000
        pos_y = 90*config.ALTURA //1000
        largura_max = 650*config.LARGURA //1000

        triEqui = TrianguloEquilatero(130, config.Cores.AMARELO, 0)
        triEqui.posicao= Vector2(config.LARGURA *0.5 , config.ALTURA * (0.5 -20/500) )

        triIso = TrianguloIsoceles(140,80, config.Cores.AMARELO, 0)
        triIso.posicao = Vector2(config.LARGURA *0.5 , config.ALTURA * (0.5 - 40/500))

        triEsca = TrianguloRetangulo(105,140, config.Cores.AMARELO, 0)
        triEsca.posicao = Vector2(config.LARGURA *0.5 , config.ALTURA * (0.5 - 30/500))

        formas = [[] for _ in range(6)]
        formas[1] = [triEqui]
        formas[2] = [triIso]
        formas[3] = [triEsca]
 
        super().__init__("TUTORIAL1", imagens, "FASE01_E0", "INTRO1",input_manager, legendas, pos_x, pos_y, largura_max, formas)

class PosFase01(SlideShowBase):
    def __init__(self, input_manager):
        imagens = ["images/pos1FASE1jogo.png"] + ["images/pos2FASE1.png" for _ in range(5)]+["images/pos3FASE1.png"] 
        legendas = "Posfase/Posfase_1.txt"
        pos_x = 400*config.LARGURA //1000
        pos_y = 120*config.ALTURA //1000
        largura_max = 430*config.LARGURA //1000
        formas = [[] for _ in range(7)]
        super().__init__("POSFASE01", imagens, "FASES", "TUTORIAL1",input_manager, legendas, pos_x, pos_y, largura_max, formas)




