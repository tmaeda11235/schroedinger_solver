from scipy import arange, array, zeros
from scipy.integrate import ode
from schrpy.laplasian import laplasian


class schroedinger(object):

    def __init__(self, potential, x0func, xmin=-60, xmax=60, dx=0.02, tmax=20, dt=0.02):
        self.potential = potential
        self.xmin = xmin
        self.xmax = xmax
        self.dx = dx
        self.dt = dt
        self.tmax = tmax
        self.__x = arange(xmin, xmax, dx)
        self.__x0 = array(x0func(self.__x), dtype=complex)
        self.__lap_mat = laplasian(self.dx).matrix(self.__x)
        self.__pot_mat = potential.matrix(self.__x)
        self.hamiltonian = self.__lap_mat.__add__(self.__pot_mat)
        self.__op = 0.5j * self.hamiltonian

        self.ode = ode(self.equation)
        self.ode.set_integrator('zvode', method='adams', nsteps=100000)
        self.ode.set_initial_value(self.__x0)

    def equation(self, t, phi0):
        phi = self.__op.dot(phi0)
        return phi

    def solve(self):
        index = 0
        tlen = int(self.tmax / self.dt) + 1
        xlen = len(self.__x0)
        sol = zeros([tlen, xlen], dtype=complex)
        print("now solving")
        while self.ode.successful() and self.ode.t < self.tmax:
            fin = round(index * 100 / tlen, 2)
            print('\r{}% doing! '.format(fin), end='  ')
            sol[index] = self.ode.integrate(self.ode.t + self.dt)
            index += 1
        else:
            fin = round(index * 100 / tlen, 2)
            print('\n{}% done! '.format(fin))
        return sol
