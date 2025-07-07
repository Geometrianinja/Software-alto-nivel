import pygame
from controller import *
import threading

class InputManager(Calibrattion):
    def __init__(self):
        self.controller = Controller()

        super().__init__()

        self.cont_back_pressed = False
        self.cont_back_just_pressed = False
        self.cont_select_pressed = False
        self.cont_select_just_pressed = False

        self.button_select_and_pressed = False

        self.cont_gyro = None
        self.cont_screen_pos = None
        self.cont_cut_start_pos = None


        self.controller_screen_pos_diff = [0, 0]

        self.quit_just_pressed = False
        self.mouse_left_pressed = False
        self.mouse_right_pressed = False
        self.mouse_left_just_pressed = False
        self.mouse_right_just_pressed = False
        self.mouse_pos: list[float] = [0, 0]
        self.mouse_diff: list[float] = [0, 0]

        self.Key_enter_pressed = False
        self.using_controller = False

        self.gyro = (0, 0, 0)

        self.last_time: float = 0.0
        self.dt: float = 0.0
        self.time: float = 0.0

    def update(self):
        self.time = time.time()
        self.dt = self.time - self.last_time  # Time elapsed since last frame in seconds
        self.last_time = self.time

        self.cont_back_just_pressed = False
        self.cont_select_just_pressed = False

        self.mouse_left_just_pressed = False
        self.mouse_right_just_pressed = False
        self.quit_just_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_just_pressed = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.mouse_left_pressed = True
                    self.mouse_left_just_pressed = True
                elif event.button == 3:  # Right mouse button
                    self.mouse_right_pressed = True
                    self.mouse_right_just_pressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    self.mouse_left_pressed = False
                elif event.button == 3:  # Right mouse button
                    self.mouse_right_pressed = False
                    
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                self.mouse_diff = [event.rel[0], event.rel[1]]

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_just_pressed = True
                elif event.key == pygame.K_RETURN:
                    self.Key_enter_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    self.Key_enter_pressed = False
            
            
        
        while self.using_controller:
            event = self.controller.get_event()

            if isinstance(event, GyroEvent):
                self.gyro = (event.yaw, event.pitch, event.roll)

            if isinstance(event, ButtonEvent):
                if event.button == ButtonID.BUTTON_BACK:
                    self.cont_back_pressed = True
                    self.cont_back_just_pressed = True
                elif event.button == ButtonID.BUTTON_SELECT and event.event_type == ButtonEventType.PRESSED:
                    self.cont_select_pressed = True
                    self.cont_select_just_pressed = True
                    self.button_select_and_pressed = True
                    self.cont_cut_start_pos = self.cont_screen_pos  # Salva a posição inicial do corte
                elif event.button == ButtonID.BUTTON_SELECT and event.event_type == ButtonEventType.RELEASED:
                    self.cont_select_pressed = False
                    self.button_select_and_pressed = False
                    self.cont_cut_start_pos = None  # Apenas reseta, não calcula diff aqui!
                else: 
                    self.button_select_and_pressed = False


            if self.controller.get_queue_size() < 5:
                break
        
        if self.calibrated:
            prev_cont_screen_pos = self.cont_screen_pos if self.cont_screen_pos is not None else None

            self.cont_screen_pos = self.get_point(self.gyro)

            if (
                prev_cont_screen_pos is not None
                and self.cont_screen_pos is not None
                and self.button_select_and_pressed  # Só atualiza se estiver pressionado
            ):
                self.controller_screen_pos_diff = [
                    self.cont_screen_pos[0] - prev_cont_screen_pos[0],
                    self.cont_screen_pos[1] - prev_cont_screen_pos[1]
                ]
            else:
                self.controller_screen_pos_diff = [0, 0]
