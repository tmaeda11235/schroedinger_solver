import scipy as sc
import matplotlib.pyplot as plt
import matplotlib.lines as line


x = sc.arange(-60, 61, 0.01)
z = sc.load('eigvec.npy')
v = sc.load('eigval.npy')
print(z[:, -1].shape)
print(x.shape)
plt.plot(sc.absolute(v), 'o')
plt.show()
plt.clf()
fig = plt.figure()
for param in range(0, 150, 5):
    for k in range(param, param + 5):
        fig.add_subplot(5, 1, k - param +1)
        pp = plt.plot(x, sc.absolute(z[:, k]))
        plt.xlim(-60, 60)
        #plt.ylim(0, 0.03)
    plt.savefig("eig{0:03d}.png".format(param))
    plt.clf()
