import scipy as sc
import matplotlib.pyplot as plt
import matplotlib.lines as line


x = sc.arange(-10, 10, 0.01)
z = sc.load('harmonicVec.npy')
v = sc.load('harmonicVal.npy')
#z = sc.load('eigvec.npy')
#v = sc.load('eigval.npy')
print(z[:, -1].shape)
print(x.shape)
print(sc.absolute(v)-sc.arange(0.5, 30.5,), 'o')
plt.plot(sc.absolute(sc.absolute(v)-sc.arange(0.5, 30.5,)), 'o')
plt.semilogy()
plt.ylim(10**-13, 10**-8)
plt.show()
plt.clf()
plt.plot(sc.absolute(v), 'o', sc.arange(0.5, 30.5,), '-')
plt.show()
plt.clf()
fig = plt.figure()
for param in range(0, 30, 5):
    for k in range(param, param + 5):
        fig.add_subplot(5, 1, k - param +1)
        pp = plt.plot(x, sc.absolute(z[:, k]))
        plt.xlim(-10, 10)
        plt.ylim(0, 0.08)
    plt.savefig("Heig{0:03d}.png".format(param))
    plt.clf()
