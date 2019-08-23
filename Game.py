from EngineClass import *
from DisplayClass import *
import pygame
import time

Score_Increment = 0.1
Width = 900
Height = 700
Tick_Time = 0.05


class Game:

    def __init__(self, n):
        self.paused = False

        self.ensemble = Ensemble(np.array([[Width], [Height]]))
        self.ensemble.populate(n)
        self.display = Display(self.ensemble)
        self.engine = Engine(self.ensemble)

        self.score = 0

        self.starting_bodies = 20

        self.ticks_per_new_body = 30

        self.ticks = 0

    # --------------------------- Getters and setters

    def get_ticks_per_new_body(self):
        return self.ticks_per_new_body

    def set_ticks_per_new_body(self, value):
        self.ticks_per_new_body = value

    def get_engine(self):
        return self.engine

    def get_ticks(self):
        return self.ticks

    def set_ticks(self, ticks):
        self.ticks = ticks

    def set_paused(self, bool):
        self.paused = bool

    def get_display(self):
        return self.display

    def get_paused(self):
        return self.paused

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def get_ensemble(self):
        return self.ensemble

    def get_starting_bodies(self):
        return self.starting_bodies

    # ----------------------------- Game functions

    def update_ticks_per_new_body(self):
        self.set_ticks_per_new_body(int(20 + 100 * 1.1 ** -self.get_ticks()))


    def update_score(self):
        inc = 0.1 * self.get_ticks() ** 0.1
        self.set_score(self.get_score() + inc)

    def tick(self):
        start_time = time.time()

        if self.paused:
            pass
        else:
            self.get_engine().tick()
            self.get_display().draw_game(int(self.get_score()))
            self.update_ticks_per_new_body()
            if self.get_ticks() % self.get_ticks_per_new_body() == 0:
                self.get_engine().get_ensemble().add_bodies_constant_mass(1, 4 * self.get_ticks() ** 0.15)
        self.update_score()
        self.set_ticks(self.get_ticks() + 1)

        end_time = time.time()
        time_remaining = Tick_Time + start_time - end_time
        if time_remaining > 0:
            time.sleep(time_remaining)

    def reset_game(self):
        self.get_ensemble().reset_ensemble(self.get_starting_bodies())
        self.set_score(0)

    def main_loop(self):
        self.reset_game()
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    break
            if self.get_ensemble().get_crashed():
                self.get_display().draw_game_over()
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.reset_game()
                    self.get_display().draw_game(int(self.get_score()))
            elif self.get_paused():
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.set_paused(False)
            else:
                self.tick()
                for event in events:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.set_paused(True)
        quit()

        





game = Game(20)

game.main_loop()
