import pygame

class SlideShowBase:
    def __init__(self, estado_name, imagens, proximo_estado, input_manager):
        self.estado_name = estado_name
        self.imagens = [pygame.image.load(img).convert_alpha() for img in imagens]
        self.index = 0
        self.proximo_estado = proximo_estado
        self.input_manager = input_manager

    def reset(self):
        self.index = 0

    def atualizar(self):
        avancar = self.input_manager.mouse_left_just_pressed or self.input_manager.cont_select_just_pressed
        if avancar:
            if self.index < len(self.imagens) - 1:
                self.index += 1
            else:
                return self.proximo_estado
        return self.estado_name

    def desenhar(self, tela):
        tela.fill((0,0,0))
        if self.index < len(self.imagens):
            img = pygame.transform.scale(self.imagens[self.index], tela.get_size())
            tela.blit(img, (0,0))

class Intro0(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE0intro.png",
            "images/FASE0intro.png",
        ]
        super().__init__("INTRO0", imagens, "TUTORIAL0", input_manager)

class Tutorial0(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE0tutorial.png",
            "images/FASE0tutorial.png",
        ]
        super().__init__("TUTORIAL0", imagens, "FASE00", input_manager)

class Intro1(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE1intro.png",
            "images/FASE1intro.png",
        ]
        super().__init__("INTRO1", imagens, "TUTORIAL1", input_manager)

class Tutorial1(SlideShowBase):
    def __init__(self, input_manager):
        imagens = [
            "images/FASE1tutorial.png",
            "images/FASE1tutorial.png",
        ]
        super().__init__("TUTORIAL1", imagens, "FASE01", input_manager)