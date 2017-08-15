from schrpy import Note
import schrpy as sp


mesh = sp.Mesh(-10, 10, 0.1, 0, 5, 0.1)
note = Note(mesh)
potential = sp.KPPotential(mesh, 5, 2, 1)
note.set_potential(potential)
initial_state = sp.GaussianState(mesh, -5, 1, 3)
note.set_initial(initial_state)
note.solve_schroedinger_equation()
note.easy_plot2d(title="test2", save=True)
