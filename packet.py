import scipy as sc
import matplotlib.pyplot as plt
import schrpy as sch

x = sc.arange(-60, 60, 0.001)
z = sc.load('eigenvec.npy')
xo = sch.gaussian(3, 1, 1).func(x)
coeff = sc.matmul(xo, z)
print(coeff.shape)
print(x.shape)
fig = plt.figure()
fig.add_subplot(211)
plt.plot(sc.absolute(coeff))
fig.add_subplot(212)
x1 = sc.matmul(z, coeff)
plt.plot(x, sc.absolute(x1))
plt.show(fig)
