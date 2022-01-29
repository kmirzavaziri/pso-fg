from random import random, uniform
import numpy as np
import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, rows, cols):
        self.fig = plt.figure(figsize=(20, 10))
        self.axs = []
        for i in range(rows * cols):
            ax = self.fig.add_subplot(rows, cols, i + 1, projection='3d')
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.view_init(elev=90, azim=-90)
            self.axs.append(ax)

        self.counter = 0

        plt.subplots_adjust(wspace=0, hspace=0.3)

    def add(self, x_range, y_range, func, particles=[], *, title=''):
        x = np.linspace(*x_range, 100)
        y = np.linspace(*y_range, 100)
        X, Y = np.meshgrid(x, y)
        Z = func(X, Y)
        self.axs[self.counter].contour3D(X, Y, Z, 400, cmap='Blues')
        particles_x = []
        particles_y = []
        particles_z = []
        for particle in particles:
            particles_x.append(particle.x)
            particles_y.append(particle.y)
            particles_z.append(particle.z)
        self.axs[self.counter].scatter(particles_x, particles_y, particles_z, s=15, c='red')
        self.axs[self.counter].set_title(title)
        self.counter += 1

    def show(self, filename=None):
        if filename:
            self.fig.savefig(filename, dpi=300)
        plt.show()


class Particle:
    def __init__(self, x, y, func, x_range, y_range, better, omega, c_1, c_2, c_3, t, cooling_ratio):
        self.func = func
        self.x_range = x_range
        self.y_range = y_range
        self.better = better
        self.omega = omega
        self.c_1 = c_1
        self.c_2 = c_2
        self.c_3 = c_3
        self.t = t
        self.cooling_ratio = cooling_ratio

        self.x = x
        self.y = y
        self.z = self.func(self.x, self.y)

        self.best = (self.x, self.y, self.z)
        self.v_x = 0
        self.v_y = 0

    def update(self, global_best):
        self.t *= self.cooling_ratio
        if self.z == global_best[2]:
            return

        self.v_x = (
            self.omega * self.v_x +
            self.c_1 * random() * (self.best[0] - self.x) +
            self.c_2 * random() * (global_best[0] - self.x) +
            self.c_3 * self.t * (.5 - random())
        )
        self.v_y = (
            self.omega * self.v_y +
            self.c_1 * random() * (self.best[1] - self.y) +
            self.c_2 * random() * (global_best[1] - self.y) +
            self.c_3 * self.t * (.5 - random())
        )

        new_x = self.x + self.v_x
        if new_x < self.x_range[0] or new_x > self.x_range[1]:
            self.v_x *= -.5
        self.x += self.v_x
        self.x = min(max(self.x, self.x_range[0]), self.x_range[1])

        new_y = self.y + self.v_y
        if new_y < self.y_range[0] or new_y > self.y_range[1]:
            self.v_y *= -.5
        self.y += self.v_y
        self.y = min(max(self.y, self.y_range[0]), self.y_range[1])

        self.z = self.func(self.x, self.y)
        if self.better(self.z, self.best[2]):
            self.best = (self.x, self.y, self.z)


class Swarm:
    def __init__(self, func, x_range, y_range, iterations_count, visualizer, better, best, sqrt_count, omega, c_1, c_2, c_3, t, cooling_ratio):
        self.func = func
        self.x_range = x_range
        self.y_range = y_range
        self.iterations_count = iterations_count
        self.visualizer = visualizer
        self.better = better
        self.best = best
        self.count = sqrt_count ** 2
        self.omega = omega
        self.c_1 = c_1
        self.c_2 = c_2
        self.c_3 = c_3
        self.t = t
        self.cooling_ratio = cooling_ratio

        self.particles = []
        for x in np.linspace(x_range[0] + .1, x_range[1] - .1, sqrt_count):
            for y in np.linspace(y_range[0] + .1, y_range[1] - .1, sqrt_count):
                self.particles.append(Particle(
                    x + (.5 - random()) / 5, y + (.5 - random()) / 5,
                    func, x_range, y_range, better, omega, c_1, c_2, c_3, t, cooling_ratio
                ))

    def run(self, printing_iterations=[], visualizing_iterations=[], output=None):
        for iteration in range(self.iterations_count + 1):
            values = [particle.z for particle in self.particles]
            global_best_index = values.index(self.best(values))
            global_best = (self.particles[global_best_index].x,
                           self.particles[global_best_index].y, self.particles[global_best_index].z)

            if iteration in printing_iterations:
                print(f'Iteration: {iteration}\tBest: {global_best}')
            if iteration in visualizing_iterations:
                self.visualizer.add(self.x_range, self.y_range, self.func, self.particles,
                                    title=f'Iteration {iteration}\nBest: {round(global_best[2], 2)}')

            for particle in self.particles:
                particle.update(global_best)

        self.visualizer.show(output)
