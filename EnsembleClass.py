import numpy as np
import math
from BodyClass import *
import random
from ShipClass import *
import time

Top_Speed = 3
G = 0.1
Ship_Grav_Coeff = 100
Restitution = 0.9
Max_Body_Radius = 20
Min_Body_Radius = 10
Ship_Radius = 10
Grav_Exponent = 2
Tick_Time = 0.05

class Ensemble:
    def __init__(self, dims):
        # n is the number of bodies. dims is the dimensions of the screen in a numpy vector
        self.dims = dims
        self.ship = Ship(dims * 0.5)
        self.bodies = []
        self.crashed = False

    # ---------------------- getters and setters

    def set_bodies(self, bodies):
        self.bodies = bodies

    def get_bodies(self):
        return self.bodies

    def get_ship(self):
        return self.ship

    def get_dims(self):
        return self.dims

    def remove_body(self, index):
        self.get_bodies().pop(index)

    def add_body(self, body):
        self.get_bodies().append(body)

    def set_crashed(self, bool):
        self.crashed = bool

    def get_crashed(self):
        return self.crashed

    # ------------------------------- Populate the map with bodies

    def is_too_close_to_body(self, new_pos, new_radius):
        # returns True if the new coordinates are too close to an existing body, False otherwise
        for body in self.bodies:
            if max(abs(new_pos[0][0] - body.get_pos()[0][0]),
                   abs(new_pos[1][0] - body.get_pos()[1][0])) < new_radius + body.get_radius():
                return True
        return False

    def is_too_close_to_ship(self, new_pos, new_r):
        # Returns True if the new coordinates are too close to the ship
        pos_x = new_pos[0][0]
        pos_y = new_pos[1][0]
        w = self.get_dims()[0][0]
        h = self.get_dims()[1][0]
        if pos_x + new_r < w / 3 or pos_x - new_r > 2 * w / 3 or pos_y + new_r < h / 3 or pos_y - new_r > 2 * h / 3:
            return False
        return True

    def is_pos_valid(self, new_pos, new_radius):
        # Returns True if new_pos is not too close to anything, and False otherwise
        if self.is_too_close_to_body(new_pos, new_radius) or self.is_too_close_to_ship(new_pos, new_radius):
            return False
        return True

    def get_new_pos(self, new_radius):
        # Generates a random position on the screen
        while True:
            new_radius = int(new_radius)
            new_x = random.randint(new_radius, self.get_dims()[0][0] - new_radius - 1)
            new_y = random.randint(new_radius, self.get_dims()[1][0] - new_radius - 1)
            new_pos = np.array([[new_x],[new_y]])
            if self.is_pos_valid(new_pos, new_radius):
                return new_pos

    def get_new_vel(self):
        # Generates a velocity vector in a random direction and of random magnitude
        speed = random.uniform(0, Top_Speed)
        angle = random.uniform(0, 2 * math.pi)

        return np.array([[speed * math.cos(angle)], [speed * math.sin(angle)]])

    def populate(self, n):
        # Places n bodies that do not intersect and are not close to the ship
        for i in range(n):
            new_radius = random.uniform(Min_Body_Radius, Max_Body_Radius)
            new_pos = self.get_new_pos(new_radius)
            new_vel = self.get_new_vel()
            new_body = Body(new_pos, new_vel, new_radius)

            self.add_body(new_body)

    # ------------------------------------Calculate acceleration

    def get_shortest_displacement (self, pos_1, pos_2):
        # Assuming a torus-shaped universe, returns the shortest path from pos_1 to pos_2 under some weird distortion of
        # surface distance

        w = self.get_dims()[0][0]
        h = self.get_dims()[1][0]

        naive_x_disp = pos_2[0][0] - pos_1[0][0]
        naive_y_disp = pos_2[1][0] - pos_1[1][0]

        if naive_x_disp > w / 2:
            x_disp = naive_x_disp - w
        elif naive_x_disp > - w / 2:
            x_disp = naive_x_disp
        else:
            x_disp = naive_x_disp + w

        if naive_y_disp > h / 2:
            y_disp = naive_y_disp - h
        elif naive_y_disp > - h / 2:
            y_disp = naive_y_disp
        else:
            y_disp = naive_y_disp + h

        return np.array([[x_disp], [y_disp]])

    def get_acc_from(self, pos):
        # Returns the acceleration due to gravity of a particle at pos
        bodies = self.get_bodies()
        total_acc_vec = np.array([[0], [0]])
        for body in bodies:
            if np.linalg.norm(pos - body.get_pos()) < Min_Body_Radius:
                continue
            else:
                displacement = self.get_shortest_displacement(pos, body.get_pos())
                distance = np.linalg.norm(displacement)
                contribution_magnitude = G * body.get_mass() / distance ** Grav_Exponent

                unit_vec = displacement / distance

                total_acc_vec = total_acc_vec + unit_vec * contribution_magnitude
        return total_acc_vec

    def update_body_acc(self):
        # Updates acceleration of the bodies
        for body in self.get_bodies():
            acc = self.get_acc_from(body.get_pos())
            body.set_acc(acc)

    def update_ship_acc(self):
        # Updates acceleration of the ship or reflects it off a body
        acc = self.get_acc_from(self.get_ship().get_pos())
        self.get_ship().set_acc(self.get_ship().get_thrust() + Ship_Grav_Coeff * acc)

    # ----------------------------------- Torus universe

    def teleport(self, thing):
        # Thing is a body or a ship. Facilitates the wrap-around of the torus
        pos = thing.get_pos()
        x = pos[0][0]
        y = pos[1][0]
        dims = self.get_dims()
        w = dims[0][0]
        h = dims[1][0]
        if x > w:
            thing.set_pos(np.array([[x - w], [y]]))
        elif x < 0:
            thing.set_pos(np.array([[x + w], [y]]))
        if y > h:
            thing.set_pos(np.array([[x], [y - h]]))
        elif y < 0:
            thing.set_pos(np.array([[x], [y + h]]))

    def teleport_all(self):
        for body in self.get_bodies():
            self.teleport(body)
        self.teleport(self.get_ship())

    # --------------------------------- Coalesce

    def is_collided(self, body_1, body_2):
        # Takes two objects (ship or body) as arguments and returns True if they intersect, and False if not
        return np.linalg.norm(body_1.get_pos() - body_2.get_pos()) <= body_1.get_radius() + body_2.get_radius()

    def get_collided_bodies(self):
        # Returns a list of 2-lists containing all the pairs of collided bodies
        collided_indices = []
        bodies = self.get_bodies()
        n = len(self.get_bodies())
        for i in range(n):
            for j in range(i):
                if self.is_collided(bodies[i], bodies[j]):
                    collided_indices.append([i,j])
        return collided_indices

    def coalesce_bodies(self, index_1, index_2):
        # Combines two bodies, conserving mass and momentum. Index_1 must be greater than index_2
        bodies = self.get_bodies()
        body_1 = bodies[index_1]
        body_2 = bodies[index_2]

        total_mass = body_1.get_mass() + body_2.get_mass()
        centre_of_mass = (body_1.get_pos() * body_1.get_mass() + body_2.get_pos() * body_2.get_mass()) / total_mass

        momentum = body_1.get_vel() * body_1.get_mass() + body_2.get_vel() * body_2.get_mass()

        new_velocity = momentum / total_mass

        new_body = Body(centre_of_mass, new_velocity, 1)
        new_body.set_mass(total_mass)

        self.remove_body(index_1)
        self.remove_body(index_2)

        self.add_body(new_body)

    # -------------------------- Crash
    def is_near_body(self, ship, body):
        # Returns True if the ship is near the body, but not necessarily touching it (computationally faster than
        # calculating distance straight away)
        ship_pos = ship.get_pos()
        x_ship = ship_pos[0][0]
        y_ship = ship_pos[1][0]

        body_pos = body.get_pos()
        x_body = body_pos[0][0]
        y_body = body_pos[1][0]

        safe_distance = Ship_Radius + body.get_radius()

        if abs(x_body - x_ship) < safe_distance and abs(y_body - y_ship) < safe_distance:
            return True
        return False

    def is_touching_ship(self, body):
        # Returns True if the ship actually intersects the body
        ship = self.get_ship()
        return np.linalg.norm(
            self.get_shortest_displacement(body.get_pos(), ship.get_pos())) <= Ship_Radius + body.get_radius()

    def get_bodies_touching_ship(self):
        # Returns a list containing all bodies touching the ship
        bodies_touching_ship = []
        for body in self.get_bodies():
            if self.is_touching_ship(body):
                bodies_touching_ship.append(body)
        return bodies_touching_ship




    def tick(self):

        self.update_body_acc()
        self.update_ship_acc()
        for body in self.get_bodies():
            body.update_vel()
            body.update_pos()
        ship = self.get_ship()
        ship.update_vel()
        ship.update_pos()
        self.teleport_all()
        collided_bodies = self.get_collided_bodies()
        while collided_bodies:
            self.coalesce_bodies(collided_bodies[0][0], collided_bodies[0][1])
            collided_bodies = self.get_collided_bodies()
        if self.get_bodies_touching_ship():
            self.set_crashed(True)





