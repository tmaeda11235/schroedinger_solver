import scipy as sc
import matplotlib.pyplot as plt
x, y = sc.meshgrid(sc.arange(-60, 60, 0.005), sc.arange(0, 20, 0.005))
z = sc.load('uskp_a[0.05]b[5.0]k[1.0].npy')
fig = plt.figure()
plt.pcolor(x[::10, ::10], y[::10, ::10], sc.absolute(z[1::10, ::10]) ** 2)
plt.colorbar()
plt.show()