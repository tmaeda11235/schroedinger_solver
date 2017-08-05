from scipy.sparse import dia_matrix
from scipy.signal import sawtooth
from scipy.interpolate import interp1d
from scipy import pi, isrealobj, linspace
from unittest import mock


class __Potential:
    """If you make this class. you should overwrite func() method. func() method defines evaluation of potential
    actual value. """

    def __init__(self, mesh):
        self._x_vector = mesh.x_vector
        self._x_num = mesh.x_num
        self._x_min = mesh.x_min
        self._x_max = mesh.x_max
        self._mesh_param = mesh.param

    def vector(self):
        pass

    def matrix(self):
        offset = [0]
        n = self._x_num
        mat = dia_matrix((self.vector(), offset), shape=(n, n), dtype=complex)
        return mat.tocsr()


class Potential(__Potential):
    """Putting function, you can make original potential. """

    def __init__(self, mesh, arg):
        super(Potential, self).__init__(mesh)
        if isrealobj(arg) and arg.len() == self._x_num:
            self._vec = arg
        elif isrealobj(arg):
            tics = linspace(self._x_min, self._x_max, num=self._vec.len())
            self._func = interp1d(tics, self._vec)
            self._vec = self._func(self._x_vector)
        elif callable(arg):
            self._func = arg
            self._vec = self._func(self._x_vector)

    def vector(self):
            return self._vec


class _CorePotential(__Potential):
    """If you make this class. you should overwrite set_property(). The height represents strength of potential. """

    def __init__(self, mesh, height):
        super(_CorePotential, self).__init__(mesh)
        self.height = height

    def vector(self):
        return self.func(self._x_vector)

    def set_property(self, **args):
        if 'height' in args:
            self.height = args['height']
        return self

    def set_height(self, height):
        self.height = height
        return self

    def func(self, x):
        pass


class StepPotential(_CorePotential):
    """This potential is raised up the right hand side. The distance represents the position of cliff. """

    def __init__(self, mesh, height, distance):
        super(StepPotential, self).__init__(mesh, height)
        self.distance = distance

    def set_property(self, **args):
        super(StepPotential, self).set_property(**args)
        if 'distance' in args:
            self.distance = args['distance']
        return self

    def set_distance(self, distance):
        self.distance = distance
        return self

    def func(self, x):
        val = self.height * (x > self.distance)
        return val


class BoxPotential(_CorePotential):

    def __init__(self, mesh, height, distance, barrier):
        super(BoxPotential, self).__init__(mesh, height)
        self.distance = distance
        self.barrier = barrier

    def set_property(self, **args):
        super(BoxPotential, self).set_property(**args)
        if 'disanse' in args:
            self.distance = args['distance']
        if 'barrier' in args:
            self.barrier = args['barrier']
        return self

    def set_distance(self, distance):
        self.distance = distance
        return self

    def set_barrier(self, barrier):
        self.barrier = barrier
        return self

    def func(self, x):
        dummy = mock.Mock(x_vector=self._x_vector, x_num=self._x_num)
        raised = StepPotential(dummy, self.height, self.distance).func(x)
        fallen = StepPotential(dummy, self.height, self.distance + self.barrier).func(x)
        return raised - fallen


class KPPotential(_CorePotential):

    def __init__(self, mesh, height, well, barrier):
        super(KPPotential, self).__init__(mesh, height)
        self.well = well
        self.barrier = barrier
        self._span = well + barrier

    def set_property(self, **args):
        super(KPPotential, self).set_property(**args)
        if 'well' in args:
            self.well = args['well']
        if 'barrier' in args:
            self.barrier = args['barrier']
        self._span = self.well + self.barrier
        return self

    # noinspection PyTypeChecker
    def func(self, x):
        nom = 2 * pi * x / self._span
        saw = self._span * (sawtooth(nom) + 1) / 2
        dummy = mock.Mock(x_vector=self._x_vector, x_num=self._x_num)
        bp = BoxPotential(dummy, self.height, self.well, self.barrier)
        return bp.func(saw)


class UsKPPotential(KPPotential):

    def func(self, x):
        dummy = mock.Mock(x_vector=self._x_vector, x_num=self._x_num)
        flp = super(UsKPPotential, self).func(-x)
        rtn = StepPotential(dummy, 1, 0).func(x) * flp
        return rtn
