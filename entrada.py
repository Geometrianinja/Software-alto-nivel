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
        self.cont_gyro = None
        self.cont_screen_pos = None

        self.quit_just_pressed = False
        self.mouse_left_pressed = False
        self.mouse_right_pressed = False
        self.mouse_left_just_pressed = False
        self.mouse_right_just_pressed = False
        self.mouse_pos = [0, 0]
        
        self.Key_enter_pressed = False
        self.using_controller = False

        self.gyro = (0, 0, 0)

    def update(self):
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
                else: 
                    self.button_select_and_pressed = False


            if self.controller.get_queue_size() < 5:
                break
        
        if self.calibrated:
            self.cont_screen_pos = self.get_point(self.gyro)
    