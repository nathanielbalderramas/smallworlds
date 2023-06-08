import textwrap
import random


# should be its own module
class Navigator:
    def move(
        self,
        position: (int, int),
        velocity: (int, int),
        speed: int,
        neighbours: list[Organism],
    ) -> ((int, int), (int, int)):
        pass

    def initialize(self) -> ((int, int), (int, int)):
        pass

    def is_in_range(self, position_a: (int, int), position_b: (int, int), threshold: int) -> bool:
        distance = self.calculate_distance(position_a, position_b)
        return distance <= threshold

    @staticmethod
    def calculate_distance(position_a: (int, int), position_b: (int, int)) -> float:
        pass


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
        navigator: Navigator,
        speed: int,
        base_hunger: int,
        feeding_range: int,
        feeding_chance: int,
        offspring_chance: int,
        litter_size: int,
    ) -> None:
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

    def reset(self) -> None:
        self.position, self.velocity = self.navigator.initialize()
        self.hunger = self.base_hunger
        self.is_alive = True
        self.reproduced_this_epoch = False
        self.offspring = []

    def advance_time(self) -> None:
        self.move()
        self.eat()
        self.reproduce()

    def move(self) -> None:
        self.position, self.velocity = self.navigator.move(
            self.position, self.velocity, self.speed, self.neighbours
        )

    def eat(self) -> None:
        for neighbour in self.neighbours:
            if neighbour.is_alive():
                if self.is_in_range(neighbour.get_position()) and self.is_successful_attempt(self.feeding_chance):
                    food = neighbour.be_eaten()
                    self.feed(food)
                    return
            else:
                self.remove_from_neighbours(neighbour)

    def reproduce(self) -> None:
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
        return self.hunger <= 0

    def produce_offspring(self) -> None:
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

    def feed(self, food: int) -> None:
        self.hunger -= food

    def remove_from_neighbours(self, neighbour: Organism) -> None:
        self.neighbours.remove(neighbour)

    def be_eaten(self) -> int:
        self.is_alive = False
        food = int(self.base_hunger / 5) + 1
        return food

    def is_in_range(self, position) -> bool:
        return self.navigator.is_in_range(self.position, position, self.feeding_range)

    def get_position(self) -> (int, int):
        return self.position
