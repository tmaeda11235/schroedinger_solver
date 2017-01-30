from time import time  # noqa
import scipy as sp  # noqa
import schrpy as sch  # noqr
for a in [round(l * 0.01, 4) for l in range(0, 100, 5)]:
    b = 5.0
    k = 1.0
    testpot = sch.us_KP_potential(8., a, b)
    xo = sch.gaussian(-15, 1., k).func
    solver = sch.schroedinger(testpot, xo, dx=0.005, dt=0.005)
    t = time()
    Z = solver.solve()
    print('spent', time() - t, 'seconds.')
    sp.save('uskp_a:{}_b:{}_k:{}.npy'.format(a, b, k), Z)
    print('Saved as uskp_a:{}_b:{}_k:{}.npy'.format(a, b, k))
