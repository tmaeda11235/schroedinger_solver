from schrpy import *
from time import time
from scipy import save
mesh = Mesh(-10, 10, 0.05, 0, 10, 0.05)
note = Note(mesh)
note.set_potential(Potential(mesh, lambda y: 5 * (0 < y) * (y < 1) + 5 * (3 < y) * (y < 4)))
note.set_initial(GaussianState(mesh, -3, 3, 3))
note.solve_schroedinger_equation(boundary="absorb")
note.easy_plot2d(save=True, title="aaaaaaa")

