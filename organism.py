import textwrap
import random
import numpy as np


class Organism:
    last_id = 1

    @staticmethod
    def get_new_id() -> int:
        new_id = Organism.last_id
        Organism.last_id += 1
        return new_id

    @staticmethod
    def is_successful_attempt(reference: int) -> bool:
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
            if neighbour.is_alive():
                if (
                    self.outrank(neighbour)
                    and self.is_in_range(neighbour.get_position())
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
        has this organism eaten enough food already?
        """
        return self.hunger <= 0

    def produce_offspring(self) -> None:
        """
        creates a new organism and adds it to offspring list
        """
        for i in range(self.litter_size):
            child = Organism(
                self.species_name,
                self.trophic_level,
                self.navigator,
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
        lowers hunger level
        """
        self.hunger -= food

    def remove_from_neighbours(self, neighbour: Organism) -> None:
        """
        removes another organism from the neighbour list
        """
        self.neighbours.remove(neighbour)

    def be_eaten(self) -> int:
        """
        dies and is turned into food
        """
        self.is_alive = False
        food = int(self.base_hunger / 5) + 1
        return food

    def is_in_range(self, position: np.ndarray[float, float]) -> bool:
        """
        is that other organism inside my feeding range?
        """
        return self.navigator.is_in_range(self.position, position, self.feeding_range)

    def get_position(self) -> np.ndarray[float, float]:
        """
        :returns: (x, y)
        """
        return self.position

    def outrank(self, neighbour: Organism) -> bool:
        """
        :param neighbour: Organism
        :return: bool
        """
        return self.trophic_level > neighbour.trophic_level
