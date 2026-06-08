from Vector import Vector
from abc import ABC, abstractmethod
import random


class Walker(ABC):
    """ Walker class is inheriting from the ABC class
    By inheriting from ABC, the Walker class is recognized as an abstract base class.

    An abstract base class is like a blueprint for other sub classes.
    It defines methods that must be implemented by its subclasses but doesn't provide
    implementations for those methods itself"""

    def __init__(self, random_step=False, bias: int = 0, direction: int = 0, return_to_start: bool = False,
                 constant_return: bool = True) -> None:
        """ Initialize a walker, with negative default values of random step, bias and direction,
        return_to_start and constant unless called otherwise as an argument"""
        self.__vector = Vector()
        self.__random_step = random_step
        self.__bias = bias
        self.__direction = direction
        self.step = 1  # default value
        self.__return_to_start = return_to_start
        self.__constant = constant_return

    def pick_rand_step(self) -> float:
        """ This method picks a random step size for the walker, returns a float."""
        if self.__random_step:
            random_step = random.random() + 0.5
            return random_step * self.step
        else:
            return self.step

    def return_to_start(self):
        """ This method returns a boolean value based on whether the walker will need to go in the specific step."""
        if self.__return_to_start:
            if self.__constant:
                if random.randint(0, 99) < 1:
                    return True
                else:
                    return False
            else:
                if random.randint(0, 999) < self.__vector.magnitude_from_start():
                    # for each 1 unit from start it increase the chance to get to (0,0) by 0.1%
                    return True
                else:
                    return False
        return False

    @abstractmethod
    def unit_single_random_walk(self):
        """ Abstract method that defines the behavior of generating a unit(length 1) random step.
        This method doesn't have an implementation (the pass statement is just a placeholder)
        it MUST (!) be implemented by subclasses."""
        pass

    def scaled_single_random_walk(self) -> Vector:
        """ This method generates a scaled random step based on the unit random step and the current step size.
        Returns: A Vector object representing the scaled random step. """
        if self.__random_step:
            self.step = self.pick_rand_step()
        vector = self.unit_single_random_walk()
        scaled_vec = vector * self.step
        return scaled_vec

    def final_single_walk(self) -> Vector:
        """ This method which will be used as the API of the final step of the walker"""
        if self.return_to_start():
            vec_start_direction = Vector() - self.__vector
            return vec_start_direction
        elif self.__bias == 0 or self.__direction == 0:
            return self.scaled_single_random_walk()
        else:
            # biased single walk!
            vec_start_direction = Vector() - self.__vector
            vec_start_direction = vec_start_direction.normalize()
            vec_start_direction = vec_start_direction * self.step
            dict_possible_biased_directions = {
                1: vec_start_direction,  # Starting Point
                2: Vector(1, 0),  # Right
                3: Vector(-1, 0),  # Left
                4: Vector(0, 1),  # Up
                5: Vector(0, -1)  # Down
            }
            if random.randint(0, 9) < self.__bias:
                # then we successfully entered the biased area
                return dict_possible_biased_directions[self.__direction] * self.pick_rand_step()
            else:
                return self.scaled_single_random_walk()

    def __repr__(self):
        """This method returns a string representation of the walker object."""
        return f"This is {type(self).__name__} at {self.__vector}"

    def get_loc(self) -> Vector:
        """ This method returns the location of the walker"""
        return self.__vector

    def set_vec_loc(self, vector: Vector) -> None:
        """ This method sets the location of the walker"""
        self.__vector = vector

    def change_step_size(self, step_size: float):
        """ This method changes the step size of the walker, in slow areas"""
        self.step = step_size
        return


class WalkerDiscrete(Walker):
    """ This class represents a discrete walker which is able to walk left, right, up, down.
    Inherits from the abstract base class Walker"""

    def unit_single_random_walk(self):
        """ This method calculates a unit-length random step for the discrete walker."""
        possible_moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        rand_step = random.choice(possible_moves)
        return Vector(rand_step[0], rand_step[1])


class Walker360(Walker):
    """ This class represents a 360-degree walker.
    It inherits from the abstract base class Walker"""
    @staticmethod
    def choose_direction() -> Vector:
        """ This method generates a random direction vector """
        # We need to adjust the random selection range from 0 to 1 to -1 to 1 by scaling the array by 2
        # and shifting one step to the left.
        random_x = random.random() * 2 - 1
        random_y = random.random() * 2 - 1
        return Vector(random_x, random_y)

    def unit_single_random_walk(self) -> Vector:
        """ This method calculates a unit-length random step for the 360 walker."""
        vector = self.choose_direction()
        norm_vector = vector.normalize()
        return norm_vector
