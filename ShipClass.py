import numpy as np
import math

Thrust_Constant = 0.5
Turn_Speed = 0.3  # in radians
Throttle_Speed = 0.03


class Ship:
    def __init__(self, pos):
        # pos is a np 2-vector
        self.angle = 0.0
        self.pos = pos
        self.vel = np.array([[0.0], [0.0]])
        self.acc = np.array([[0.0], [0.0]])
        self.throttle = 0.0
        self.direction_vec = np.array([[1.0], [0.0]])
        self.thrust = np.array([[0.0], [0.0]])
        self.max_throttle = 1

    # Getters and setters
    def get_max_throttle(self):
        return self.max_throttle
    def get_direction_vec(self):
        return self.direction_vec

    def set_direction_vec(self, direction_vec):
        self.direction_vec = direction_vec

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        # Set angle and calculate corresponding unit direction vector
        self.angle = angle
        self.set_direction_vec(np.array([[math.cos(angle)], [math.sin(angle)]]))

    def get_pos(self):
        return self.pos

    def set_pos(self, pos):
        self.pos = pos

    def get_vel(self):
        return self.vel

    def set_vel(self,vel):
        self.vel = vel

    def get_acc(self):
        return self.acc

    def set_acc(self, acc):
        self.acc = acc

    def get_thrust(self):
        return self.thrust

    def set_thrust(self, thrust):
        self.thrust = thrust

    def get_throttle(self):
        return self.throttle

    def set_throttle(self, throttle):
        self.throttle = throttle

        self.update_thrust()


    # Motion updates

    def update_vel(self):
        self.set_vel(self.get_vel() + self.get_acc())

    def update_pos(self):
        self.set_pos(self.get_pos() + self.get_vel())

    def update_thrust(self):
        self.set_thrust(self.get_throttle() * Thrust_Constant * self.get_direction_vec())

    # Controls

    def turn_left(self):
        self.set_angle(self.get_angle() - Turn_Speed)

    def turn_right(self):
        self.set_angle(self.get_angle() + Turn_Speed)

    def throttle_up(self):
        self.set_throttle(min(self.get_max_throttle(), self.get_throttle() + Throttle_Speed))

    def throttle_down(self):
        self.set_throttle(max(0, self.get_throttle() - Throttle_Speed))

    def full_throttle(self):
        self.set_throttle(self.get_max_throttle())

    def cut_throttle(self):
        self.set_throttle(0.0)

#Test:

a = Ship(np.array([[0], [0]]))

        
