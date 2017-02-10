import scipy as sc
import matplotlib.pyplot as plt


x = sc.arange(-60, 60, 0.001)
z = sc.load('eigenvec.npy')
print(z[:, -1].shape)
print(x.shape)
fig = plt.figure()
for k in range(0, 50):
    plt.plot(x, sc.absolute(z[:, k]))
    plt.show()
