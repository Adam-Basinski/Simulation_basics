import Organisms                                # Separated lib with organisms
import matplotlib.pyplot as plt
from simulation_settings import settings        # Separated settings file
from matplotlib.animation import FuncAnimation  # To animate and run simulation
from random import uniform
from math import cos, sin

foods = []
population = []


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
        if len(population) <= 10:
            plt.text(org.x_coord, org.y_coord, org.fitness)

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
            org.x_coord += org.velocity * cos(org.rotation)
            org.y_coord += org.velocity * sin(org.rotation)
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
        foods.append(Organisms.Food(settings=settings))

    # Organism distribution
    for i in range(settings['start_population']):
        population.append(Organisms.Organism1(settings=settings))


def animate(i):
    simulate(settings=settings, population=population, foods=foods)
    for food in foods:
        food.try_re_spawn(settings)


run(settings=settings)
ani = FuncAnimation(plt.gcf(), animate, interval=50)
plt.show()
x = input("any key")
