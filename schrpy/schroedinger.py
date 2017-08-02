from scipy import zeros
from scipy.integrate import ode
from schrpy import laplasian


class Schroedinger:

    def __init__(self, potential, x0state, mesh):
        self._x_num = mesh.x_num
        self._t_num = mesh.t_num
        self._dt = mesh.dt
        self._tmax = mesh.tmax

        self._laplasian = laplasian(mesh).matrix()
        self._potential = potential.matrix()
        self.hamiltonian = -0.5 * self._laplasian + self._potential
        self._operator = -1j * self.hamiltonian

        self._x0 = x0state.vector()

        self.ode = ode(self.equation)
        self.ode.set_integrator('zvode', method='adams', nsteps=1000000)
        self.ode.set_initial_value(self._x0)

    def equation(self, t, phi0):
        return self._operator.dot(phi0)

    def solve(self):
        index = 0
        sol = zeros([self._t_num, self._x_num], dtype=complex)
        print("now solving\n")
        while self.ode.successful() and self.ode.t < self._tmax:
            fin = round(index * 100 / self._t_num, 2)
            print('\r {}% doing! '.format(fin), end=' ', flush=True)
            sol[index] = self.ode.integrate(self.ode.t + self._dt)
            index += 1
        else:
            fin = round(index * 100 / self._t_num, 2)
            print('\n{}% done! '.format(fin))
        return sol
