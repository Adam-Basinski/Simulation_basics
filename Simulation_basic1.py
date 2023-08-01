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
settings['food_drop'] = 0.1

settings['v_max'] = 0.05
settings['v_min'] = 0.01
settings['start_population'] = 50
settings['eating_distance'] = 0.05

def calc_distance(org_x, org_y, food_x, food_y):
    return math.sqrt((org_x-food_x)**2 + (org_y-food_y)**2)


def plot_simulation(foods, population):
    # "Clear axis"
    plt.cla()

    # Creating food and organisms axis
    X_food = []
    Y_food = []
    X_organism = []
    Y_organism = []
    for i in range(len(foods)):
        X_food.append(foods[i].x_coord)
        Y_food.append(foods[i].y_coord)

    for i in range(len(population)):
        X_organism.append(population[i].x_coord)
        Y_organism.append(population[i].y_coord)

    # Draw food
    plt.plot(X_food, Y_food, linestyle='None', marker='.')

    # Draw "targeting rays" 
    for org in population:
        plt.plot([org.food_at.x_coord, org.x_coord], [
                 org.food_at.y_coord, org.y_coord], marker='x', linestyle=':', color='green')
        
    # Draw organisms
    plt.plot(X_organism, Y_organism, linestyle='None', marker='o')

    # last polish to plot
    plt.xlim(settings['x_min'], settings['x_max'])
    plt.ylim(settings['y_min'], settings['y_max'])
    plt.tight_layout()


def calc_next_heading(organism, target):
    # Takes turn toward food
    diff_x = target.x_coord - organism.x_coord
    diff_y = target.y_coord - organism.y_coord
    theta = math.atan2(diff_y, diff_x)
    return theta


def simulate(settings, population, foods):

# Organism Eats, if possible
    for food in foods:
        for org in population:
            food_to_organism_dist = calc_distance(
                org.x_coord, org.y_coord, food.x_coord, food.y_coord)
            # Eating
            # If the food is close enough, organism will eat food and re spawn it.
            if food_to_organism_dist <= org.velocity:
                # Update organism
                org.fitness += food.energy
                org.x_coord = food.x_coord
                org.y_coord = food.y_coord
                org.near_food_distance = 100
                # Update food
                food.re_spawn_food(settings)
                

# Organism takes action
    for org in population:
        # Organism looks for nearest food
        # Reset nearest food distance
        org.near_food_distance = 100
        for food in foods:
            # Calculate distance for this piece of food
            food_to_organism_dist = calc_distance(
                org.x_coord, org.y_coord, food.x_coord, food.y_coord)
            # Check, if last food piece was closer than current
            if food_to_organism_dist < org.near_food_distance:
                org.near_food_distance = food_to_organism_dist
                # Memorize chosen food piece 
                org.food_at = food
        org.rotation = calc_next_heading(org, org.food_at)
        # Hunger
        org.fitness = round(org.fitness-(settings["food_drop"]), 4)
        # Starvation
        # Delete organism if it starve to death
        if org.fitness <= 0:
            del population[population.index(org)]
        # Move
        org.x_coord += org.velocity * math.cos(org.rotation)
        org.y_coord += org.velocity * math.sin(org.rotation)
        # Borders
        # Delete organism, if it somehow hit borders
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

    def data_organism(Self):

        pass


class food():
    def __init__(self, settings) -> None:
        self.x_coord = uniform(0.9*settings['x_min'], 0.9*settings['x_max'])
        self.y_coord = uniform(0.9*settings['y_min'], 0.9*settings['y_max'])
        self.energy = settings['food_energy']

    def re_spawn_food(self, settings):
        self.x_coord = uniform(0.9*settings['x_min'], 0.9*settings['x_max'])
        self.y_coord = uniform(0.9*settings['y_min'], 0.9*settings['y_max'])


run(settings=settings)
ani = FuncAnimation(plt.gcf(), animate, interval=50)
plt.show()
x = input("any key")
