import secrets
from noise import pnoise2
import numpy as np
from PIL import Image

shape = (1500, 1000)
scale = .5
octaves = 6
persistence = 0.5
lacunarity = 2.0
seed = secrets.randbelow(100000)

world = np.zeros(shape)

# make coordinate grid on [0,1]^2
x_idx = np.linspace(0, 1, shape[0])
y_idx = np.linspace(0, 1, shape[1])
world_x, world_y = np.meshgrid(x_idx, y_idx)

# apply perlin noise, instead of np.vectorize, consider using itertools.starmap()
world = np.vectorize(pnoise2)(world_x / scale,
                              world_y / scale,
                              octaves=octaves,
                              persistence=persistence,
                              lacunarity=lacunarity,
                              repeatx=1500,
                              repeaty=1000,
                              base=seed)

# print(world)
img = np.floor((world + .5) * 255).astype(np.uint8)  # <- Normalize world first
fileimg = Image.fromarray(img, mode='L')
fileimg.save("../generated/img.png")
fileimg.show()
