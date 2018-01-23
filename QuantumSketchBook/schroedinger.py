from QuantumSketchBook.state import State
from QuantumSketchBook.nelson import Nelson
from scipy import zeros, meshgrid, absolute
from scipy.integrate import ode
from matplotlib.pyplot import figure


class Schroedinger:

    def __init__(self, hamiltonian, x0state: State):
        self.mesh = hamiltonian.mesh
        self.potential = hamiltonian.potential
        self._operator = -1j * hamiltonian.matrix
        self.x0state = x0state
        self._sol = None

        self.ode = ode(self.equation)
        self.ode.set_integrator('zvode', nsteps=1000000)
        self.ode.set_initial_value(self.x0state.vector)

    def equation(self, t, phi0):  # noqa
        return self._operator.dot(phi0)

    def __iter__(self):
        yield self.x0state.vector
        index = 1
        print("now solving", end=" ")
        while self.ode.successful() and index < self.mesh.t_num:
            fin = (index + 1) / self.mesh.t_num
            print('\rSchrodinger have solved {:3.2%}! '.format(fin), end=' ' if not fin == 1 else "\n", flush=True)
            yield self.ode.integrate(self.mesh.t_vector[index])
            index += 1

    def solution(self):
        if self._sol is None:
            self._sol = zeros([self.mesh.t_num, self.mesh.x_num], dtype=complex)
            for i, s in enumerate(self):
                self._sol[i] = s
        return self._sol

    def nelson(self, n: int, micro_steps=10):
        return Nelson(self, n, micro_steps)

    def __plot__(self, show=True, save=False, title="no_title", max_pix=(1000, 1000), limit=()):
        x_step = int(self.mesh.x_num / max_pix[0]) + 1
        t_step = int(self.mesh.x_num / max_pix[1]) + 1
        x_grid, t_grid = meshgrid(self.mesh.x_vector[::x_step], self.mesh.t_vector[::t_step])
        phi2 = absolute(self.solution()[1::t_step, ::x_step]) ** 2
        potential_ = self.potential.vector
        x = self.mesh.x_vector
        fig = figure()
        above = fig.add_axes((0.06, 0.25, 0.9, 0.7))
        under = fig.add_axes((0.06, 0.1, 0.9, 0.17), sharex=above)

        above.set_title(title)
        above.tick_params(labelbottom="off")
        above.set_ylabel("time(a.u.)")
        under.tick_params(labelleft="off")
        under.set_xlabel("space(a.u.)")

        above.pcolormesh(x_grid, t_grid, phi2, cmap="nipy_spectral_r")
        under.plot(x, potential_)

        if limit is not ():
            above.set_xlim(*limit)
            under.set_xlim(*limit)

        if save:
            fig.savefig(title + ".png")

        if show:
            fig.show()
        return fig

