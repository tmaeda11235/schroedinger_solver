from scipy.stats import norm
from scipy import random
from scipy import array, exp, linspace, ndarray, absolute, ones, empty, append
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

    def random_values(self, n):
        probability = absolute(self.vector()) ** 2
        probability = probability * 10000  # 有効数字を3ケタ以上取るために10000倍する
        probability_naturalized = probability.astype(int)
        target = []
        for i in range(self._x_num):
            weight = probability_naturalized[i]
            if not weight == 0:
                weight_array = i * ones(weight, dtype=int)
                target.extend(weight_array.tolist())
        max_random = len(target)
        target_index = random.randint(0, max_random, n)
        random_index = array(target)[target_index]
        return self._x_vector[random_index]


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
        pdf = array(norm.pdf(x, self.mean, self.sd / 2), dtype=complex)
        wav = exp(1j * self.wave_number * x)
        return pdf * wav

    def vector(self):
        return self._func(self._x_vector)
