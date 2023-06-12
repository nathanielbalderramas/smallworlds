from organism import Organism


class Population:
    """
    This is mainly a collection of Organisms of the same species.
    It has the ability to create more organisms, add already created
    offspring organisms and remove dead ones.

    non obvious attributes:
    -----------------------
    individuals_specs: is a dictionary containing arguments for initialization of organisms
    """

    def __init__(
        self,
        individuals_specs: dict,
        initial_size: int,
    ):
        self.species_name = individuals_specs["species_name"]
        self.trophic_level = individuals_specs["trophic_level"]
        self.individuals_specs = individuals_specs
        self.living_individuals = []
        self.dead_individuals = []
        for i in range(initial_size):
            self.create_individual()

    def add_individual(self, organism: Organism) -> None:
        """
        adds an already existing individual (mainly used for offspring instances)
        :param organism: Organism
        :return:
        """
        self.living_individuals.append(organism)

    def create_individual(self) -> None:
        """
        creates a new individual calling on the Organism constructor with individuals_specs as keyword arguments.
        :return:
        """
        self.living_individuals.append(Organism(**self.individuals_specs))

    def remove_individual(self, individual: Organism) -> None:
        """
        stashes an individual into the dead_individuals list to save its offspring for next epoch
        :param individual: Organism
        :return:
        """
        self.dead_individuals.append(individual)
        self.living_individuals.remove(individual)

    def advance_time(self) -> None:
        """
        Makes every organism in the population to run for a timestep.
        If a dead organism is found then it's transferred to dead_individuals
        :return:
        """
        for individual in self.living_individuals:
            if individual.is_alive:
                individual.advance_time()
            else:
                self.remove_individual(individual)

    def advance_epoch(self) -> None:
        """
        Adds offspring organisms to the pool of living organisms and resets every organism to begin a new epoch
        :return:
        """
        # generates new individuals based on the offspring of both dead and living individuals
        for individual in self.dead_individuals + self.living_individuals:
            for child in individual.offspring:
                self.add_individual(child)
            individual.reset()

        # resets dead_individuals
        self.reset_dead_individuals()

    def reset_dead_individuals(self) -> None:
        """
        destroys the last reference to each dead individual and clears the dead_individuals list
        :return:
        """
        for dead in self.dead_individuals:
            del dead
        self.dead_individuals = []

    def get_size(self):
        return len(self.living_individuals)
