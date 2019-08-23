import pygame
from EnsembleClass import *

Ship_Colour = (255, 0, 0)
Body_Colour = (255, 255, 255)
Ship_Radius = 10
Line_Length = 15

pygame.init()

class Display:
    def __init__(self, ensemble):
        self.ensemble = ensemble
        self.width = ensemble.dims[0][0]
        self.height = ensemble.dims[1][0]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.score_font = pygame.font.SysFont('arial', 20)
        self.title_font = pygame.font.SysFont('arial', 25)
        self.title_font.set_underline(True)

    def get_ensemble(self):
        return self.ensemble

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_screen(self):
        return self.screen

    def get_score_font(self):
        return self.score_font

    def get_title_font(self):
        return self.title_font

    def draw_one_ship(self, x_pos, y_pos, angle):
        centre = (x_pos, y_pos)
        tip = (x_pos + Ship_Radius * math.cos(angle), y_pos + Ship_Radius * math.sin(angle))
        right_corner = (x_pos + Ship_Radius * math.cos(angle - 2 * math.pi / 3), y_pos + Ship_Radius *
                       math.sin(angle - 2 * math.pi / 3))
        left_corner = (x_pos + Ship_Radius * math.cos(2 * math.pi / 3 + angle), y_pos + Ship_Radius *
                       math.sin(2 * math.pi / 3 + angle))

        pygame.draw.circle(self.get_screen(), Ship_Colour, (x_pos, y_pos), Ship_Radius, 1)

        pygame.draw.polygon(self.get_screen(), Ship_Colour, (centre, right_corner, tip, left_corner))


    def draw_ship(self):
        ship = self.get_ensemble().get_ship()
        pos_vec = ship.get_pos()
        direction_vec = ship.get_direction_vec()

        (w, h) = (self.get_ensemble().get_dims()[0][0], self.get_ensemble().get_dims()[1][0])
        (x, y) = (int(pos_vec[0][0]), int(pos_vec[1][0]))
        
        line_end_vec = pos_vec - Line_Length * direction_vec
        (line_x, line_y) = (int(line_end_vec[0][0]), int(line_end_vec[1][0]))
        for i in range(3):
            for j in range(3):
                self.draw_one_ship(x + (i - 1) * w, y + (j - 1) * h, self.get_ensemble().get_ship().get_angle())

    def draw_body(self, body):
        pos_vec = body.get_pos()

        (w, h) = (self.get_ensemble().get_dims()[0][0], self.get_ensemble().get_dims()[1][0])
        (x, y) = (int(pos_vec[0][0]), int(pos_vec[1][0]))

        radius = int(body.get_radius())
        for i in range(3):
            for j in range(3):
                pygame.draw.circle(self.get_screen(), Body_Colour, (x + (i-1) * w, y + (j-1) * h), radius, 1)

    def draw_all_bodies(self):
        bodies = self.ensemble.get_bodies()
        for body in bodies:
            self.draw_body(body)

    def draw_score(self, score):
        text = self.get_score_font().render("Score: " + str(score), True, (255, 255, 255))
        text_rect = text.get_rect()

        size = self.get_score_font().size("Score: " + str(score))

        text_rect.center = (5 + size[0] / 2, 5 + size[1] / 2)
        self.get_screen().blit(text, text_rect)

    def draw_instructions(self):
        title = self.get_title_font().render("How To Play", True, (255, 255, 255))
        title_rect = title.get_rect()
        title_size = self.get_title_font().size("How To Play")

        w = self.get_ensemble().get_dims()[0][0]

        title_rect.center = (w - title_size[0] / 2 - 5, title_size[1] / 2 + 5)

        self.get_screen().blit(title, title_rect)

        lines = []

        lines.append("Space: Play/Pause/New Game")
        lines.append("z: Full Throttle")
        lines.append("x: Cut Throttle")
        lines.append("L_SHIFT: Increase Throttle")
        lines.append("CTRL: Decrease Throttle")

        for i in range(5):
            line = lines[i]
            text = self.get_score_font().render(line, True, (255, 255, 255))
            rect = text.get_rect()
            size = self.get_score_font().size(line)

            rect.center = (w - size[0] / 2 - 5, (i+2) * size[1]  + 5)
            self.get_screen().blit(text, rect)

    def draw_throttle(self, current_throttle, max_throttle):
        dims = self.get_ensemble().get_dims()
        w = dims[0][0]
        h = dims[1][0]

        rect_width = 80
        rect_height = 20

        pygame.draw.rect(self.get_screen(), (255, 255, 255), ((w - rect_width) / 2, h - rect_height - 30, rect_width,
                                                              rect_height), 1)

        throttle_rect_width = current_throttle / max_throttle * rect_width - 2

        pygame.draw.rect(self.get_screen(), (255, 0, 0), ((w - rect_width) / 2 + 1,
                                            h - rect_height - 28, throttle_rect_width, rect_height - 4))

        text = self.get_score_font().render("Throttle", True, (255, 255, 255))
        rect = text.get_rect()
        size = self.get_score_font().size("Throttle")
        rect.center = (w / 2, h - size[1]/2 - 5)

        self.get_screen().blit(text, rect)

    def draw_game_over(self):
        dims = self.get_ensemble().get_dims()
        w = dims[0][0]
        h = dims[1][0]
        font = pygame.font.SysFont('arial', 50)
        font.set_bold(True)

        text = font.render("Game Over!", True, (255, 255, 255))
        rect = text.get_rect()
        rect.center = (w / 2, h / 2 - 20)
        self.get_screen().blit(text, rect)

        text = self.get_score_font().render("Press SPACE to restart", True, (255, 255, 255))
        rect = text.get_rect()
        rect.center = (w / 2, h / 2 + 20)
        self.get_screen().blit(text, rect)



        pygame.display.update()

    def draw_game(self, score):
        pygame.draw.rect(self.get_screen(), (0, 0, 0),
                         (0, 0, self.get_ensemble().get_dims()[0][0], self.get_ensemble().get_dims()[1][0]))
        self.draw_all_bodies()
        self.draw_ship()
        self.draw_score(score)
        self.draw_instructions()
        self.draw_throttle(self.get_ensemble().get_ship().get_throttle(),
                           self.get_ensemble().get_ship().get_max_throttle())
        pygame.display.update()









