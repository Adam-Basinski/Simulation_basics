from random import uniform, choice
from math import sqrt, atan2, cos, sin
from numpy import nan


class Organism1():
    def __init__(self, settings: dict, name: str = None) -> None:
        # Position
        self.x_coord = uniform(settings['x_min'], settings['x_max'])
        self.y_coord = uniform(settings['y_min'], settings['y_max'])
        # Perks
        self.velocity = uniform(settings['v_min'], settings['v_max'])
        # Rest properties
        self.rotation = 0
        self.fitness = 10
        self.near_target_distance = 100
        self.readyToMate = False

        self.name = name

    def modify_offspring(self, parent1: object, parent2: object) -> None:
        # Position
        self.x_coord = parent1.x_coord
        self.y_coord = parent2.y_coord

        # Perks
        self.velocity = uniform(parent1.velocity, parent2.velocity)
        self.fitness = round(
            (parent1.target.fitness/2 + parent2.target.fitness/2)/2, 2)

    def calc_distance(self, target: object) -> float:
        """calculate distance to target."""
        return sqrt((self.x_coord-target.x_coord)**2 + (self.y_coord-target.y_coord)**2)

    def calc_next_heading(self, target: object) -> None:
        """Rotate organism to target."""
        self.rotation = atan2(
            target.y_coord - self.y_coord, target.x_coord - self.x_coord)

    def move_org(self, isAnyTarget: bool) -> None:
        """Organism move based of .velocity and .rotation. If there are no target, organism move in random direction."""
        if isAnyTarget:
            self.x_coord += self.velocity * cos(self.rotation)
            self.y_coord += self.velocity * sin(self.rotation)
        else:
            # Random direction if there aren't any target
            self.x_coord += uniform(-self.velocity, self.velocity)
            self.y_coord += uniform(-self.velocity, self.velocity)

    def is_ready_to_mate(self, settings: dict, population: list) -> None:
        """Check if organism is ready to mate.
        Change .readyToMate from False to True, if 2* minimum fitness required to looking for mating partner.
        Change it back to False, if fitness is less than minimum."""
        if self.fitness >= 2*settings['mate_search_fitness']:
            for organism in population:
                if (organism != self and organism.fitness >= 2*settings['mate_search_fitness']):
                    self.readyToMate = True
        if self.readyToMate and (self.fitness < settings['mate_search_fitness']):
            self.readyToMate = False

    def look_for_food(self, food_list: list) -> None:
        # Reset nearest food distance
        self.near_target_distance = 100
        for food in food_list:
            if food.re_spawn_bool == False:
                # Calculate distance for this piece of food
                food_to_organism_dist = self.calc_distance(food)
                # Check, if last food piece was closer than current
                if food_to_organism_dist < self.near_target_distance:
                    self.near_target_distance = food_to_organism_dist
                    # Memorize chosen food piece
                    # There are no .target in init
                    self.target = food

    def look_for_mate(self, population: list) -> None:
        # Work mostly the same to above
        # Reset the nearest mate distance
        self.near_target_distance = 100
        for potential_org in population:
                # check if organism isn't looking for himself
            if self != potential_org:
                mate_to_organism_dist = self.calc_distance(potential_org)
                if mate_to_organism_dist < self.near_target_distance:
                    self.near_target_distance = mate_to_organism_dist
                    self.target = potential_org

class Food():
    def __init__(self, settings: dict) -> None:
        self.x_coord = uniform(0.9*settings['x_min'], 0.9*settings['x_max'])
        self.y_coord = uniform(0.9*settings['y_min'], 0.9*settings['y_max'])
        self.energy = settings['food_energy']
        self.re_spawn_bool = False
        self.re_spawn_counter = 0
        self.readyToMate = False

    def try_re_spawn(self, settings: dict) -> None:
        if self.re_spawn_bool == True:
            self.re_spawn_counter += 1
            if self.re_spawn_counter >= settings['re_spawn_cycles']:
                self.re_spawn_food(settings=settings)
                self.re_spawn_bool = False
                self.re_spawn_counter = 0

    def re_spawn_food(self, settings: dict) -> None:
        self.x_coord = uniform(0.9*settings['x_min'], 0.9*settings['x_max'])
        self.y_coord = uniform(0.9*settings['y_min'], 0.9*settings['y_max'])

    def temporarily_de_spawn(self) -> None:
        self.x_coord = nan
        self.y_coord = nan
