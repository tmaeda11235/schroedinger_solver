import schrpy as sch  # noqr
from time import time  # noqa
import scipy as sp  # noqa
import os.path as pth
import itertools as itools
V = [6.5]
A = [1.4]
B = [0.2]
K = [2.0]
itr = itools.product(V, A, B, K)
for (v, a, b, k) in itr:
    if not pth.isfile('H_uskp_v[{}]a[{}]b[{}]k[{}].npy'.format(v, a, b, k),):
        testpot = sch.us_KP_potential(v, a, b)
        xo = sch.gaussian(-15, 3., k).func
        solver = sch.schroedinger(testpot, xo, dx=0.005, dt=0.001, tmax=30)
        t = time()
        Z = solver.solve()
        print('spent', time() - t, 'seconds.')
        sp.save('Huskp_v[{}]a[{}]b[{}]k[{}].npy'.format(v, a, b, k), Z)
        print('Saved as uskp_v[{}]a[{}]b[{}]k[{}].npy'.format(v, a, b, k))
    else:
        print('It has been saved  as uskp_v[{}]a[{}]b[{}]k[{}].png\n\n'.format(v, a, b, k))
