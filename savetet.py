import scipy as sc
import matplotlib.pyplot as plt
# import mpl_toolkits.mplot3d as mpl3d
x, y = sc.meshgrid(sc.arange(-60, 60, 0.005), sc.arange(0, 20, 0.005))
z = sc.load('highacc.npy')
fig = plt.figure()
# fig.add_subplot(1, 1, 1, projection='3d')
# aa = mpl3d.Axes3D(fig)
# aa.contour(x, y, sc.absolute(z[1:])**2, 10, rstride=400, cstride=2000)
plt.pcolor(x[::10, ::10], y[::10, ::10], sc.absolute(z[1::10,::10]) ** 2)
plt.colorbar()
plt.show()
