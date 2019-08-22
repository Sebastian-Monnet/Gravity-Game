from EnsembleClass import *
import pygame
import time

class Engine:
    def __init__(self, ensemble):
        self.ensemble = ensemble
        self.paused = False
        self.game_over = False

    # ------------------- Getters and setters

    def set_ensemble(self, ensemble):
        self.ensemble = ensemble

    def get_ensemble(self):
        return self.ensemble

    def set_paused(self, bool):
        self.paused = bool

    def get_paused(self):
        return self.paused

    def set_game_over(self, bool):
        self.game_over = bool

    def get_game_over(self):
        if self.get_ensemble().get_crashed():
            self.set_game_over(True)
        return self.game_over

    # --------------------------- Keys

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.get_ensemble().get_ship().full_throttle()
        if keys[pygame.K_LCTRL]:
            self.get_ensemble().get_ship().throttle_down()
        if keys[pygame.K_LSHIFT]:
            self.get_ensemble().get_ship().throttle_up()
        if keys[pygame.K_x]:
            self.get_ensemble().get_ship().cut_throttle()
        if keys[pygame.K_LEFT]:
            self.get_ensemble().get_ship().turn_left()
        if keys[pygame.K_RIGHT]:
            self.get_ensemble().get_ship().turn_right()

    # ------------------------- Tick

    def tick(self):
        start_time = time.time()
        self.handle_keys()
        self.get_ensemble().tick()
        end_time = time.time()
        pygame.event.pump()
        time_remaining = Tick_Time + start_time - end_time
        if time_remaining > 0:
            time.sleep(time_remaining)



