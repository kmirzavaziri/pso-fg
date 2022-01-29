import math
import numpy as np

import utils


g = lambda x, y: x * np.sin(math.pi * np.cos(x) * np.tan(y)) * (np.sin(y / x) / (1 + np.cos(y / x)))
x_range = [-100, 100]
y_range = [-100, 100]

ITERATIONS_COUNT = 4000
VISUALIZER = utils.Visualizer(2, 3)

BETTER = lambda x, y: x < y
BEST = min
SQRT_COUNT = 40
OMEGA = 2
C_1 = 3
C_2 = 4
C_3 = 1
T = 1
COOLING_RATIO = .99

PRINTING_ITERATIONS = range(0, ITERATIONS_COUNT + 1, ITERATIONS_COUNT // 10 or 1)
VISUALIZING_ITERATIONS = range(0, ITERATIONS_COUNT + 1, ITERATIONS_COUNT // 5 or 1)

swarm = utils.Swarm(
    g, x_range, y_range,
    ITERATIONS_COUNT, VISUALIZER,
    BETTER, BEST, SQRT_COUNT, OMEGA, C_1, C_2, C_3, T, COOLING_RATIO
)
swarm.run(PRINTING_ITERATIONS, VISUALIZING_ITERATIONS, 'g.png')
