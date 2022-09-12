import numpy as np
import math
import random
def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def round_(x):
    c = math.ceil(x)
    f = math.floor(x)
    if random.uniform(0, 1) < (x-f):
        return c
    else:
        return f