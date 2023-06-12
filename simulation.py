import environment
import population


class Simulation:
    """
    This is an individual and independent simulation, with its own environment and populations.
    Must be initialized with a pair of dictionaries containing keyword-argument pairs for the
    environment and the populations.

    If for some reason a simulation is stopped, it can be restarted from the last completed epoch.
    """

    def __init__(
        self,
        name: str,
        time_per_epoch: int,
        neighbour_update_interval: int,
        environment_config: dict,
        populations_configs: list,
    ):
        self.name = name
        self.time_per_epoch = time_per_epoch
        self.time = 0
        self.epoch = 0
        self.neighbour_update_interval = neighbour_update_interval
        self.neighbour_update_ticks = 0

        # create environment
        self.environment = environment.Environment(**environment_config)

        # create populations
        self.populations = []
        navigator = (
            self.environment.get_navigator()
        )  # original navigator to be replicated by organisms
        for pop_config in populations_configs:
            pop_config["individuals_specs"][
                "navigator"
            ] = navigator  # add navigator to individuals_specs
            self.populations.append(population.Population(**pop_config))

        # sort populations by trophic level
        self.populations.sort(key=lambda pop: pop.trophic_level, reverse=True)

        # calculates ideal range for neighbour lists
        self.neighbour_range = self.calculate_neighbour_range()

    def start_simulation(self, epochs_to_run: int) -> None:
        """
        begins a simulation run.
        :param epochs_to_run: int
        :return:
        """
        self.time = 0
        self.update_neighbours()
        while epochs_to_run:
            self.print_organisms_count(discriminate=True)  # for dev purposes
            while self.time <= self.time_per_epoch:
                self.advance_time()
            self.advance_epoch()
            epochs_to_run -= 1

    def advance_time(self) -> None:
        """
        runs a time tick of the simulation
        :return:
        """
        if self.neighbour_update_ticks >= self.neighbour_update_interval:
            self.update_neighbours()

        for pop in self.populations:
            pop.advance_time()

        self.time += 1
        self.neighbour_update_ticks += 1

    def advance_epoch(self) -> None:
        """
        runs an epoch tick for the simulation
        :return:
        """
        for pop in self.populations:
            pop.advance_epoch()
        self.epoch += 1
        self.time = 0
        self.neighbour_update_ticks = 0
        self.update_neighbours()

    def print_organisms_count(self, discriminate: bool) -> None:
        """
        prints to console a count of organisms inside living_individuals for each population.
        if discriminate is false, then prints the accumulated total of living organisms.
        :param discriminate:
        :return:
        """
        if discriminate:
            print("Organism count:")
            for pop in self.populations:
                print(f"{pop.species_name}: {pop.get_size()}")
        else:
            pop_count = sum([pop.get_size for pop in self.populations])
            print(f"Total organisms: {pop_count}")

    def update_neighbours(self):
        """
        updates the neighbour list in each organism. currently each organism only track those of lower trophic level.
        Thus, organisms of the lowest level track no neighbours. This is for computational limitations only.
        :return:
        """
        # selects two populations, one i and one j where i can prey on j
        for pop_index_i in range(len(self.populations)):
            pop_i = self.populations[pop_index_i]
            for pop_index_j in range(pop_index_i, len(self.populations)):
                pop_j = self.populations[pop_index_j]
                if pop_i.trophic_level > pop_j.trophic_level:

                    # checks whether there is an individual from j "near" i and adds it to its neighbour list
                    for ind_i in pop_i.living_individuals:
                        for ind_j in pop_j.living_individuals:
                            if self.is_in_neighbour_range(ind_i, ind_j):
                                ind_i.neighbours.append(ind_j)

    def calculate_neighbour_range(self):
        """
        returns the optimal range for neighbours lists based on the fastest organism in the simulation and
        the value of neighbour_update_interval
        :return: int
        """
        speeds = [pop.individuals_specs["speed"] for pop in self.populations]
        optimum_range = int(max(speeds) * (2 * self.neighbour_update_interval + 2))
        return optimum_range

    def is_in_neighbour_range(self, ind_i, ind_j):
        """
        Checks whether two organisms are close enough to be considered neighbours.

        Careful! This function takes around 75 % of the simulations time.
        :param ind_i: an Organism
        :param ind_j: another Organism
        :return: bool
        """
        return self.environment.navigator.is_in_range(
            ind_i.position, ind_j.position, self.neighbour_range)
