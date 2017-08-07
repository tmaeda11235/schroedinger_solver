import schrpy as sp
import scipy as sc
import matplotlib.pyplot as plt


class Note:
    def __init__(self, xmin, xmax, dx, tmin, tmax, dt):
        self.mesh = sp.Mesh(xmin, xmax, dx, tmin, tmax, dt)
        self.potential = sp.Potential(self.mesh, lambda x: 0 * x)
        self.initial = sp.GaussianState(self.mesh, 0, 1, 0)
        self.solution = None

    def set_potential(self, potential):
        if potential.mesh_param == self.mesh.param:
            self.potential = potential
        else:
            print("Different meshes have imputed. ")
            raise AssertionError

    def set_initial(self, state):
        if state.mesh_param == self.mesh.param:
            self.initial = state
        else:
            print("Different meshes have imputed. ")
            raise AssertionError

    def solve_schroedinger_equation(self):
        self.solution = sp.Schroedinger(self.potential, self.initial, self.mesh).solve()
        return self.solution

    def save_solution(self, file_name):
        sc.save(file_name, self.solution)

    def easy_plot2d(self, max_pix=(1000, 1000), save=False, title="no_title"):
        x_step = int(self.mesh.x_num / max_pix[0]) + 1
        t_step = int(self.mesh.x_num / max_pix[1]) + 1
        x_grid = self.mesh.x_matrix[::t_step, ::x_step]
        t_grid = self.mesh.t_matrix[::t_step, ::x_step]
        phi2 = sc.absolute(self.solution[1::t_step, ::x_step]) ** 2
        potential = self.potential.vector()[::x_step]
        x = self.mesh.x_vector[::x_step]

        fig = plt.figure()
        above = fig.add_axes((0.05, 0.25, 0.91, 0.7))
        under = fig.add_axes((0.05, 0.05, 0.91, 0.17), sharex=above)
        above.set_title(title)
        above.tick_params(labelbottom="off")
        under.tick_params(labelleft="off")

        above.pcolor(x_grid, t_grid, phi2)
        under.plot(x, potential)
        if save:
            fig.savefig(title + ".png")
        return fig
