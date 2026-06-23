# RandomWalk
OOP Python implementation of random walk in n dimensions. includes vector operations: addition, subtraction, scalar arithmetic, magnitude calculations, normalization. Designed as a foundation for random walk simulations

## Core Features:

### 1. Extended Walker Dynamics
The engine features customizable, modular walker types (`discrete` or `360-degree`) embedded with configurable dynamic behaviors:
* **Dynamic Restart Mechanism:** Employs a stochastic reset constraint. It can operate via a **Constant Probability Mode** (fixed $1\%$ reset likelihood per step) or a **Distance-Proportional Mode** where reset probability scales linearly with displacement magnitude from origin, simulating a pseudo-gravitational vector pull.
* **Directional Bias Tuning:** Implements localized vector weights from $0\%$ to $100\%$ heading toward specified targets (Origin, Left, Right, Up, Down).
* **Stochastic Variable Steps:** Supports step sizing dynamically randomized between $0.5$ and $1.5$ units.

### 2. Interactive Simulation Field & Obstacles
The landscape evaluates custom geometric coordinates as distinct boundary intersections:
* **Obstacles (Static Collisions):** Circular fields that block walker entry. Rules enforce that obstacles cannot cross the $(0,0)$ coordinate origin.
* **Slower Zones (Friction Fields):** Circular boundaries mimicking astronomical event horizons. When a walker enters, its maximum step velocity degrades gracefully ($0.5 \times$).
* **Teleportation Portals:** Paired entry/exit coordinate vectors that dynamically update the walker's internal spatial coordinate vector upon intersection.

### 3. Advanced Statistical Analytics & Plotting
The simulator captures aggregated trial runs to compute and plot macro-statistics:
* Mean displacement vectors relative to axes ($X$ and $Y$).
* Dynamic intersection interpolation (calculates exact steps required to exit a user-defined radius).
* Empirical probability distributions of $Y$-axis boundary crossings.

random_walk_simulator/
│
├── Vector.py       # Custom /nD linear algebra vector wrapper methods
├── Walkers.py      # Encapsulated Discrete or 360 Walker implementations
├── Fields.py       # Environment assets (Field, Obstacles, Teleporter, SlowArea)
├── Sim.py          # Simulator engine, Stats aggregator, and Plots pipeline
├── Inputs.py       # UserInput verification, string sanitizers, and range checkers
└── main.py         # CLI entrypoint and execution lifecycle

Quickstart help interface:
python main.py --help 
or init interactive simulation by: python main.py play

---

## System Architecture:

The simulation logic enforces a strict object-oriented structure where elements interact strictly via encapsulated vector methods:

```mermaid
graph TD
    A[main.py Entrypoint] --> B[UserInput Handler]
    A --> C[Simulator Engine]
    C --> D[Field Environment]
    D --> E[Walker Base Class]
    D --> F[Obstacles Circle]
    D --> G[TeleportingArea Circle]
    D --> H[SlowArea Circle]
    E --> I[Vector Vector Math]
    F & G & H --> I
    C --> J[Stats Processor]
    J --> K[Plots Visualizer via Matplotlib]


