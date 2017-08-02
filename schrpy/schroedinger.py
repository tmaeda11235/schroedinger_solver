from scipy import array, zeros
from scipy.integrate import ode
from schrpy import laplasian


class Schroedinger:

    def __init__(self, potential, x0state, mesh):
        self._mesh = mesh
        self._laplasian = laplasian(self._mesh).matrix()
        self._potential = potential.matrix()
        self.hamiltonian = -0.5 * self._laplasian + self._potential
        self._operator = -1j * self.hamiltonian

        self._x0 = x0state.vector()

        self.ode = ode(self.equation)
        self.ode.set_integrator('zvode', method='adams', nsteps=1000000)
        self.ode.set_initial_value(self._x0)

    def equation(self, t, phi0):
        phi = self._operator.dot(phi0)
        return phi

    def solve(self):
        index = 0
        tlen = self._mesh.t_num
        xlen = self._mesh.x_num
        sol = zeros([tlen, xlen], dtype=complex)
        print("now solving\n")
        while self.ode.successful() and self.ode.t < self._mesh.tmax:
            fin = round(index * 100 / tlen, 2)
            print('\r {}% doing! '.format(fin), end=' ', flush=True)
            sol[index] = self.ode.integrate(self.ode.t + self._mesh.dt)
            index += 1
        else:
            fin = round(index * 100 / tlen, 2)
            print('\n{}% done! '.format(fin))
        return sol
