from Vector import Vector
from Walkers import Walker


class Obstacles:
    """ This class represents obstacles in the field, the obstacles are represented as a set of vectors"""

    def __init__(self, x1: float, y1: float, radius: float):
        self.__vector = Vector(x1, y1)
        self.__radius = radius

    def check_valid_obstacle(self):
        """ Rules for obstacles:
        The obstacles are represented as a circle,
        The minimum radius value needs to be greater than 2
        The obstacles are not allowed cover the starting point (0,0) point """
        # Check if the radius is greater than 2
        if self.__radius < 2:
            return False
        # Check if the obstacles area is not covering the starting (0,0) point,
        # + two units (+2) so the walker couldn't be stuck if there are many obstacles blocking the way
        # because the walker can choose move randomly with size of 0.5 up to 1.5 (random step)
        if self.__vector.magnitude_from_start() <= self.__radius + 2:
            return False
        return True

    def get_obstacle_vector(self) -> Vector:
        """ This method returns the obstacle vector"""
        return self.__vector

    def get_obstacle_radius(self) -> float:
        """ This method returns the obstacle radius"""
        return self.__radius

    def __repr__(self):
        """ This method returns the string representation of the obstacle"""
        return f"Obstacle at {self.__vector} with radius {self.__radius}"


class TeleportingArea:
    """A class representing a magical teleporting area (circle) in the field
     that teleports the walker to different locations. """

    """ Rules for teleporting area:
        The teleporting area is represented as a magical circle,
        The min radius of the circle 2
        The teleporting area is not allowed to cover the starting point (0,0) point
        The teleporting area is not allowed to overlap
        the teleporting area is not allowed to cover the obstacles
        The x y desired are not in the teleporting area ( in order to avoid infinite teleporting)
        the teleporting area is not allowed to cover teleporting area
    """
    def __init__(self, x, y, radius, x_teleported, y_teleported):
        self.__vector = Vector(x, y)
        self.__radius = radius
        self.__vector_teleport = Vector(x_teleported, y_teleported)

    def check_valid_teleporting_area(self) -> bool:
        """ This method checks if the teleporting area is valid or not """
        # Check if the radius is greater than 2
        if self.__radius < 2:
            return False
        # Check if the teleporting area is not covering the starting (0,0) point
        if self.__vector.magnitude_from_start() <= self.__radius:
            return False
        # Checks if the teleported x y desired are not in the teleporting area
        if self.__vector.magnitude_self_other(self.__vector_teleport) <= self.__radius:
            return False
        return True

    def get_teleport_vector(self) -> Vector:
        """ This method returns the vector of the teleporting area (star location) """
        return self.__vector

    def get_teleport_radius(self) -> float:
        """ This method returns the radius of the teleporting area """
        return self.__radius

    def get_teleported_to_vector(self) -> Vector:
        """ This method returns the desired vector of the teleporting area (destination location)"""
        return self.__vector_teleport

    def __repr__(self):
        """Provide a string representation of a teleporting area."""
        return (f"TeleportCircle at x={self.__vector.get_x()}, y={self.__vector.get_y()},r={self.__radius},"
                f" to x={self.__vector_teleport.get_x()}, y={self.__vector_teleport.get_y()})")


class SlowArea:
    """ This class represents slow area in the field, when the walker walks into them, his step becomes slower,
     the slow areas are represented as a set of vectors"""

    def __init__(self, x1: float, y1: float, radius: float):
        self.__vector = Vector(x1, y1)
        self.__radius = radius

    def get_slow_area_vector(self) -> Vector:
        """ This method returns the slow area vector"""
        return self.__vector

    def get_slow_area_radius(self) -> float:
        """ This method returns the slow area radius"""
        return self.__radius

    def __repr__(self):
        """ This method returns the string representation of the slow area"""
        return f"Slow area at {self.__vector} with radius {self.__radius}"


class Field:
    """ This class represents a field where a walker can walk,
    the class has a method to add a walker (only 1!), obstacles and teleporting areas to the field,
     and it can move the walker according to the rules of the walker (and the field or game)

     The field logic is based on that the simulation  will add first the walker,
     then the obstacles and finally the teleporting areas.
     """
    def __init__(self):
        self.__walker = None
        self.__obstacles = set()
        self.__teleporting_areas = set()
        self.__slow_areas = set()

# we want only one walker in the field (!)
    def add_walker(self, walker: Walker) -> bool:
        """ This method adds a walker to the field, returns True if the walker is added successfully, False otherwise"""
        if self.__walker is None:
            self.__walker = walker
            return True
        else:
            return False  # Field already has a walker

    def move_walker(self) -> bool:
        """ This method moves the walker according to the rules of the walker and the field """
        in_slow_area = False
        for slow_area in self.__slow_areas:
            if (self.__walker.get_loc().magnitude_self_other(slow_area.get_slow_area_vector()) <
                    slow_area.get_slow_area_radius()):
                self.__walker.change_step_size(0.5)
                in_slow_area = True
        target_loc = self.__walker.final_single_walk() + self.__walker.get_loc()
        if in_slow_area is True:
            self.__walker.change_step_size(1)
        # Check if the target location is inside any obstacle
        for obstacle in self.__obstacles:
            if obstacle.get_obstacle_vector().magnitude_self_other(target_loc) <= obstacle.get_obstacle_radius():
                # If the target location is inside obstacle, do not move the walker, it is not possible to make the move
                return False
        # Check if the target location is inside any teleporting area
        for area in self.__teleporting_areas:
            if area.get_teleport_vector().magnitude_self_other(target_loc) <= area.get_teleport_radius():
                # if the magnitude between the two vectors is smaller than the radius,
                # we need to teleport the walker to the specified location
                self.__walker.set_vec_loc(area.get_teleported_to_vector())
                return True
        # If the target location is not inside any obstacle nor teleporting area, move the walker and return True
        self.__walker.set_vec_loc(target_loc)
        return True

    def get_loc_walker(self) -> Vector:
        """ This method returns the location of the walker"""
        get_loc = self.__walker.get_loc()
        return get_loc

    def __repr__(self):
        """ This method returns the string representation of the field"""
        return "Field with walker at " + str(self.__walker.get_loc())

    def field_restart(self):
        """ This method restarts the field, by setting the walker location to (0,0)
        This method is useful for the simulation (number of runs) to restart the walker after each run,
        in order to start from the same point.
        IT DOESN'T REMOVE THE OBSTACLES AND TELEPORTING AREAS (!)
        if we want to change them in the simulator, we need to do another simulation"""
        self.__walker.set_vec_loc(Vector())

    def add_obstacle(self, obstacle: Obstacles):
        """ This method adds an obstacle to the field, returns True if the obstacle is added successfully,
         False otherwise. Obstacles must be added before the teleporting areas"""
        if obstacle.check_valid_obstacle():
            # if the obstacles is valid from the obstacle class requirements, add it to the field.
            self.__obstacles.add(obstacle)
            return True
        else:
            return False

    def add_teleporting_area(self, teleporter: TeleportingArea):
        """ This method adds a teleporting area to the field,
        returns True if the teleporting area is added successfully,"""
        if teleporter.check_valid_teleporting_area():
            for telep_area in self.__teleporting_areas:
                # Check if the new teleporter overlaps with existing ones telep_areas (to avoid infinite teleporting)
                if (telep_area.get_teleport_vector().magnitude_self_other(teleporter.get_teleport_vector())
                        <= telep_area.get_teleport_radius()):
                    return False
            # Check if the new teleporting area overlaps with obstacles
            for obstacle in self.__obstacles:
                if (obstacle.get_obstacle_vector().magnitude_self_other(teleporter.get_teleport_vector())
                        <= obstacle.get_obstacle_radius()):
                    return False
            self.__teleporting_areas.add(teleporter)
            return True
        else:
            return False

    def add_slow_area(self, slow_area: SlowArea):
        """ This method adds an obstacle to the field, returns True if the obstacle is added successfully,
         False otherwise. Obstacles must be added before the teleporting areas"""
        self.__slow_areas.add(slow_area)
        return True

    def get_obstacles(self):
        return self.__obstacles

    def get_teleporting_areas(self):
        return self.__teleporting_areas

    def get_slow_areas(self):
        return self.__slow_areas
