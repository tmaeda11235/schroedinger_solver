import scipy as sp
import schrpy.laplasian as lap
import schrpy.potential as pot  # noqa


class schroedinger(object):

    def __init__(self, potential, x0func, xmin, xmax, dx, dt, tmax):
        self.potential = potential
        self.xmin = xmin
        self.xmax = xmax
        self.dx = dx
        self.dt = dt
        self.tmax = tmax
        self.__x = sp.arange(xmin, xmax, dx)
        self.__x0 = x0func(self.__x)
        self.__lap_mat = lap.laplasian(self.dx).matrix(self.__x)
        self.__pot_mat = potential.matrix(self.__x)
        self.hamiltonian = self.__lap_mat + self.__pot_mat

        self.adams = sp.integrate.ode(self.equation)
        self.adams.set_integrator('zvode', method='bdf', nsteps=10000)
        self.adams.set_initial_value(self.__x0)

    def equation(self, phi0):
        phi = sp.array(0.5j * self.hamiltonian.dot(phi0))
        return phi

    def solve(self):
        index = 0
        tlen = int(self.tmax / self.dt) + 1
        xlen = len(self.__x0)
        solx = sp.zeros([tlen, xlen])
        solt = sp.zeros([tlen])
        while self.adams.successful() and self.adams.t < self.tmax:
            solx[index] = self.adams.integrate(self.adams.t + self.dt)
            solt[index] = self.adams.t
            index += 1
        return (solt, solx)
