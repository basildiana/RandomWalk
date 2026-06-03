import math


class Vector:
    """This class represents a mathematical vector in 2d-dimensional space.
    This class will encapsulate vector operations (e.g. addition, magnitude...)"""
    def __init__(self, x: float = 0, y: float = 0) -> None:
        # the x, y, are the components of the vectors
        self.__x = x
        self.__y = y

    def __add__(self, other):
        """This method adds two vectors in a space"""
        added_result = self.__x + other.get_x(), self.__y + other.get_y()
        return Vector(added_result[0], added_result[1])

    def __sub__(self, other):
        """This method subtracts two vectors in a space"""
        subtracted_result = self.__x - other.get_x(), self.__y - other.get_y()
        return Vector(subtracted_result[0], subtracted_result[1])

    def __mul__(self, constant: float):
        """This method multiplies the vector by a constant (scaler)"""
        multiplied_result = self.__x * constant, self.__y * constant
        return Vector(multiplied_result[0], multiplied_result[1])

    def __rmul__(self, constant):
        """ useful to allow for both orders or sides of multiplication (for example, constant * vector,
        it makes the class more flexible for other users or potential future use cases"""
        return self.__mul__(constant)

    def __truediv__(self, constant):
        """This method divides the vector by a constant (scaler)"""
        division_result = self.__x / constant, self.__y / constant
        return Vector(division_result[0], division_result[1])

    def magnitude_self_other(self, other):
        """This method calculates the distance between vectors"""
        # abs = absolute value (because we don't know which one of the vectors is bigger)
        mag_result = math.sqrt((abs(self.__x - other.get_x()) ** 2) +
                               (abs(self.__y - other.get_y()) ** 2))
        return mag_result

    def magnitude_from_start(self):
        """This method calculates the distance between vectors"""
        mag_result = math.sqrt(self.__x ** 2 + self.__y ** 2)
        return mag_result

    def normalize(self):
        """This method normalizes the vector to a unit length,
        (same direction but with a magnitude (length) of 1)
        This is achieved by dividing each component of the vector by its magnitude."""
        magnitude = self.magnitude_from_start()
        if magnitude == 0:
            # If the magnitude is 0, it is indicating a zero vector.
            # return a new zero "normalized" vector to avoid division!
            return Vector()
        return Vector(self.get_x() / magnitude,
                      self.get_y() / magnitude)

    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y

    def __repr__(self):
        """String representation of the vector."""
        return f"({self.__x}, {self.__y}) "
