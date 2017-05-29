import scipy as sc
import matplotlib.pyplot as plt
x, y = sc.meshgrid(sc.arange(-60, 60, 0.05), sc.arange(0, 30, 0.05))
z = sc.load("step_potential3.npy")
fig = plt.figure()
plt.pcolor(x[::1, ::1], y[::1, ::1], sc.absolute(z[1::1, ::1]) ** 2)
plt.colorbar()
plt.show()