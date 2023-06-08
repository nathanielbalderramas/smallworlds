from organism import Organism


class Population:
    def __init__(
        self,
        species_name: str,
        species_trophic_level: int,
        initial_size: int,
        individuals_specs: dict,
    ):
        self.species_name = species_name
        self.species_trophic_level = species_trophic_level
        self.individuals_specs = individuals_specs
        self.living_individuals = []
        self.dead_individuals = []
        for i in range(initial_size):
            self.create_individual()

    def add_individual(self, organism: Organism):
        self.living_individuals.append(organism)

    def create_individual(self):
        self.living_individuals.append(Organism(*self.individuals_specs))

    def remove_individual(self, individual: Organism):
        """
        stashes an individual into the dead_individuals list to save its offspring for next epoch
        :param individual: Organism
        :return:
        """
        self.dead_individuals.append(individual)
        self.living_individuals.remove(individual)

    def advance_time(self):
        for individual in self.living_individuals:
            individual.advance_time()

    def advance_epoch(self):
        # generates new individuals based on the offspring of both dead and living individuals
        for individual in self.dead_individuals + self.living_individuals:
            for child in individual.get_offspring():
                self.add_individual(child)
            individual.reset()

        # resets dead_individuals
        self.dead_individuals = []

        # to be continued
        pass
