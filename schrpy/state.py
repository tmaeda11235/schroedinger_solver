from scipy.stats import norm
from scipy import array, exp, isrealobj


class _CoreState:

    def __init__(self, mesh):
        self.mesh = mesh

    def vector(self):
        pass


class State(_CoreState):

    def __init__(self, mesh, arg):
        super(State).__init__(mesh)
        if callable(arg):
            self.func = arg
            self._vec = self.func(self.mesh.x_vector)

        if isrealobj(arg):
            self._vec = arg

    def vector(self):
        return self._vec


class GaussianState(_CoreState):

    def __init__(self, mesh, mean, sd, wave_number):
        super(GaussianState, self).__init__(mesh)
        self.mean = mean
        self.sd = sd
        self.wave_number = wave_number

    def _func(self, x):
        pdf = array(norm.pdf(x, self.mean, self.sd), dtype=complex)
        wav = exp(1j * self.wavenumber * x)
        return pdf * wav

    def vector(self):
        return self._func(self.mesh.x_vector)
