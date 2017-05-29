from time import time  # noqa
import scipy as sp  # noqa
import schrpy as sch  # noqr
import matplotlib.pyplot as plt
import os.path as pth
import itertools as itools
x, y = sp.meshgrid(sp.arange(-60, 60, 0.05), sp.arange(0, 30, 0.05))
V = [round(l * 0.1, 4) for l in range(60, 70, 5)]
A = [round(l * 0.1, 4) for l in range(2, 20, 2)]
B = [round(l * 0.1, 4) for l in range(1, 10, 1)]
K = [2.0]
itr = itools.product(V, A, B, K)
for (v, a, b, k) in itr:
    if not pth.isfile('data/uskp_v[{}]a[{}]b[{}]k[{}].npy'.format(v, a, b, k),):
        testpot = sch.us_KP_potential(v, a, b)
        xo = sch.gaussian(-15, 3., k).func
        solver = sch.schroedinger(testpot, xo, dx=0.05, dt=0.05, tmax=30)
        t = time()
        Z = solver.solve()
        print('spent', time() - t, 'seconds.')
        sp.save('data/uskp_v[{}]a[{}]b[{}]k[{}].npy'.format(v, a, b, k), Z)
        print('Saved as uskp_v[{}]a[{}]b[{}]k[{}].npy'.format(v, a, b, k))
        plt.pcolor(x[::5, ::5], y[::5, ::5], sp.absolute(Z[1::5, ::5]) ** 2)
        plt.colorbar()
        plt.savefig('pic/uskp_v[{}]a[{}]b[{}]k[{}].png'.format(v, a, b, k))
        plt.clf()
        print('Saved as uskp_v[{}]a[{}]b[{}]k[{}].png\n\n'.format(v, a, b, k))
    else:
        print('It has been saved  as uskp_v[{}]a[{}]b[{}]k[{}].png\n\n'.format(v, a, b, k))
