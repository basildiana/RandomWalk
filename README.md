# RandomWalk
OOP Python implementation of random walk in n dimensions. includes vector operations: addition, subtraction, scalar arithmetic, magnitude calculations, normalization. Designed as a foundation for random walk simulations




Extra Features to the simulation:


#1 Extended Walker Dynamics:
Beyond basic requirements, the simulation introduces modular walker types with traits such as:
    1) a customizable RESTART option for the walker
    (The walker can "jump" to the the the start location (0,0) in mid simulation,
    The user can choose 2 options: a constant probability (1%) or changing probability where when the walker
    is more far from the starting point he is more likely to "jump" into the start location
    2) a customizable degree of walker bias (from 0-100% with steps of 10%)
    3) random step length abilities (0.5-1.5) to ALL type of walkers

#2 SLOW Areas + Interactive Simulation Environment(Obstacles):
Drawing inspiration from space and astronomical black holes, the simulation landscape can be filled with obstacles,
teleporting areas, and SLOWER areas which look like...... CIRCLES in the space :),
All of which are  customizable to user specifications. (The user types the desired x,y locations and radius)

#3 Enhanced Plots Abilities:
The simulation allows some extra abilities in the plots:
    1) The user can choose the radius of the plot that the walker has exited (not only the radius of 10)
    2) The user can see an extra plot about the probability of the walker cross the y axis in the space.

 ==============================

Enhanced Overview of Two Notable Features:

1) Dynamic Restart Mechanism:
The restart walker functionality can be divided into two modes of operation:
* Constant Probability Mode: the walker has 1% likelihood of reinitialization to the origin coordinates (0,0)
at every step. This introduces a deterministic element to the stochastic nature of the random walks.
* Distance-Proportional Probability Mode: This mode adjusts the reset probability in proportion to the walker's
magnitude from the origin. The further the walker strays, the higher the probability of a reset,
thereby simulating a "pseudo-gravitational" pull towards the starting point.

2) Slower Zones:
The concept of slow areas is introduced to adjust the walker's speed based on where they are.
This brings in two main scenarios:
*SLOW Areas: If the walker enters the predefined slow zone, like a circle, it moves slower,
as if the area is more challenging to navigate. T
* Normal Speed Everywhere Else: Outside these special zones, the walker moves at its usual speed,
