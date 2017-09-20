from schrpy import *
from scipy.integrate import trapz
import matplotlib.pyplot as plt
from scipy import *
from time import time
from scipy import save
mesh = Mesh(-15, 10, 0.05, 0, 120, 0.01)
note = Note(mesh)
note.set_potential(Potential(mesh, lambda y: 6 * ((0 < y) * (y < 1) + (3 < y) * (y < 4))))
note.set_initial(GaussianState(mesh, -5, 3, 3))
note.solve_schroedinger_equation(boundary="absorb")
note.easy_plot2d(save=True, title="Double-well")
s = trapz(absolute(note.solution[:, 310:370])**2)
plt.plot(mesh.t_vector, s)
plt.xlabel("time")
plt.ylabel("P(t)")
plt.yscale("log")
plt.xscale("log")
plt.show()