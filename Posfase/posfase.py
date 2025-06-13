import pygame

class PosFaseSlideShow:
    def __init__(self, estado_name, imagens, input_manager, proximo_estado="FASES"):
        self.estado_name = estado_name
        self.imagens = [pygame.image.load(img).convert_alpha() for img in imagens]
        self.index = 0
        self.proximo_estado = proximo_estado
        self.input_manager = input_manager

    def atualizar(self):
        avancar = self.input_manager.mouse_left_just_pressed or self.input_manager.cont_select_just_pressed

        if avancar:
            if self.index < len(self.imagens) - 1:
                self.index += 1
            
            else:
            
                return self.proximo_estado
        return self.estado_name

    def desenhar(self, tela):
        tela.fill((0, 0, 0))
        if 0 <= self.index < len(self.imagens):
            img = pygame.transform.scale(self.imagens[self.index], tela.get_size())
            tela.blit(img, (0, 0))
    def reset(self):
        self.index = 0

# Pós-fase da Fase 0
class PosFase00(PosFaseSlideShow):
    def __init__(self, input_manager):
        imagens = [
            "images/pos1FASE0jogo.png",
            "images/pos2FASE0jogo.png",
         
        ]
        super().__init__("POSFASE00", imagens, input_manager, "FASES")


# Pós-fase da Fase 1
class PosFase01(PosFaseSlideShow):
    def __init__(self, input_manager):
        imagens = [
            "images/pos1FASE1jogo.png",
            "images/pos2FASE1jogo.png",
            
        ]
        super().__init__("POSFASE01", imagens, input_manager, "FASES")