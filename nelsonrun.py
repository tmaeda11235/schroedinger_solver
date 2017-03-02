import schrpy as sch
import scipy as sci

cache = sci.zeros((1000, 1000000))
psi = sci.load('uskp_a[0.05]b[5.0]k[1.0].npy')[:-1] + 2 ** -50
x = sci.arange(-60, 60, 0.005)
t = sci.arange(0, 20, 0.005)
init = sch.gaussian(-15, 1., 1.)
nel = sch.nelson(x, t, psi, init)
k = 0
s = 0
while nel.t <= 20.:
    cache[k] = nel.run(0.001)
    k += 1
    print('\r{}.{} doing! '.format(s, k), end='  ')
    if k == 1000:
        sci.save("RW_{}.npy".format(s), cache)
        s += 1
        k = 0