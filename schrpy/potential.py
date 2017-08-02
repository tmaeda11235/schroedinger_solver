from scipy.sparse import dia_matrix
from scipy.signal import sawtooth
from scipy import pi
from schrpy import mesh


class __potential:
    """If you make this class. you should overwrite func() method. func() method defines evaluation of potential
    actual value. """

    def __init__(self, mesh_):
        self._x_vector = mesh_.x_vector
        self._x_num = mesh_.x_num

    def vector(self):
        pass

    def matrix(self):
        offset = [0]
        n = self._x_num
        mat = dia_matrix((self.vector(), offset), shape=(n, n), dtype=complex)
        return mat.tocsr()


class potential(__potential):
    """Putting function, you can make original potential. """

    def __init__(self, mesh_, func):
        super(potential, self).__init__(mesh_)
        if callable(func):
            self._func = func

    def vector(self):
        return self._func(self._x_vector)


class _corepotential(__potential):
    """If you make this class. you should overwrite set_property(). The height represents strength of potential. """

    def __init__(self, mesh_, height):
        super(_corepotential, self).__init__(mesh_)
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


class step_potential(_corepotential):
    """This potential is raised up the right hand side. The distance represents the position of cliff. """

    def __init__(self, mesh_, height, distance):
        super(step_potential, self).__init__(mesh_, height)
        self.distance = distance

    def set_property(self, **args):
        super(step_potential, self).set_property(**args)
        if 'distance' in args:
            self.distance = args['distance']
        return self

    def set_distance(self, distance):
        self.distance = distance
        return self

    def func(self, x):
        val = self.height * (x > self.distance)
        return val


class box_potential(_corepotential):

    def __init__(self, mesh_, height, distance, barrier):
        super(box_potential, self).__init__(mesh_, height)
        self.distance = distance
        self.barrier = barrier

    def set_property(self, **args):
        super(box_potential, self).set_property(**args)
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
        xmin = self._x_vector[0]
        xmax = self._x_vector[-1]
        dx = (xmax-xmin)/self._x_num
        dummy = mesh.mesh(xmin, xmax, dx, 0, 1, 1)
        raised = step_potential(dummy, self.height, self.distance).func(x)
        fallen = step_potential(dummy, self.height, self.distance + self.barrier).func(x)
        return raised - fallen


class KP_potential(_corepotential):

    def __init__(self, mesh_, height, well, barrier):
        super(KP_potential, self).__init__(mesh_, height)
        self.well = well
        self.barrier = barrier
        self._span = well + barrier

    def set_property(self, **args):
        super(KP_potential, self).set_property(**args)
        if 'well' in args:
            self.well = args['well']
        if 'barrier' in args:
            self.barrier = args['barrier']
        self._span = self.well + self.barrier
        return self

    # noinspection PyTypeChecker
    def func(self, x):
        nom = 2 * pi * x / self._span
        # noinspection PyTypeChecker
        saw = self._span * (sawtooth(nom) + 1) / 2
        xmin = self._x_vector[0]
        xmax = self._x_vector[-1]
        dx = (xmax-xmin)/self._x_num
        dummy = mesh.mesh(xmin, xmax, dx, 0, 1, 1)
        bp = box_potential(dummy, self.height, self.well, self.barrier)
        return bp.func(saw)


class us_KP_potential(KP_potential):

    def func(self, x):
        xmin = self._x_vector[0]
        xmax = self._x_vector[-1]
        dx = (xmax-xmin)/self._x_num
        dummy = mesh.mesh(xmin, xmax, dx, 0, 1, 1)
        flp = super(us_KP_potential, self).func(-x)
        rtn = step_potential(dummy, 1, 0).func(x) * flp
        return rtn
