import QuantumSketchBook as sp
from QuantumSketchBook.potential import Potential
from QuantumSketchBook.state import State
import scipy as sc
from matplotlib.pyplot import figure
from matplotlib.colors import Normalize


class Note:

    def __init__(self, mesh, mass=1):
        self.mesh = mesh
        self.potential = sp.potential(self.mesh, lambda x: 0 * x)
        self.initial = sp.gaussian_state(self.mesh, 0, 1, 0)
        self.hamiltonian = sp.Hamiltonian(self.mass, self.potential, mass=mass)
        self.schroedinger = sp.Schroedinger(self.hamiltonian, self.initial)
        self.solution = None
        self.locus = None
        self.mass = mass

    def set_potential(self, potential: Potential):
        if not potential.mesh.param == self.mesh.param:
            raise ValueError("objects based on different meshes have been imputed. ")
        self.potential = potential

    def set_initial(self, state: State):
        if not state.mesh.param == self.mesh.param:
            raise ValueError("objects based on different meshes have been imputed. ")
        self.initial = state

    def solve_schroedinger_equation(self, boundary="free"):
        self.hamiltonian = sp.Hamiltonian(self.mesh, self.potential, mass=self.mass, boundary=boundary)
        self.schroedinger = sp.Schroedinger(self.hamiltonian, self.initial)
        self.solution = self.schroedinger.solution()
        return self.solution

    def save_solution(self, file_name):
        sc.save(file_name, self.solution)

    def load_solution(self, file_name):
        sol = sc.load(file_name)
        if not sol.shape == (self.mesh.t_num, self.mesh.x_num):
            raise ValueError("Different meshes have been imputed")
        self.solution = sol

    def generate_locus(self, n, micro_steps=10):
        nel = sp.Nelson(self.schroedinger, n, micro_steps=micro_steps)
        self.locus = nel.locus()
        return self.locus

    def easy_plot2d(self, max_pix=(1000, 1000), show=True, save=False, title="no_title", limit=()):
        x_step = int(self.mesh.x_num / max_pix[0]) + 1
        t_step = int(self.mesh.x_num / max_pix[1]) + 1
        x_grid, t_grid = sc.meshgrid(self.mesh.x_vector[::x_step], self.mesh.t_vector[::t_step])
        phi2 = sc.absolute(self.solution[1::t_step, ::x_step]) ** 2
        potential = self.potential.vector
        x = self.mesh.x_vector
        norm = Normalize(vmax=phi2[0].max())
        fig = figure()
        above = fig.add_axes((0.06, 0.25, 0.9, 0.7))
        under = fig.add_axes((0.06, 0.1, 0.9, 0.17), sharex=above)

        above.set_title(title)
        above.tick_params(labelbottom="off")
        above.set_ylabel("time(a.u.)")
        under.tick_params(labelleft="off")
        under.set_xlabel("space(a.u.)")

        above.pcolormesh(x_grid, t_grid, phi2, cmap="nipy_spectral_r", norm=norm)
        under.plot(x, potential, ".")

        if limit is not ():
            above.set_xlim(*limit)
            under.set_xlim(*limit)

        if save:
            fig.savefig(title + ".png")

        if show:
            fig.show()
        fig.clf()
