import Organisms                                # Separated lib with organisms
import matplotlib.pyplot as plt
from simulation_settings import settings        # Separated settings file
from matplotlib.animation import FuncAnimation  # To animate and run simulation

foods = []
population = []

# Just test for git mod.


def plot_simulation(foods, population):
    # "Clear axis"
    plt.cla()

    # Draw food
    X_food = []
    Y_food = []
    for i in range(len(foods)):
        X_food.append(foods[i].x_coord)
        Y_food.append(foods[i].y_coord)

    plt.plot(X_food, Y_food, linestyle='None', marker='.', color='black')

    # Draw "targeting rays"
    for org in population:
        plt.plot([org.target.x_coord, org.x_coord], [
            org.target.y_coord, org.y_coord], marker='x', linestyle=':', color='green')
        if len(population) <= 20:
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
                # Eating
                # If the food is close enough, organism will eat food and re spawn it.
                if org.calc_distance(food) <= org.velocity:
                    # Update organism
                    org.fitness += food.energy
                    org.x_coord = food.x_coord
                    org.y_coord = food.y_coord
                    org.near_target_distance = 100
                    # Update food
                    food.re_spawn_bool = True
                    food.temporarily_de_spawn()

    # Organism produce offspring
    for org in population:
        # Check if organism is ready to mate
        if org.readyToMate and org.target.readyToMate:
            # If distance is small enough, produce offspring
            if org.calc_distance(org.target) <= org.velocity:
                # Append population with new offspring
                population.append(Organisms.Organism1(settings=settings))
                # Modify position and perks (velocity) based on parents perks
                population[-1].modify_offspring(org, org.target)
                # Making those 2 organisms no longer ready to mate
                org.target.fitness = round(org.target.fitness/2, 2)
                org.target.readyToMate = False
                org.fitness = round(org.fitness/2, 2)
                org.readyToMate = False

    # Organism takes action
    for org in population:
        # Hunger
        org.fitness = round(org.fitness-(settings["food_drop"]), 4)

        # Starvation ---- Delete organism if it starve to death
        if org.fitness <= 0:
            del population[population.index(org)]

        # Mating search
        org.is_ready_to_mate(settings, population)

        # Organism is looking for nearest food
        if not org.readyToMate:
            org.look_for_food(foods)

        # Organism is looking for mate partner
        else:
            org.look_for_mate(population)

        # Move
        org.calc_next_heading(org.target)
        org.move_org((is_any_food(food_list=foods) or org.readyToMate))

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
    print(len(population))


run(settings=settings)
ani = FuncAnimation(plt.gcf(), animate, interval=2)
plt.show()
x = input("any key")
