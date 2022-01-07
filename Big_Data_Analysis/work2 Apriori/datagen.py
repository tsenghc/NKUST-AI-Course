import numpy as np
import random

_rd = []
for i in range(500):
    s = random.randint(2, 15)
    _rd.append(np.random.randint(low=1, high=20, size=(s)).tolist())


print(_rd)
np.savetxt("min.txt", _rd, delimiter=",", fmt="%s")
