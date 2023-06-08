import textwrap
import random


class Organism:
    last_id = 1

    @staticmethod
    def get_new_id():
        new_id = Organism.last_id
        Organism.last_id += 1
        return new_id

    @staticmethod
    def is_successful_attempt(reference):
        return random.randint(0, 100) <= reference

    def __init__(
        self,
        species_name,
        navigator,
        speed,
        base_hunger,
        feeding_range,
        feeding_chance,
        offspring_chance,
        litter_size,
    ):
        # parameter dependent attributes
        self.species_name = species_name
        self.navigator = navigator
        self.speed = speed
        self.base_hunger = base_hunger
        self.feeding_range = feeding_range
        self.feeding_chance = feeding_chance
        self.offspring_chance = offspring_chance
        self.litter_size = litter_size

        # parameter independent attributes
        self.id = Organism.get_new_id()
        self.offspring = []
        self.neighbours = []
        self.hunger = 0
        self.position = (0, 0)
        self.velocity = (0, 0)
        self.reproduced_this_epoch = False
        self.is_alive = False

    def reset(self):
        self.position, self.velocity = self.navigator.initialize()
        self.hunger = self.base_hunger
        self.is_alive = True
        self.reproduced_this_epoch = False
        self.offspring = []

    def advance_time(self):
        self.move()
        self.eat()
        self.reproduce()

    def move(self):
        self.position, self.velocity = self.navigator.move(
            self.position, self.velocity, self.speed, self.neighbours
        )

    def eat(self):
        pass

    def reproduce(self):
        if self.is_satiated() and self.is_successful_attempt(self.offspring_chance):
            self.produce_offspring()

    def __str__(self):
        # self string formatting
        txt = f"{self.species_name} {self.id}"
        txt += f"\nposition: {self.position} | velocity: {self.velocity} | hunger: {self.hunger}"

        # offspring string formatting
        if len(self.offspring):
            offspring_strings = ["\n" + str(offspring) for offspring in self.offspring]
            txt += f"\nOffspring:\n" + 10 * "-"
            txt += textwrap.indent("".join(offspring_strings), "\t")
            txt += "\n" + 10 * "-"

        return txt

    def is_satiated(self):
        return self.hunger <= 0

    def produce_offspring(self):
        for i in range(self.litter_size):
            child = Organism(
                self.species_name,
                self.navigator,
                self.speed,
                self.base_hunger,
                self.feeding_range,
                self.feeding_chance,
                self.offspring_chance,
                self.litter_size,
            )
            self.offspring.append(child)
