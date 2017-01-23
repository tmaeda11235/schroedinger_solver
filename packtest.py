import matplotlib.pyplot as plt  # noqa
import schrpy.potential as pot  # noqa
import schrpy.schroedinger as sch  # noqa
import schrpy.laplasian as lap  # noqa
import scipy.stats as stt  # noqa
from time import time  # noqa
import scipy as sp  # noqa


testpot = pot.KP_potential(7, 5, 1)
xo = lambda l: stt.norm.pdf(l, 2.5, 0.5)
solver = sch.schroedinger(testpot, xo)
t = time()
solver.solve()
print(time() - t)
