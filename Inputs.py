# Description: This file contains the UserInput class
# which handles all user interactions for the user
# to input data for the simulation.

class UserInput:
    """ Handles all user interactions for the user to input data for the simulation."""
    def __init__(self):
        self.__plots = {
            1: "Mean distance from starting point",
            2: "The mean time (number of steps) to exit a given radius",
            3: "Mean distance from x-axis",
            4: "Mean distance from y-axis",
            5: "Number of times the walker crosses the y-axis",
            6: "(EXTRA!) Probability of crossing the y-axis"
        }

    def check_walker_input(self):
        # Walker type
        while True:
            walker_type = input("\n\nEnter walker type (discrete/360): ").strip().lower()
            if walker_type in ["discrete", "360"]:
                break
            print("Error: Invalid walker type. Please choose 'discrete' or '360'.")

        while True:
            walker_bool_rand_step = input("Set random step (y/n): ").strip().lower()
            if walker_bool_rand_step == "y":
                random_step = True
                break
            elif walker_bool_rand_step == "n":
                random_step = False
                break
            else:
                print("Error: Invalid input. Please enter 'y' or 'n'.")

        while True:
            bias_str = input("Enter bias of the walker 0-10 (0 = None, 1-10 for desired intensity): ").strip()
            if bias_str.isdigit() and 0 <= int(bias_str) <= 10:
                bias = int(bias_str)
                break
            print("Error: Bias value must be an integer between 0 and 10.")

        # in the logic of the program, if the walker is not biased, the direction is 0
        # (there is no direction to be biased for)
        if bias == 0:
            direction = 0
        else:
            while True:
                direction_str = input("Enter direction (1-5): 1=Starting Point, 2=Right,"
                                      " 3=Left, 4=Up, 5=Down ").strip()
                if direction_str.isdigit() and 1 <= int(direction_str) <= 5:
                    direction = int(direction_str)
                    break
                print("Error: Invalid direction. Please choose from 1 to 5.")

        while True:
            walker_chance_to_return = input("Set a chance to return to starting point (y/n): ").strip().lower()
            if walker_chance_to_return == "y":
                return_to_start = True
                while True:
                    constant_chance = input("chance to return of 1% constant? if not, there will be a chance that"
                                            " will grow by 0.1% for each step away from starting point (y/n): "
                                            ).strip().lower()
                    if constant_chance == "y":
                        constant_return = True
                        break
                    elif constant_chance == "n":
                        constant_return = False
                        break
                    else:
                        print("Error: Invalid input. Please enter 'y' or 'n'.")
                break
            elif walker_chance_to_return == "n":
                return_to_start = False
                constant_return = True
                break
            else:
                print("Error: Invalid input. Please enter 'y' or 'n'.")
        return walker_type, random_step, bias, direction, return_to_start, constant_return

    def get_simulator_data(self):
        while True:
            try:
                num_steps = int(input("Enter the number of steps: "))
                if num_steps <= 0:
                    print("Number of steps must be a positive number.")
                # elif num_steps > 5000:
                #     print("Number of steps must be less than 5000 in our simulation.")
                else:
                    break
            except ValueError:
                print("Value Error! Invalid input! Please enter a valid NUMBER.")

        while True:
            try:
                num_runs = int(input("Enter the number of simulation runs: "))
                if num_runs <= 0:
                    print("Number of simulation runs must be a positive integer.")
                # elif num_runs > 5000:
                #     print("Number of simulation runs must be less than 5000 in our simulation.")
                else:
                    break
            except ValueError:
                print("Value Error! Invalid input! Please enter a valid NUMBER.")

        return num_steps, num_runs

    def get_validated_input(self, prompt, validation_func):
        """General method for getting validated input using a validation function."""
        while True:
            user_input = input(prompt)
            try:
                # Attempt to convert and validate the input using the provided validation function
                return validation_func(user_input)
            except ValueError as e:
                # Print the error message from the validation function and prompt again
                print(e)

    def validate_float(self, input_str):
        """Validation function for float inputs."""
        value = float(input_str)
        return value

    def validate_positive_float(self, input_str):
        """Validation function for positive float inputs."""
        value = float(input_str)
        if value <= 0:
            raise ValueError("The value must be a positive number.")
        return value

    def get_obstacle_data(self):
        obstacles = []
        while True:
            obstacle_bool = input("\nDo you want to add an obstacle? (y/n): ").strip().lower()
            if obstacle_bool == 'y':
                # Validate and get x-coordinate
                x = self.get_validated_input("Enter the obstacle's x-coordinate: ", self.validate_float)
                # Validate and get y-coordinate
                y = self.get_validated_input("Enter the obstacle's y-coordinate: ", self.validate_float)
                # Validate and get radius (positive number)
                radius = self.get_validated_input("Enter the obstacle's radius: ", self.validate_positive_float)

                obstacles.append((x, y, radius))
            elif obstacle_bool == 'n':
                if not obstacles:
                    print("No obstacles added.")
                return obstacles
            else:
                print("Invalid input! Please enter 'y' or 'n'.")

    def ask_to_continue_adding(self):
        while True:
            choice = input("Feeling very forgiving, I can give you another chance to add again."
                           " Ready for the adventure?  (y/n)").strip().lower()
            if choice in ['y', 'n']:
                if choice == 'y':
                    return True
                else:
                    return False
            else:
                print("Invalid input! Please enter 'y' for yes or 'n' for no.")

    def get_teleporting_area_data(self):
        """Gathers data from the user to create TeleportingArea instances."""
        teleporting_areas = []
        while True:
            choice = input("\nDo you want to add a teleporting area? (y/n): ").strip().lower()
            if choice == 'y':
                x = self.get_validated_input("Enter the teleporting area's x-coordinate: ", self.validate_float)
                y = self.get_validated_input("Enter the teleporting area's y-coordinate: ", self.validate_float)
                radius = self.get_validated_input("Enter the teleporting area's radius: ", self.validate_positive_float)
                x_teleported = self.get_validated_input("Enter the x-coordinate to teleport to: ", self.validate_float)
                y_teleported = self.get_validated_input("Enter the y-coordinate to teleport to: ", self.validate_float)

                teleporting_areas.append((x, y, radius, x_teleported, y_teleported))
            elif choice == 'n':
                if not teleporting_areas:
                    print("No teleporting areas added.")
                return teleporting_areas
            else:
                print("Invalid input! Please enter 'y' or 'n'.")

    def get_slow_area_data(self):
        slow_areas = []
        while True:
            slow_area_bool = input("\nDo you want to add a slow area? (y/n): ").strip().lower()
            if slow_area_bool == 'y':
                # Validate and get x-coordinate
                x = self.get_validated_input("Enter the slow area's x-coordinate: ", self.validate_float)
                # Validate and get y-coordinate
                y = self.get_validated_input("Enter the slow area's y-coordinate: ", self.validate_float)
                # Validate and get radius (positive number)
                radius = self.get_validated_input("Enter the slow area's radius: ", self.validate_positive_float)

                slow_areas.append((x, y, radius))
            elif slow_area_bool == 'n':
                if not slow_areas:
                    print("No obstacles added.")
                return slow_areas
            else:
                print("Invalid input! Please enter 'y' or 'n'.")

    def want_to_see_plot(self):
        return self.get_yes_no_input("Want to see a plot? (y/n): ")

    def which_plot(self):
        print("Available plots:")
        for key, value in self.__plots.items():
            print(f"{key}: {value}")
        while True:
            choice = input("Which one? Choose a number: ").strip()
            if choice.isdigit() and int(choice) in self.__plots:
                return int(choice)
            else:
                print("Invalid input! Please choose a valid plot number.")

    def want_to_save(self):
        return self.get_yes_no_input("Want to save it? (y/n): ")

    def get_yes_no_input(self, prompt):
        """General method for getting a yes/no answer and returning it as a boolean."""
        while True:
            choice = input(prompt).strip().lower()
            if choice in ['y', 'n']:
                return choice == 'y'
            else:
                print("Invalid input! Please enter 'y' for yes or 'n' for no.")

    def decide_on_plots(self):
        """Extended to include asking for radius on the second plot choice."""
        while True:
            if not self.want_to_see_plot():
                return None, None, None, None  # Indicates no more plots are desired

            plot_choice = self.which_plot()
            save_plot = False
            filename = None
            radius = None

            if plot_choice:
                save_plot = self.want_to_save()
                if save_plot:
                    filename = self.get_filename()

            if plot_choice == 2:  # Specific case for the second plot choice
                radius = self.get_radius_for_plot()

            yield plot_choice, save_plot, filename, radius

    def get_filename(self):
        """Asks the user for a filename to save the plot."""
        filename = input("Enter the filename to save: ").strip()
        # Add any validation or processing of filename if needed
        return filename

    def get_radius_for_plot(self):
        """Asks the user for a radius for specific plots that require it, with a warning about large values."""
        print("Please enter the radius for the plot.\nNote: Choosing a large radius value might result in not "
              " seeing the red dot, which indicates the num step at which the walker reaches this radius,\n "
              "This will not being shown because walker doesn't reach that radius within the given number of steps.\n")

        while True:
            radius_input = input("Enter the radius for the plot: ").strip()
            try:
                radius = float(radius_input)
                if radius > 0:
                    return radius
                else:
                    print("Radius must be a positive number.")
            except ValueError:
                print("Invalid input! Please enter a valid number for the radius.")
