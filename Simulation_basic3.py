import math
import numpy as np
from random import uniform
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

foods = []
population = []

settings = {}

settings['x_min'] = -2.0
settings['x_max'] = 2.0
settings['y_min'] = -2.0
settings['y_max'] = 2.0

settings['food_energy'] = 0.5
settings['food_number'] = 100
settings['food_drop'] = 0.05
settings['re_spawn_cycles'] = 30

settings['v_max'] = 0.05
settings['v_min'] = 0.01
settings['start_population'] = 100
settings['eating_distance'] = 0.05


def plot_simulation(foods, population):
    # "Clear axis"
    plt.cla()

    # Draw food
    X_food = []
    Y_food = []
    for i in range(len(foods)):
        X_food.append(foods[i].x_coord)
        Y_food.append(foods[i].y_coord)

    plt.plot(X_food, Y_food, linestyle='None', marker='.')

    # Draw "targeting rays"
    for org in population:
        plt.plot([org.food_at.x_coord, org.x_coord], [
            org.food_at.y_coord, org.y_coord], marker='x', linestyle=':', color='green')

    # Draw organisms
    X_organism = []
    Y_organism = []
    for i in range(len(population)):
        X_organism.append(population[i].x_coord)
        Y_organism.append(population[i].y_coord)

    plt.plot(X_organism, Y_organism, linestyle='None', marker='o')

    # last polish to plot
    plt.xlim(settings['x_min'], settings['x_max'])
    plt.ylim(settings['y_min'], settings['y_max'])
    plt.tight_layout()


def is_any_food(food_list):
    for i in food_list:
        if i.re_spawn_bool == False:
            return True
    return False


def simulate(settings, population, foods):
    # Organism Eats, if possible
    for food in foods:
        if food.re_spawn_bool == False:
            for org in population:
                food_to_organism_dist = org.calc_distance(food)
                # Eating
                # If the food is close enough, organism will eat food and re spawn it.
                if food_to_organism_dist <= org.velocity:
                    # Update organism
                    org.fitness += food.energy
                    org.x_coord = food.x_coord
                    org.y_coord = food.y_coord
                    org.near_food_distance = 100
                    # Update food
                    food.re_spawn_bool = True
                    food.temporarily_de_spawn()

    # Organism takes action
    for org in population:
        # Organism looks for nearest food
        # Reset nearest food distance
        org.near_food_distance = 100
        for food in foods:
            if food.re_spawn_bool == False:
                # Calculate distance for this piece of food
                food_to_organism_dist = org.calc_distance(food)
                # Check, if last food piece was closer than current
                if food_to_organism_dist < org.near_food_distance:
                    org.near_food_distance = food_to_organism_dist
                    # Memorize chosen food piece
                    org.food_at = food
        if org.food_at.re_spawn_bool == False:
            org.calc_next_heading(org.food_at)
        # Hunger
        org.fitness = round(org.fitness-(settings["food_drop"]), 4)
        # Starvation
        # Delete organism if it starve to death
        if org.fitness <= 0:
            del population[population.index(org)]
        # Move
        if is_any_food(food_list=foods):
            org.x_coord += org.velocity * math.cos(org.rotation)
            org.y_coord += org.velocity * math.sin(org.rotation)
        else:
            org.x_coord += uniform(-org.velocity, org.velocity)
            org.y_coord += uniform(-org.velocity, org.velocity)
        # Borders -> Delete organism, if it somehow hit borders
        if org.x_coord > settings['x_max'] or org.x_coord < settings['x_min'] or org.y_coord > settings['y_max'] or org.y_coord < settings['y_min']:
            del population[population.index(org)]

    plot_simulation(foods=foods, population=population)


def run(settings):
    # run() provide starting settings by generating randomly food and organism in plot.
    # Simulation take place in FuncAnimation(), so there is no need to loop this separated.

    # Food distribution
    for i in range(0, settings['food_number']):
        foods.append(food(settings=settings))

    # Organism distribution
    for i in range(settings['start_population']):
        population.append(organism(settings=settings))


def animate(i):
    simulate(settings=settings, population=population, foods=foods)
    for i in foods:
        i.try_re_spawn()


class organism():
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
        return math.sqrt((self.x_coord-target.x_coord)**2 + (self.y_coord-target.y_coord)**2)

    def calc_next_heading(self, target):
        self.rotation = math.atan2(
            target.y_coord - self.y_coord, target.x_coord - self.x_coord)


class food():
    def __init__(self, settings) -> None:
        self.x_coord = uniform(0.9*settings['x_min'], 0.9*settings['x_max'])
        self.y_coord = uniform(0.9*settings['y_min'], 0.9*settings['y_max'])
        self.energy = settings['food_energy']
        self.re_spawn_bool = False
        self.re_spawn_counter = 0

    def try_re_spawn(self):
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
        self.x_coord = np.nan
        self.y_coord = np.nan


run(settings=settings)
ani = FuncAnimation(plt.gcf(), animate, interval=50)
plt.show()
x = input("any key")
