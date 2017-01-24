import matplotlib.pyplot as plt  # noqa
from time import time  # noqa
import scipy as sp  # noqa
import schrpy as sch  # noqa


testpot = sch.KP_potential(7, 5, 1)
xo = sch.gaussian(2.5, 0.1, 0.1).func
solver = sch.schroedinger(testpot, xo)
t = time()
solver.solve()
print(time() - t)
