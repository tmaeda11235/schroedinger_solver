import scipy as sc
import matplotlib.pyplot as plt
import schrpy as sch

x = sc.arange(-60, 60, 0.02)
z = sc.load('eigenvec.npy')
xo = sch.gaussian(-30, 5, -1).func(x)
coeff = xo.dot(z)
print(coeff.shape)
print(x.shape)
fig = plt.figure()
plt.plot(sc.absolute(coeff))
plt.show()
x1 = z.dot(coeff)
plt.plot(x, sc.absolute(x1))
plt.show()
