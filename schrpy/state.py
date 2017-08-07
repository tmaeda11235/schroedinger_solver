from scipy.stats import norm
from scipy import array, exp, linspace, ndarray
from scipy.interpolate import interp1d


class _CoreState:

    def __init__(self, mesh):
        self._x_vector = mesh.x_vector
        self._x_num = mesh.x_num
        self._x_min = mesh.x_min
        self._x_max = mesh.x_max
        self.mesh_param = mesh.param

    def vector(self):
        pass


class State(_CoreState):

    def __init__(self, mesh, arg):
        super(State, self).__init__(mesh)
        if isinstance(arg, ndarray) and arg.len() == self._x_num:
            self._vec = arg
        elif isinstance(arg, ndarray):
            tics = linspace(self._x_min, self._x_max, num=self._vec.len())
            self._func = interp1d(tics, self._vec)
            self._vec = self._func(self._x_vector)
        elif callable(arg):
            self._func = arg
            self._vec = self._func(self._x_vector)

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
        wav = exp(1j * self.wave_number * x)
        return pdf * wav

    def vector(self):
        return self._func(self._x_vector)
