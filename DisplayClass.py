import pygame
from EnsembleClass import *
import threading
import time

Ship_Colour = (255, 255, 255)
Body_Colour = (255, 255, 255)
Ship_Radius = 10
Line_Length = 15


class Display:
    def __init__(self, ensemble):
        self.ensemble = ensemble
        self.width = ensemble.dims[0][0]
        self.height = ensemble.dims[1][0]
        self.screen = pygame.display.set_mode((self.width, self.height))

    def get_ensemble(self):
        return self.ensemble

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_screen(self):
        return self.screen

    def draw_ship(self):
        ship = self.get_ensemble().get_ship()
        pos_vec = ship.get_pos()
        direction_vec = ship.get_direction_vec()
        
        pos_tup = (int(pos_vec[0][0]), int(pos_vec[1][0]))
        
        line_end_vec = pos_vec - Line_Length * direction_vec
        line_end_tup = (int(line_end_vec[0][0]), int(line_end_vec[1][0]))
        pygame.draw.circle(self.get_screen(), Ship_Colour, pos_tup, int(Ship_Radius), 1)
        pygame.draw.line(self.get_screen(), Ship_Colour, pos_tup, line_end_tup)

    def draw_body(self, body):
        pos_vec = body.get_pos()
        pos_tup = (int(pos_vec[0][0]), int(pos_vec[1][0]))

        radius = int(body.get_radius())

        pygame.draw.circle(self.get_screen(), Body_Colour, pos_tup, radius, 1)

    def draw_all_bodies(self):
        bodies = self.ensemble.get_bodies()
        for body in bodies:
            self.draw_body(body)

    def draw_ensemble(self):
        pygame.draw.rect(self.get_screen(), (0, 0, 0), (0, 0, self.get_ensemble().get_dims()[0][0], self.get_ensemble().get_dims()[1][0]))
        self.draw_all_bodies()
        self.draw_ship()
        pygame.display.flip()




