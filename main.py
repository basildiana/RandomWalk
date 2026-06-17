from Fields import Field, Obstacles, TeleportingArea, SlowArea
from Walkers import Walker360, WalkerDiscrete
from Sim import Simulator, Stats, Plots
from Inputs import UserInput
import sys


def main():
    user_input = UserInput()

    # Phase 1: Get walker data, and create walker object, add it to field

    walker_type, random_step, bias, direction, return_to_start, constant_return = user_input.check_walker_input()
    if walker_type == "360":
        walker = Walker360(random_step=random_step, bias=bias, direction=direction,
                           return_to_start=return_to_start,
                           constant_return=constant_return)
    else:
        walker = WalkerDiscrete(random_step=random_step, bias=bias, direction=direction,
                                return_to_start=return_to_start, constant_return=constant_return)

    field = Field()
    field.add_walker(walker)

    # Phase 2: Get obstacles data

    if bias != 10:
        # The feature of adding obstacles is only available for walkers who are not 100% biased
        # ( Because the user could block the walker's path and the program will loop to infinity)
        while True:
            obstacles_data = user_input.get_obstacle_data()  # Gather obstacle data
            obstacles_to_add = len(obstacles_data)  # Count of obstacles to attempt to add
            obstacles_added_successfully = 0  # Counter for successfully added obstacles

            for obstacle_data in obstacles_data:
                x, y, radius = obstacle_data
                obstacle = Obstacles(x, y, radius)  # Create the obstacle object
                if field.add_obstacle(obstacle):  # Attempt to add the obstacle, check if successful
                    obstacles_added_successfully += 1
                else:
                    print(f"Could not add obstacle at ({x}, {y}) with radius {radius}. It violates field rules.")

            if obstacles_added_successfully == obstacles_to_add and obstacles_to_add > 0:
                print("All obstacles added successfully.")
                break  # Exit the while-loop; all obstacles processed successfully
            elif obstacles_to_add == 0:
                break
            else:
                if len(field.get_obstacles()) == 0:
                    print("No obstacles in the space.")
                else:
                    print(f"Those are the obstacles which were added successfully: {field.get_obstacles()}")
                user_choice = user_input.ask_to_continue_adding()
                if not user_choice:
                    print("\nContinuing without adding more obstacles.")
                    break  # User chooses not to add more obstacles, exit the main loop

    # Phase 3: Create teleporting area and get its data

    while True:
        teleporting_area_data = user_input.get_teleporting_area_data()  # Gather teleporting area data
        areas_to_add = len(teleporting_area_data)  # Count of teleporting areas to attempt to add
        areas_added_successfully = 0  # Counter for successfully added teleporting areas

        for area_data in teleporting_area_data:
            x, y, radius, x_teleported, y_teleported = area_data
            teleporting_area = TeleportingArea(x, y, radius, x_teleported, y_teleported)
            if field.add_teleporting_area(teleporting_area):  # Attempt to add the teleporting area, check if successful
                areas_added_successfully += 1
            else:
                print(f"Could not add teleporting area at ({x}, {y}) with radius {radius}. It violates field rules.")

        if areas_added_successfully == areas_to_add and areas_to_add > 0:
            print("All teleporting areas added successfully.")
            break  # Exit the while-loop; all areas processed successfully
        elif areas_to_add == 0:
            break
        else:
            if len(field.get_teleporting_areas()) == 0:
                print("No teleporting areas in the space.")
            else:
                print(f"Those are the teleporting areas which were added successfully: {field.get_teleporting_areas()}")
            user_choice = user_input.ask_to_continue_adding()
            if not user_choice:
                print("\nContinuing without adding more teleporting areas.")
                break  # User chooses not to add more areas, exit the main loop

    # Phase 4: Create slow area and get its data

    while True:
        slow_areas_data = user_input.get_slow_area_data()  # Gather slow area data
        for slow_area_data in slow_areas_data:
            x, y, radius = slow_area_data
            slow_area = SlowArea(x, y, radius)  # Create the slow area object
            field.add_slow_area(slow_area)  # add the slow area
        if len(field.get_slow_areas()) != 0:
            print(f"Those are the slow areas added successfully: {field.get_slow_areas()}")
        break  # the slow areas were added exit the  loop

    # Phase 5: Create simulator object, and run the simulation

    print("\nLets gather some info for the simulation!\n")
    num_steps, num_runs = user_input.get_simulator_data()
    print(f"Great choice! {num_steps} step and {num_runs} runs. Let's get started!")
    simulation = Simulator(field, num_steps, num_runs)
    simulation.run_sim()
    print("Simulation is done!")
    stats = Stats(simulation)

    # Phase 6: Raw Data, Get user input  whether they want to save raw stats
    print("\nThere is raw data from the simulation!")
    if user_input.want_to_save():
        stats.save_stat_csv(user_input.get_filename())  # Save raw data to a file

    # Phase 7: Get user's plot choices and whether they want to save them

    plotter = Plots()
    for choice, save_plot, filename, radius in user_input.decide_on_plots():
        if choice is None:  # No more plots to show
            break
        if choice == 1:
            plotter.get_mean_distance_plot(stats, save_plot, filename)
        elif choice == 2:
            plotter.get_time_exit_radius(stats, radius, save_plot, filename)
        elif choice == 3:
            plotter.get_mean_x_distance_plot(stats, save_plot, filename)
        elif choice == 4:
            plotter.get_mean_y_distance_plot(stats, save_plot, filename)
        elif choice == 5:
            plotter.get_mean_y_axis_crossings_plot(stats, save_plot, filename)
        elif choice == 6:
            plotter.get_probability_mean_y_axis_crossings_plot(stats, save_plot, filename)
    print("\nGreat, Hope You Enjoyed My Random Walk, Stay Unpredictable :) !")


def print_help_message():
    help_message = (
        "Welcome to the Random Walk Simulation Program!\n"
        "This script allows you to simulate various types of random walks\n\n "
        "\nPlease Open the program in the main.py file and run it from the pycharm or vscode interface,"
        "or please write main.py play \n\n"
        "The program will guide you through setting up your simulation, asking for input on walker type and more!" 
        " You will be able to customize your simulation with different parameters, such as the type of walker,"
        "directional bias, and even include unique simulation features like obstacles or slower zones.\n\n"
        "Start your adventure into the unpredictable world of random walks by answering the prompts, "
        "and let the simulation begin!")
    return help_message


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            print(print_help_message())
            exit(0)
        if sys.argv[1] == "play":
            main()
    else:
        main()
