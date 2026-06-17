from Fields import Field
import matplotlib.pyplot as plt
import csv


class Simulator:
    """ This class simulates a random walk in a ready field.
     Meaning, the field already has a walker, obstacles and teleporting areas."""
    def __init__(self, field1: Field, steps: int, runs: int = 1):
        """ Initialize the Simulator with a given field. """
        self.__field = field1
        self.__num_steps = steps
        self.__num_runs = runs
        self.__data_magnitude = None
        self.__dist_x = None
        self.__dist_y = None
        self.__probability_y_axis_crossings = None
        self.__number_y_axis_crossings = None

    def run_sim(self):
        """ Simulates a random walk in the field for a given number of steps and a given number of runs. """
        final_dist_all_runs = []
        final_x_all_runs = []
        final_y_all_runs = []
        final_y_prob_crossing_all_times = []
        final_y_crossing_all_times = []
        for run in range(self.__num_runs):
            self.__field.field_restart()
            dist_per_run = [0]
            abs_x_loc_per_run = [0]
            abs_y_loc_per_run = [0]
            y_crossings_per_run = [0]
            y_prob_crossings_per_run = [0]
            positive_state = None
            y_crossing = 0
            for step in range(self.__num_steps):
                while True:
                    if self.__field.move_walker():
                        # if the walker moved, we can break the loop, if it didn't move it's not a step!
                        break
                abs_x_loc_per_run.append(abs(self.__field.get_loc_walker().get_x()))
                abs_y_loc_per_run.append(abs(self.__field.get_loc_walker().get_y()))
                dist_per_run.append(self.__field.get_loc_walker().magnitude_from_start())
                current_x = self.__field.get_loc_walker().get_x()
                if current_x == 0:
                    y_prob_crossings_per_run.append(0)
                else:
                    if positive_state is None:
                        positive_state = (current_x > 0)
                        y_prob_crossings_per_run.append(0)
                    else:
                        positive_state, did_cross = self.__crossing(positive_state, current_x)
                        y_prob_crossings_per_run.append(did_cross)
                        if did_cross == 1:
                            y_crossing += 1
                y_crossings_per_run.append(y_crossing)
            final_x_all_runs.append(abs_x_loc_per_run)
            final_y_all_runs.append(abs_y_loc_per_run)
            final_dist_all_runs.append(dist_per_run)
            final_y_prob_crossing_all_times.append(y_prob_crossings_per_run)
            final_y_crossing_all_times.append(y_crossings_per_run)
        self.__dist_x = final_y_all_runs
        self.__dist_y = final_x_all_runs
        self.__data_magnitude = final_dist_all_runs
        self.__probability_y_axis_crossings = final_y_prob_crossing_all_times
        self.__number_y_axis_crossings = final_y_crossing_all_times
        return True

    def get_magnitude(self):
        """ returns a list of lists, each list represents a run, and its elements are the magnitude for each step
         example: [[dist1, dist2, dist3, dist4, dist5],
                 [dist'1, dist'2, dist'3, dist'4, dist'5],
                  ...]"""
        return self.__data_magnitude

    def get_x(self):
        """ returns a list of lists, each list represents a run, and its elements are the x distance value for each step
        example: [[x1, x2, x3, x4, x5],
                 [x'1, x'2, x'3, x'4, x'5],
                  ...] """
        return self.__dist_x

    def get_y(self):
        """ returns a list of lists, each list represents a run, and its elements are the y distance value for each step
        example: [[y1, y2, y3, y4, y5],
                 [y'1, y'2, y'3, y'4, y'5],
                  ...] """
        return self.__dist_y

    def get_num_steps(self) -> int:
        """ returns the number of steps for the simulation"""
        return self.__num_steps

    def get_num_runs(self) -> int:
        return self.__num_runs

    def get_y_crossing_data(self):
        """ returns the data of the y crossing after the simulation"""
        return self.__number_y_axis_crossings

    def get_y_prob_crossing_data(self):
        """ returns the data of the probability to crossing after the simulation"""
        return self.__probability_y_axis_crossings

    def __crossing(self, is_positive: bool, current_x: float):
        """ This method will check if the walker crossed the y-axis,
        positive is a boolean that represents if the walker is on the positive side of the x-axis,
        current_x is the current x value of the walker."""
        if is_positive:
            if current_x < 0:
                # crossed the y-axis, we need to update the state of the is positive to False
                return False, 1
            else:
                return True, 0
        else:
            if current_x > 0:
                # crossed the y-axis, we need to update the state of the is positive (it was False, and now it's True)
                return True, 1
            else:
                return False, 0


class Stats:
    """ This class will calculate the statistics of the random walk."""
    def __init__(self, simulation: Simulator):
        self.__simulation = simulation
        self.__magnitude_data = None
        self.__distance_from_x_data = None
        self.__distance_from_y_data = None
        self.__y_axis_crossings = None
        self.__y_prob_crossings = None

    def __mean_data(self, data: list[list[float]]) -> list[float]:
        """ This method will calculate the mean of any given data (list of lists) and return a list of the means"""
        mean_list = []
        for step in range(len(data[0])):
            sum_all_runs_per_step = 0
            for run in data:
                sum_all_runs_per_step += run[step]
            mean = sum_all_runs_per_step / len(data)
            mean_list.append(mean)
        return mean_list

    def get_mean_distance(self):
        """ Calculate the mean distance from the starting point
        for a given number of steps and a given number of runs."""
        if self.__magnitude_data is None:
            self.__magnitude_data = self.__mean_data(self.__simulation.get_magnitude())
        return self.__magnitude_data

    def get_mean_exit_time_radius(self, radius: int = 10) -> int:
        """ This method will calculate the mean time to reach a given radius"""
        if self.__magnitude_data is None:
            self.get_mean_distance()
        for step in range(len(self.__magnitude_data)):
            if self.__magnitude_data[step] > radius:
                mean_exit_times = step
                return mean_exit_times

    def get_mean_dis_from_x(self):
        """ updates the mean distance from the x-axis to the
        self.distance_from_x_data attribute with list of means for each step."""
        if self.__distance_from_x_data is None:  # Should it be self.distance_from_y_data?
            self.__distance_from_x_data = self.__mean_data(self.__simulation.get_x())
        return self.__distance_from_x_data

    def get_mean_dis_from_y(self):
        """ updates the mean distance from the y-axis to the
        self.distance_from_y_data attribute with list of means for each step."""
        if self.__distance_from_y_data is None:
            self.__distance_from_y_data = self.__mean_data(self.__simulation.get_y())
        return self.__distance_from_y_data

    def get_mean_y_axis_crossings(self):
        """ This method will calculate the mean number of times the walker crosses the y-axis"""
        if self.__y_axis_crossings is None:
            self.__y_axis_crossings = self.__mean_data(self.__simulation.get_y_crossing_data())
        return self.__y_axis_crossings

    def get_prob_mean_y_axis_crossings(self):
        """ This method will calculate the mean number of times the walker crosses the y-axis"""
        if self.__y_prob_crossings is None:
            self.__y_prob_crossings = self.__mean_data(self.__simulation.get_y_crossing_data())
        return self.__y_prob_crossings

    def get_sim_all_data(self):
        """ This method will return all the data of the simulation"""
        list_of_data = [self.get_mean_distance(),
                        self.get_mean_dis_from_x(),
                        self.get_mean_dis_from_y(),
                        self.get_mean_y_axis_crossings(),
                        self.get_prob_mean_y_axis_crossings()]
        return list_of_data

    def save_stat_csv(self, file_name: str):
        with open(f'{file_name}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            # Assuming the first row to be headers
            headers = ["Mean Distance", "Mean Distance from X", "Mean Distance from Y",
                       "Mean Y-Axis Crossings", "Probability Mean Y-Axis Crossings"]
            writer.writerow(headers)
            # Writing the statistics data
            writer.writerows(zip(*self.get_sim_all_data()))


class Plots:
    """ This class create plots (with matplotlib library) of the statistics of the random walk.
    The class can create 6 plot types:
    1. Mean distance from starting point
    2. The mean time (number of steps) to exit a given radius
    3. Mean distance from x-axis
    4. Mean distance from y-axis
    5. Number of times the walker crosses the y-axis
    6. (EXTRA!) Probability of crossing the y-axis

    All plots use the 'generic_plot' and the 'show_and_save_plot' method to show the plot, and save if needed.
     """
    def __init__(self):
        pass

    def __generic_plot(self, data: list[float], x_label, y_label, title) -> None:
        """ Plot generic data with customizable labels and title. """
        y = data
        x = []
        for i in range(len(y)):
            x.append(i)
        plt.plot(x, y, color='purple', linewidth=2)
        plt.xlabel(x_label, fontsize=14, fontweight='bold', color='#900C3F', fontname='Comic Sans MS')
        plt.ylabel(y_label, fontsize=14, fontweight='bold', color='#900C3F', fontname='Comic Sans MS', labelpad=20)
        plt.title(title, fontsize=15, fontweight='heavy', color='#FF33CE', fontname='Comic Sans MS', style='italic')
        plt.xticks(fontsize=12, fontname='Arial')  # Change font and size of x-axis ticks
        plt.yticks(fontsize=10, fontname='Arial')
        plt.grid(True, linestyle='--', alpha=0.5)  # Add grid with custom line style and transparency

    def __display_plot(self) -> None:
        """ Display the plot without saving. """
        plt.show()

    def __show_and_save_plot(self, save_plot: bool, file_name: str) -> bool:
        """ Save the plot to a file. """
        if save_plot:
            plt.savefig(file_name + '.png', dpi=300, bbox_inches='tight')
            self.__display_plot()
            plt.close()
            return True
        else:
            self.__display_plot()
            return False

    def get_mean_distance_plot(self, statistics: Stats,
                               save_plot: bool = False,
                               file_name: str = 'mean_distance_plot') -> None:

        """ Plot mean distance from starting point. """
        title = f"Mean distance from starting point for {len(statistics.get_mean_distance()) - 1} steps"
        self.__generic_plot(statistics.get_mean_distance(), "Number of steps", "Mean distance from"
                                                                               " starting point", title)
        self.__show_and_save_plot(save_plot, file_name)

    def get_time_exit_radius(self, statistics: Stats, radius: float = 10,
                             save_plot: bool = False,
                             file_name: str = f"time_to_ex_radius") -> None:

        """ Plot mean time (time = num steps) to exit_radius """
        title = f"Mean time (num step) to exit a radius of {radius}"
        self.__generic_plot(statistics.get_mean_distance(), "Number of steps",
                            "Mean distance from starting point", title)
        # Find intersection point
        intersection_x = None
        intersection_y = radius  # Marking the intersection point at (x, radius)
        for i in range(len(statistics.get_mean_distance())):
            if statistics.get_mean_distance()[i] >= radius:
                if i == 0:  # If the first point already crosses the radius
                    intersection_x = 1
                else:
                    # Interpolate to find more accurate x-coordinate
                    fraction = ((radius - statistics.get_mean_distance()[i - 1]) /
                                (statistics.get_mean_distance()[i] - statistics.get_mean_distance()[i - 1]))
                    intersection_x = i + round(fraction, 2)
                break

        # Mark intersection point
        if intersection_x is not None:
            plt.plot(intersection_x, intersection_y, 'ro')  # Red circle marker

            # Add annotation for intersection point
            plt.text(intersection_x, intersection_y, f'({intersection_x}, {intersection_y})',
                     fontsize=16, ha='left', va='bottom')

        self.__show_and_save_plot(save_plot, file_name)

    def get_mean_x_distance_plot(self, statistics: Stats,
                                 save_plot: bool = False,
                                 file_name: str = 'mean_X_dist_plot') -> None:

        """ Plot distance from x-axis vs N steps. """
        title = (f"Mean distance from from X Axis for"
                 f" {len(statistics.get_mean_dis_from_x()) -1} steps")
        self.__generic_plot(statistics.get_mean_dis_from_x(),
                            "Number of Steps", "Average Distance from X Axis", title)
        self.__show_and_save_plot(save_plot, file_name)

    def get_mean_y_distance_plot(self, statistics: Stats,
                                 save_plot: bool = False,
                                 file_name: str = 'mean_Y_dist_plot') -> None:

        """ Plot distance from y-axis vs N steps. """
        title = (f"Mean distance from from Y Axis for "
                 f"{len(statistics.get_mean_dis_from_y()) -1} steps")
        self.__generic_plot(statistics.get_mean_dis_from_y(),
                            "Number of Steps", "Average Distance from Y Axis", title)
        self.__show_and_save_plot(save_plot, file_name)

    def get_probability_mean_y_axis_crossings_plot(self, statistics: Stats,
                                                   save_plot: bool = False,
                                                   file_name: str = 'Prob_Y_cross_plot') -> None:

        """ Plot mean number of times the walker crosses the y-axis. """
        title = (f" Mean num of probability for the walker to cross the y-axis for "
                 f"{len(statistics.get_prob_mean_y_axis_crossings()) -1} steps")
        self.__generic_plot(statistics.get_prob_mean_y_axis_crossings(),
                            "Number of Steps", "Probability of Crossings", title)
        self.__show_and_save_plot(save_plot, file_name)

    def get_mean_y_axis_crossings_plot(self, statistics: Stats, save_plot: bool = False,
                                       file_name: str = 'mean_y_cross_plot') -> None:

        """ Plot mean number of times the walker crosses the y-axis. """
        title = (f" Mean number of times the walker crosses the y-axis for "
                 f"{len(statistics.get_mean_y_axis_crossings()) -1} steps")
        self.__generic_plot(statistics.get_mean_y_axis_crossings(),
                            "Number of Steps", "Number of Crossings", title)
        self.__show_and_save_plot(save_plot, file_name)
