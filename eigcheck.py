import schrpy as sc
import scipy as sp
import matplotlib.pyplot as plt

L = 10
N = 15
t = 0
dt = 0.001
dx = 0.01
x1 = sp.arange(-5, 5, dx)
x2 = sp.arange(-5, 5, dx) + 10
wave_number = [2 * sp.pi * (n + 0.5) / L for n in range(N)]
amplitude = sp.random.rand(N)


def base(i, x):
    return sp.cos(wave_number[i] * x)*(sp.absolute(x) < 0.499*L)


def xo(x):
    func = 0
    for i in range(N):
        func = func + amplitude[i] * base(i, x)
    return func

potential = sc.potential(lambda x: 4 * x ** 2)
solver = sc.schroedinger(potential, xo, xmax=5, xmin=-5, dx=dx).ode


def dynamic(before, after):
    dd = sp.absolute(after) ** 2 - sp.absolute(before) ** 2
    if dd.sum() ==0:
        print("{}\n".format(t))
        return False
    else:
        print("{}\n".format(t))
        return True


def draw(time):
    decant = 10 * time
    det = decant == int(decant)
    return det
a = 0
while dynamic(x1, x2):
    t += dt
    a += 1
    x1, x2 = (x2, solver.integrate(t))
    if a == 1:
        plt.plot(sp.absolute(x2)**2)
        plt.savefig('pic/harmonicTest{}.png'.format(t))
        plt.clf()
        a = 0

plt.plot(sp.absolute(x2)**2)
plt.savefig('pic/HarmonicTest1_{}.png'.format(t))
plt.clf()
