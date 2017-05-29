import schrpy as sch
import scipy as sci

cache = sci.zeros((100, 100000))
print("cache")
psi = sci.load('Huskp_v[6.5]a[1.4]b[0.2]k[2.0].npy')[:-15001] + 2 ** -50
print("psi")
x = sci.arange(-60, 60, 0.005)
print("x")
t = sci.arange(0, 15, 0.001)
print("t")
init = sci.random.normal(loc=-15, size=100000, scale=3.0)
print("init")
nel = sch.nelson(x, t, psi, init)
print("nel")
k = 0
s = 0
while nel.t <= 15.:
    cache[k] = nel.run(0.001)
    k += 1
    print('\r{}.{} doing! '.format(s, k), end='  ', flush=True)
    if k == 100:
        sci.save("RW_{}.npy".format(s), cache)
        s += 1
        k = 0
