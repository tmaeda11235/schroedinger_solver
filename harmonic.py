import scipy as sc
from scipy.special import eval_hermite
from scipy.linalg import norm
import matplotlib.pyplot as plt
import matplotlib.lines as line


x = sc.arange(-10, 10, 0.01)
z = sc.load('harmonicVec.npy')
v = sc.load('harmonicVal.npy')
z0 = lambda n: eval_hermite(n, x) * sc.e ** (- 0.5 * x ** 2)
z1 = lambda k: z0(k) / norm(z0(k))
print(z0(1).shape)
plt.plot(sc.absolute(sc.absolute(v)-sc.arange(0.5, 30.5,)), 'o')
plt.semilogy()
plt.show()
plt.clf()
plt.plot(sc.absolute(v), 'o', sc.arange(0.5, 30.5,), '-')
plt.show()
plt.clf()
fig = plt.figure()
for param in range(0, 30, 5):
    for k in range(param, param + 5):
        fig.add_subplot(5, 1, k - param +1)
        plt.plot(x, sc.absolute(sc.absolute(z[:, k]) - sc.absolute(z1(k))))
        #plt.plot(x, sc.absolute(z[:, k]))
        #plt.plot(x, sc.absolute(z1(k)))
        plt.semilogy()
        plt.xlim(-10, 10)
        plt.ylim(0., 0.08)
        plt.savefig("HeigError{0:03d}.png".format(param))
    plt.clf()
