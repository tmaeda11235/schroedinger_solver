from schrpy import *
from scipy import *
from matplotlib.pyplot import figure
# import seaborn
# seaborn.set_style(style="darkgrid")
# seaborn.set_palette("bright", 2)
mesh = Mesh(-10, 10, 0.05, 0, 10, 0.05)
note = Note(mesh)
note.set_initial(GaussianState(mesh, -2, 3, 5))
note.set_potential(Potential(mesh, lambda x: (x < -8) + (x > 8)))
note.solve_schroedinger_equation(boundary="free")
note.easy_plot2d(save=True, title="free")
# note.solve_schroedinger_equation(boundary="fix")
# note.easy_plot2d(save=True, title="fix")
# note.solve_schroedinger_equation(boundary="period")
# note.easy_plot2d(save=True, title="period")
note.solve_schroedinger_equation(boundary="absorb")
note.easy_plot2d(save=True, title="absorb")

