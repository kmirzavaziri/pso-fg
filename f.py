import math
import numpy as np

import utils


f = lambda x, y: abs(np.sin(x) * np.cos(y) * np.exp(np.abs(1 - (np.sqrt(np.power(x, 2) + np.power(y, 2)) / math.pi))))
x_range = [-10, 10]
y_range = [-10, 10]

ITERATIONS_COUNT = 20
VISUALIZER = utils.Visualizer(2, 3)

BETTER = lambda x, y: x > y
BEST = max
SQRT_COUNT = 40
OMEGA = .3
C_1 = .3
C_2 = .3
C_3 = 1
T = 1
COOLING_RATIO = .99

PRINTING_ITERATIONS = range(0, ITERATIONS_COUNT + 1, ITERATIONS_COUNT // 10 or 1)
VISUALIZING_ITERATIONS = range(0, ITERATIONS_COUNT + 1, ITERATIONS_COUNT // 5 or 1)

swarm = utils.Swarm(
    f, x_range, y_range,
    ITERATIONS_COUNT, VISUALIZER,
    BETTER, BEST, SQRT_COUNT, OMEGA, C_1, C_2, C_3, T, COOLING_RATIO
)
swarm.run(PRINTING_ITERATIONS, VISUALIZING_ITERATIONS, 'f.png')
