

import numpy as np
from numpy.random import random



def random_position(center, radius):
    radius = radius * np.sqrt(random())
    angle = 2 * np.pi * random()

    return np.array([
        center[0] + radius * np.cos(angle),
        center[1] + radius * np.sin(angle)
    ])


