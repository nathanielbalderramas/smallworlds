from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np


class Navigator(ABC):
    """
    this is an abstract class that must be subclassed.
    All of its methods should be implemented in subclasses (aka, an informal interface in python).

    the concept behind this is that depending on the rules of an environment a certain displacement may
    or may not be valid, and the logic concerning this doesn't fit into the Organism class. It would also be weird
    to ask for environment to move an organism around, so the solution I came up with is this class that calculates
    where an organism should be on the next time step but only returns this information and then the Organism can update
    its position and velocity.

    Why is this an interface?
    -------------------------
    well, there may be different kinds of environment. as of right now an environment is only of rectangular shape and
    can have 1 or 2 periodic boundary conditions. the validations required to check whether a movement is valid or
    how far are two objects vary significantly, and it would be gruesome to have all of it coded into a single class
    with conditional expressions to check for environment rules. Also, I would like to implement different box shapes
    in the future, as well as discretizing space into a rectangular or hexagonal grid, so the interface is welcome.

    For more information on Periodic Boundary Conditions see here
    (https://en.wikipedia.org/wiki/Periodic_boundary_conditions)
    """
    @abstractmethod
    def move(
        self,
        position: np.ndarray[float, float],
        speed: int,
    ) -> tuple[np.ndarray[float, float], np.ndarray[float, float]]:
        """
        should calculate and return the position and orientation of an organism for the next step according to
        environment rules.

        :param position: a 2d vector
        :param speed:  a scalar
        :return: position (x, y) and orientation (x, y)
        """
        pass

    @abstractmethod
    def initialize(self) -> tuple[np.ndarray[float, float], np.ndarray[float, float]]:
        """
        should return a set of randomized position and orientation to begin a simulation epoch.
        :return: position (x, y), orientation (x, y)
        """
        pass

    @abstractmethod
    def is_in_range(
        self,
        position_a: np.ndarray[float, float],
        position_b: np.ndarray[float, float],
        threshold: int,
    ) -> bool:
        """
        should check whether the distance between position_a and position_b is bellow the threshold
        :param position_a: (x, y)
        :param position_b: (x, y)
        :param threshold: a scalar
        :return: bool
        """
        pass

    @abstractmethod
    def get_replica(self) -> Navigator:
        """
        Creates a new object of the same class with the same environment rules.
        This is useful when reproducing organisms!
        :return: Navigator
        """
        pass


class ClassicNavigator(Navigator):
    """
    This navigator responds to an environment that is continuous in nature, with rectangular shape and solid walls.
    organisms bounce elastically into the walls
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.orientation = np.zeros(2)

    def get_replica(self) -> ClassicNavigator:
        return self.__class__(self.x, self.y)

    def initialize(self) -> tuple[np.ndarray[float, float], np.ndarray[float, float]]:
        """
        returns a set of randomized position and orientation to begin a simulation epoch.
        :return: position (x, y), orientation (x, y)
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
        speed: int
    ) -> tuple[np.ndarray[float, float], np.ndarray[float, float]]:
        """
        returns an updated position and velocity according to current position and speed,
        respecting environment rules
        :param position:
        :param speed:
        :return: position (x, y), orientation (x, y)
        """
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
        """
        checks whether the distance between position_a and position_b is bellow the given threshold
        :param position_a: (x, y)
        :param position_b: (x, y)
        :param threshold: a scalar
        :return: bool
        """
        return self.calculate_distance(position_a, position_b) <= threshold

    def correct_trajectory(
        self, position: np.ndarray[float, float], velocity: np.ndarray[float, float]
    ) -> tuple[np.ndarray[float, float], np.ndarray[float, float]]:
        """
        corrects the trajectory if position is outside the environment by making it bounce with its walls.
        :param position:
        :param velocity:
        :return: (position, velocity)
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

    @staticmethod
    def calculate_distance(a: np.ndarray[float, float], b: np.ndarray[float, float]) -> float:
        """
        calculates the distance between points a and b in a simple Euclidean fashion
        :param a: position (x, y)
        :param b: position (x, y)
        :return: distance: float
        """
        return np.linalg.norm(b-a)
