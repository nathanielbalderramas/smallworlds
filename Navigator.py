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