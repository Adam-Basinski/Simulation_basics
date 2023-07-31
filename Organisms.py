from random import uniform
from math import sqrt, atan2, cos, sin
from numpy import nan


class Organism1():
    def __init__(self, settings, name=None) -> None:

        self.x_coord = uniform(settings['x_min'], settings['x_max'])
        self.y_coord = uniform(settings['y_min'], settings['y_max'])

        self.rotation = uniform(0, 360)
        self.velocity = uniform(settings['v_min'], settings['v_max'])

        self.rotation = 0
        self.fitness = 5
        self.near_food_distance = 100

        self.name = name

    def calc_distance(self, target):
        return sqrt((self.x_coord-target.x_coord)**2 + (self.y_coord-target.y_coord)**2)

    def calc_next_heading(self, target):
        self.rotation = atan2(
            target.y_coord - self.y_coord, target.x_coord - self.x_coord)

    def move_org(self, isAnyTarget):
        if isAnyTarget:
            self.x_coord += self.velocity * cos(self.rotation)
            self.y_coord += self.velocity * sin(self.rotation)
        else:
            self.x_coord += uniform(-self.velocity, self.velocity)
            self.y_coord += uniform(-self.velocity, self.velocity)


class Food():
    def __init__(self, settings) -> None:
        self.x_coord = uniform(0.9*settings['x_min'], 0.9*settings['x_max'])
        self.y_coord = uniform(0.9*settings['y_min'], 0.9*settings['y_max'])
        self.energy = settings['food_energy']
        self.re_spawn_bool = False
        self.re_spawn_counter = 0

    def try_re_spawn(self, settings):
        if self.re_spawn_bool == True:
            self.re_spawn_counter += 1
            if self.re_spawn_counter >= settings['re_spawn_cycles']:
                self.re_spawn_food(settings=settings)
                self.re_spawn_bool = False
                self.re_spawn_counter = 0

    def re_spawn_food(self, settings):
        self.x_coord = uniform(0.9*settings['x_min'], 0.9*settings['x_max'])
        self.y_coord = uniform(0.9*settings['y_min'], 0.9*settings['y_max'])

    def temporarily_de_spawn(self):
        self.x_coord = nan
        self.y_coord = nan
