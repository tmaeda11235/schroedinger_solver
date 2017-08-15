import schrpy as sp
import scipy as sc
from matplotlib.pyplot import figure


class Note:
    def __init__(self, mesh):
        self.mesh = mesh
        self.potential = sp.Potential(self.mesh, lambda x: 0 * x)
        self.initial = sp.GaussianState(self.mesh, 0, 1, 0)
        self.solution = None
        self.locus = None

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

    def solve_schroedinger_equation(self, boundary="free"):
        self.solution = sp.Schroedinger(self.mesh, self.potential, self.initial, boundary=boundary).solve()
        return self.solution

    def save_solution(self, file_name):
        sc.save(file_name, self.solution)

    def load_solution(self, file_name):
        sol = sc.load(file_name)
        if sol.shape == (self.mesh.t_num, self.mesh.x_num):
            self.solution = sol
        else:
            print("Different meshes have imputed")
            raise AssertionError

    def generate_locus(self, n, run_times=10):
        random_init = self.initial.random_values(n)
        nel = sp.Nelson(self.mesh, self.solution + 2 ** -50, random_init, run_times=run_times)
        self.locus = nel.locus()
        return self.locus

    def easy_plot2d(self, max_pix=(1000, 1000), show=True, save=False, title="no_title", limit=()):
        x_step = int(self.mesh.x_num / max_pix[0]) + 1
        t_step = int(self.mesh.x_num / max_pix[1]) + 1
        x_grid = self.mesh.x_matrix[::t_step, ::x_step]
        t_grid = self.mesh.t_matrix[::t_step, ::x_step]
        phi2 = sc.absolute(self.solution[1::t_step, ::x_step]) ** 2
        potential = self.potential.vector()
        x = self.mesh.x_vector

        fig = figure()
        above = fig.add_axes((0.06, 0.25, 0.9, 0.7))
        under = fig.add_axes((0.06, 0.1, 0.9, 0.17), sharex=above)

        above.set_title(title)
        above.tick_params(labelbottom="off")
        above.set_ylabel("time(a.u.)")
        under.tick_params(labelleft="off")
        under.set_xlabel("space(a.u.)")

        above.pcolormesh(x_grid, t_grid, phi2, cmap="nipy_spectral")
        under.plot(x, potential)

        if limit is not ():
            above.set_xlim(*limit)
            under.set_xlim(*limit)

        if save:
            fig.savefig(title + ".png")

        if show:
            fig.show()
        fig.clf()
