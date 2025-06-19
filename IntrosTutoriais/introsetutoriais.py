import pygame

class SlideShowBase:
    def __init__(self, estado_name, imagens, proximo_estado, input_manager, legendas, x, y, largura_maxima):
        self.estado_name = estado_name
        self.imagens = [pygame.image.load(img).convert_alpha() for img in imagens]
        self.index = 0
        self.proximo_estado = proximo_estado
        self.input_manager = input_manager

        self.pos_x = x
        self.pos_y = y
        self.largura_maxima = largura_maxima
        self.fonte = pygame.font.Font("PressStart2P.ttf", 20) 
        self.texto_mostrado = ""        
        self.texto_index = 0            
        self.tempo_ultima_letra = 0     
        self.velocidade_texto = 35       
        self.legendas = self.carregar_legendas_em_blocos(legendas)

    def carregar_legendas_em_blocos(self, caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.read().split('\n\n')  # separa por parágrafos (linhas em branco)
            return [bloco.replace('\n', ' ') for bloco in linhas if bloco.strip()]

    def reset(self):
        self.index = 0
        self.texto_index = 0
        self.texto_mostrado = ""  
        self.tempo_ultima_letra = 0     

    def atualizar(self):
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
                tela.blit(superficie, (self.pos_x, self.pos_y + i * 28))  


class Intro0(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE0intro.png" for _ in range(2)
        ]
        legendas = "IntrosTutoriais/Introducoes/Introducao_0.txt"
        pos_x = 250
        pos_y = 40
        largura_max = 400  
        super().__init__("INTRO0", imagens, "TUTORIAL0", input_manager, legendas, pos_x, pos_y, largura_max)

class Tutorial0(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE0tutorial.png" for _ in range(6)
        ]
        legendas = "IntrosTutoriais/Tutoriais/Tutorial_0.txt"
        pos_x = 150
        pos_y = 90
        largura_max = 740  
        super().__init__("TUTORIAL0", imagens,  "FASE00_" , input_manager, legendas, pos_x, pos_y, largura_max)

class Tutorial0_(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE0tutorial.png" for _ in range(4)
        ]
        legendas = "IntrosTutoriais/Tutoriais/Tutorial_0_.txt"
        pos_x = 150
        pos_y = 90
        largura_max = 740  
        super().__init__("TUTORIAL0_", imagens, "FASE00", input_manager, legendas, pos_x, pos_y, largura_max)

class Intro1(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE1intro.png" for _ in range(4)
        ]
        legendas = "IntrosTutoriais/Introducoes/Introducao_1.txt"
        pos_x = 250
        pos_y = 40
        largura_max = 400  
        super().__init__("INTRO1", imagens, "TUTORIAL1", input_manager, legendas, pos_x, pos_y, largura_max)

class Tutorial1(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE1tutorial.png",
            "images/FASE1tutorial.png",
        ]
        legendas = "IntrosTutoriais/Tutoriais/Tutorial_1.txt"
        pos_x = 250
        pos_y = 40
        largura_max = 400  
        super().__init__("TUTORIAL1", imagens, "FASE01", input_manager, legendas, pos_x, pos_y, largura_max)