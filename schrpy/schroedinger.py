from scipy import zeros
from scipy.integrate import ode
from schrpy import Laplasian


class Schroedinger:
    def __init__(self, mesh, potential, x0state, mass=1, boundary="free"):
        self._x_num = mesh.x_num
        self._t_num = mesh.t_num
        self._dt = mesh.dt
        self._tmax = mesh.t_max
        self._tic = mesh.t_vector

        self._laplasian = Laplasian(mesh).matrix(boundary=boundary)
        self._potential = potential.matrix()
        self.hamiltonian = -1 / (2 * mass) * self._laplasian + self._potential
        self._operator = -1j * self.hamiltonian

        self._x0 = x0state.vector()

        self.ode = ode(self.equation)
        self.ode.set_integrator('zvode', nsteps=1000000)
        self.ode.set_initial_value(self._x0)

    def equation(self, t, phi0):
        return self._operator.dot(phi0)

    def generator(self):
        yield self._x0
        index = 1
        print("now solving", end=" ")
        while self.ode.successful() and index < self._t_num:
            fin = (index+1) / self._t_num
            print('\rSchrodinger have solved {:3.2%}! '.format(fin), end=' ' if not fin == 1 else "\n", flush=True)
            yield self.ode.integrate(self._tic[index])
            index += 1

    def solve(self):
        sol = zeros([self._t_num, self._x_num], dtype=complex)
        for i, s in enumerate(self.generator()):
            sol[i] = s
        return sol
