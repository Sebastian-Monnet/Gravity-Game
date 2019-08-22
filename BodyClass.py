import numpy as np
import math
import copy

Density = 0.1


class Body:
    def __init__(self, pos, vel, radius):
        # Sets values of attributes. pos and vel are numpy 2-vectors; mass and radius are floats
        self.pos = pos
        self.set_radius(radius)
        self.vel = vel
        self.acc = np.array([[0], [0]])

    # Getters and setters
    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def set_vel(self, vel):
        self.vel = vel

    def get_vel(self):
        return self.vel

    def set_acc(self, acc):
        self.acc = acc

    def get_acc(self):
        return self.acc

    def get_mass(self):
        return self.mass

    def set_mass(self, mass):
        self.mass = mass
        self.radius = (mass / Density) ** 0.5

    def get_radius(self):
        return self.radius

    def set_radius(self, radius):
        self.radius = radius
        self.mass = Density * radius ** 2

    # Motion

    def update_vel(self):
        # Add acceleration to velocity
        self.set_vel(self.get_vel() + self.get_acc())

    def update_pos(self):
        # Add velocity to position
        self.set_pos(self.get_pos() + self.get_vel())

    def add_to_acc(self, del_acc):
        self.set_acc(self.get_acc() + del_acc)

    # Calculate mass proportional to area

    def calculate_mass(self):
        return Density * self.radius ** 2


# Test stuff:

pos = np.array([[1], [0]])
vel = np.array([[0], [1]])
radius = 1

a = Body(pos, vel, radius)
