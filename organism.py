import textwrap

import setuptools


class Organism:
    last_id = 1

    @staticmethod
    def get_new_id():
        new_id = Organism.last_id
        Organism.last_id += 1
        return new_id

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

    def play_routine(self):
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
        pass

    def __str__(self):
        txt = f"{self.species_name} {self.id}"
        txt += f"\nposition: {self.position} | velocity: {self.velocity} | hunger: {self.hunger}"
        if len(self.offspring):
            txt += f"\nOffspring:\n" + 10 * "-"
            txt += textwrap.indent(
                "".join(["\n" + str(offspring) for offspring in self.offspring]), "    "
            )
            txt += "\n" + 10 * "-"
        return txt
