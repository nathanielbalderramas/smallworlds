from abc import ABC, abstractmethod
import numpy as np


class Navigator(ABC):
    @abstractmethod
    def move(
        self,
        position: np.ndarray[float, float],
        speed: int,
        neighbours: list[any],
    ) -> tuple[np.ndarray[float, float], np.ndarray[float, float]]:
        pass

    @abstractmethod
    def initialize(self) -> tuple[np.ndarray[float, float], np.ndarray[float, float]]:
        pass

    @abstractmethod
    def is_in_range(
        self,
        position_a: np.ndarray[float, float],
        position_b: np.ndarray[float, float],
        threshold: int,
    ) -> bool:
        pass


class ClassicNavigator(Navigator):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.orientation = np.zeros(2)

    def initialize(self) -> tuple[np.ndarray[float, float], np.ndarray[float, float]]:
        """
        returns a randomized set of position and orientation to begin a new epoch
        :return: (position_array, orientation_array)
        """
        # generates random position inside environment coordinates
        position = np.array(
            [np.random.randint(0, self.x + 1), np.random.randint(0, self.y + 1)]
        )

        # generates random unitary orientation vector
        orientation = np.random.rand(2)
        orientation = orientation / np.linalg.norm(orientation)
        self.orientation = orientation

        return position, orientation

    def move(
        self,
        position: np.ndarray[float, float],
        speed: int,
        neighbours: list[any],
    ) -> tuple[np.ndarray[float, float], np.ndarray[float, float]]:
        velocity = self.orientation * speed
        position = position + velocity
        position, velocity = self.correct_trajectory(position, velocity)
        return position, velocity

    def is_in_range(
        self,
        position_a: np.ndarray[float, float],
        position_b: np.ndarray[float, float],
        threshold: int,
    ) -> bool:
        pass

    def correct_trajectory(
        self, position: np.ndarray[float, float], velocity: np.ndarray[float, float]
    ) -> tuple[np.ndarray[float, float], np.ndarray[float, float]]:
        """
        :param position:
        :param velocity:
        :return: (position, velocity)

        corrects the trajectory if position is outside the environment by making it bounce with its "walls"
        """

        # corrects in x direction
        if position[0] < 0:
            position[0] = position[0] * -1
            velocity[0] = velocity[0] * -1
        elif position[0] > self.x:
            position[0] = 2 * self.x - position[0]
            velocity[0] = velocity[0] * -1

        # corrects in y direction
        if position[1] < 0:
            position[1] = position[1] * -1
            velocity[1] = velocity[1] * -1
        elif position[1] > self.y:
            position[1] = 2 * self.y - position[1]
            velocity[1] = velocity[1] * -1

        return position, velocity


if __name__ == "__main__":
    n1 = ClassicNavigator(100, 100)
    p0, o0 = n1.initialize()
    print(p0, o0, n1.orientation)
    p1, v1 = n1.move(p0, 10, [])
    print(p1, v1)
