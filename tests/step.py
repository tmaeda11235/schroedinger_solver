from time import time  # noqa
import scipy as sp  # noqa
import schrpy as sch  # noqa

testpot = sch.step_potential(10, 0)
xo = sch.gaussian(-15, 5., 2).func
solver = sch.schroedinger(testpot, xo, dx=0.05, dt=0.05, tmax=30)
t = time()
Z = solver.solve()
print('spent', time() - t, 'seconds.')
sp.save('step_potential3.npy', Z)
print('step_potential3.npy\n\n')