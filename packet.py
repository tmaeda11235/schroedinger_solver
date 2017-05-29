import scipy as sc
import matplotlib.pyplot as plt
import schrpy as sch

x = sc.arange(-60, 61, 0.01)
z = sc.load('eigvec.npy')
xo = sch.gaussian(-15, 3, 2).func(x)
coeff = sc.matmul(xo.conj(), z)
print(coeff.shape)
print(x.shape)
fig = plt.figure()
fig.add_subplot(211)
plt.plot(sc.absolute(coeff))
plt.plot(sc.real(coeff))
plt.plot(sc.imag(coeff))
fig.add_subplot(212)
x1 = sc.matmul(z.conj(), coeff)
plt.plot(x, sc.absolute(x1))
plt.plot(x, sc.real(x1))
plt.plot(x, sc.imag(x1))
plt.show(fig)
