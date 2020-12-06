import os
import random
import numpy as np
from math import sin, cos, degrees
from numpy import dot, arccos, arcsin
import map.noise.prereq

random.seed(a=os.urandom(1024))

def twod_vectorize():
    angle = random.randint(0, 360)
    return [(sin(angle)), (cos(angle))]
    # return [(random.randrange(-100, 101, 1)/100), (random.randrange(-100, 101, 1)/100)]

def vector_grid(x, y):
    grid = []

    for i in range(y + 1):
        grid.append([])

    for i in grid:
        random.seed(a=os.urandom(1024))
        for j in range(x + 1):
            i.append(twod_vectorize())
    return grid

def final_noise(x, y):
    vectors = vector_grid(10, 10)
    for counti, i in enumerate(vectors):
        for countj, j in enumerate(i):
            components = []
            if counti > 0:
                components.append((vectors[i - 1])[j - 1])
                if countj > 0:
                    components.append((vectors[i - 1])[j - 1])
            if countj > 0:
                components.append((vectors[i])[j - 1])
            components.append((vectors[i])[j])
            for i in components:
                pass




# grid = final_noise(10, 10)
# print(grid)

#numpy based version

def generate_perlin_noise_2d(shape, res):
    def f(t):
        return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = np.mgrid[0:res[0]:delta[0], 0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2 * np.pi * np.random.rand(res[0] + 1, res[1] + 1)
    gradients = np.dstack((np.cos(angles), np.sin(angles)))
    g00 = gradients[0:-1, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1, 1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:, 1:].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = np.sum(grid * g00, 2)
    n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, 2)
    n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, 2)
    n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
    n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11
    return np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)

def generate_fractal_noise_2d(shape, res, octaves=1, persistence=0.5):
    noise = np.zeros(shape)
    frequency = 1
    amplitude = 1
    for _ in range(octaves):
        noise += amplitude * generate_perlin_noise_2d(shape, (frequency*res[0], frequency*res[1]))
        frequency *= 2
        amplitude *= persistence
    return noise

# print(generate_perlin_noise_2d((2, 4), (4, 8)))

