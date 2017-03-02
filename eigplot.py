import scipy as sc
import matplotlib.pyplot as plt


x = sc.arange(-60, 60, 0.001)
z = sc.load('eigenvec.npy')
print(z[:, -1].shape)
print(x.shape)
fig = plt.figure()
param = 950
for k in range(param, param + 20):
    fig.add_subplot(10, 2, k - param +1)
    pp = plt.plot(x, sc.absolute(z[:, k]))
    plt.axis([-1., 0., -0.008, 0.008])
plt.show(fig)
