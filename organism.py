from __future__ import annotations
import textwrap
import random
import numpy as np


class Organism:
    """
    This is the base class of entities to be simulated.
    It's core loop is move -> eat (try to) -> reproduce (try to)
    could be subclassed and have some of its methods overriden to account for certain "special" kind of organisms

    non-obvious attributes:
    -----------------------
    navigator: an object capable of updating position and velocity for the organism according to environment rules.
    also used to calculate distance between organisms.

    trophic_level: how high it stands in the chain food.
    Usually an organism can only feed of those who are of lower level.
    base_hunger: how much it needs to eat before being able to reproduce.

    offspring: a list of new organism that descend from this one.
    They won't enter the simulation until the next epoch

    neighbours: a list of organisms that the simulation has deemed sufficiently close to this one.
    It's for computational efficiency reasons.
    (see https://nanohub.org/resources/7578/download/Martini_L6_NeighborList.pdf as an introduction to the topic)

    a note on speed and velocity:
    -----------------------------
    As commonly defined in physics, speed is a scalar value and velocity a vectorial one.
    The norm of velocity is actually speed.
    """

    ids = {}

    @staticmethod
    def get_new_id(species_name) -> int:
        """
        This method ensures that every  organism in a species
        gets assigned a unique value of id
        :return: new_id: int
        """
        new_id = Organism.ids.setdefault(species_name, 1)
        Organism.ids[species_name] += 1
        return new_id

    @staticmethod
    def is_successful_attempt(reference: int) -> bool:
        """
        this method checks for a "roll of the dice"
        :param reference: value to compare to random number. should be between 0 and 100.
        :return: bool
        """
        return random.randint(0, 100) <= reference

    def __init__(
        self,
        species_name: str,
        trophic_level: int,
        navigator: Navigator,
        speed: float,
        base_hunger: int,
        feeding_range: float,
        feeding_chance: int,
        offspring_chance: int,
        litter_size: int,
    ) -> None:
        # parameter dependent attributes
        self.species_name = species_name
        self.trophic_level = trophic_level
        self.navigator = navigator.get_replica()
        self.speed = speed
        self.base_hunger = base_hunger
        self.feeding_range = feeding_range
        self.feeding_chance = feeding_chance
        self.offspring_chance = offspring_chance
        self.litter_size = litter_size

        # parameter independent attributes
        self.id = Organism.get_new_id(self.species_name)
        self.offspring = []
        self.neighbours = []
        self.hunger = 0
        self.position = np.zeros(2)
        self.velocity = np.zeros(2)
        self.reproduced_this_epoch = False
        self.is_alive = False

    def reset(self) -> None:
        """
        prepares to begin a new epoch
        """
        self.position, self.velocity = self.navigator.initialize()
        self.hunger = self.base_hunger
        self.is_alive = True
        self.reproduced_this_epoch = False
        self.offspring = []
        self.neighbours = []

    def advance_time(self) -> None:
        """
        runs the basic interactions of a time tick
        """
        self.move()
        self.eat()
        self.reproduce()

    def move(self) -> None:
        """
        updates position and velocity
        """
        self.position, orientation = self.navigator.move(
            self.position, self.speed, self.neighbours
        )
        self.velocity = self.speed * orientation

    def eat(self) -> None:
        """
        tries to eat another organism if its alive and in range.
        """
        for neighbour in self.neighbours:
            if neighbour.is_alive:
                if (
                    self.outrank(neighbour)
                    and self.is_in_range(neighbour.position)
                    and self.is_successful_attempt(self.feeding_chance)
                ):
                    food = neighbour.be_eaten()
                    self.feed(food)
                    return
            else:
                # if neighbour is dead stops tracking it
                self.remove_from_neighbours(neighbour)

    def reproduce(self) -> None:
        """
        tries to produce offspring if its satiated
        """
        if self.is_satiated() and self.is_successful_attempt(self.offspring_chance):
            self.produce_offspring()

    def __str__(self) -> str:
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

    def is_satiated(self) -> bool:
        """
        checks whether this organism has eaten enough food.
        """
        return self.hunger <= 0

    def produce_offspring(self) -> None:
        """
        creates a new organism of the same class and adds it to offspring list
        """
        for i in range(self.litter_size):
            child = self.__class__(
                self.species_name,
                self.trophic_level,
                self.navigator.get_replica(),
                self.speed,
                self.base_hunger,
                self.feeding_range,
                self.feeding_chance,
                self.offspring_chance,
                self.litter_size,
            )
            self.offspring.append(child)

    def feed(self, food: int) -> None:
        """
        updates hunger value according to the amount of food ingested.
        """
        self.hunger -= food

    def remove_from_neighbours(self, neighbour: Organism) -> None:
        """
        removes another organism from the neighbour list.
        """
        self.neighbours.remove(neighbour)

    def be_eaten(self) -> int:
        """
        dies and is turned into some quantity of food.
        """
        self.is_alive = False
        food = int(self.base_hunger / 5) + 1
        return food

    def is_in_range(self, position: np.ndarray[float, float]) -> bool:
        """
        checks whether another organism is inside feeding range
        """
        return self.navigator.is_in_range(self.position, position, self.feeding_range)

    def outrank(self, neighbour: Organism) -> bool:
        """
        checks whether another organism is bellow in the food chain.
        :param neighbour: Organism
        :return: bool
        """
        return self.trophic_level > neighbour.trophic_level
