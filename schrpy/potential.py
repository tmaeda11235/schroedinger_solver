from scipy.sparse import dia_matrix
from scipy.signal import sawtooth
from scipy import pi, sign


class __potential:
    """If you make this class. you should overwrite func() method. """
    """func() method defines evalation of potenntial actual value. """

    def matrix(self, x):
        data = self.func(x)
        offset = [0]
        n = len(x)
        mat = dia_matrix((data, offset), shape=(n, n), dtype=complex)
        return mat.tocsr()


class potential(__potential):
    """Putting function, you can make original potential. """

    def __init__(self, func):
        self.func = func


class __corepotential(__potential):
    """If you make this class. you should overwrite set_property(). The height means strength of potential. """

    def __init__(self, height):
        self.height = height

    def set_property(self, **args):
        if 'height' in args:
            self.distance = args['height']
        return self

    def set_height(self, height):
        self.height = height
        return self


class step_potential(__corepotential):
    """This potential is rised up the right hand side. The distance means the position of cliff. """

    def __init__(self, height, distance):
        super(step_potential, self).__init__(height)
        self.distance = distance

    def set_property(self, **args):
        super(step_potential, self).set_property(args)
        if 'distance' in args:
            self.distance = args['distance']
        return self

    def set_distance(self, distance):
        self.distance = distance
        return self

    def func(self, x):
        potential = self.height * (sign(x - self.distance) + 1) / 2
        return potential


class box_potential(__corepotential):

    def __init__(self, height, distance, barrier):
        super(box_potential, self).__init__(height)
        self.distance = distance
        self.barrier = barrier

    def set_property(self, **args):
        super(step_potential, self).set_property(args)
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
        rizeup = step_potential(self.height, self.distance).func(x)
        falldown = step_potential(self.height, self.distance + self.barrier).func(x)
        return rizeup - falldown


class KP_potential(__corepotential):

    def __init__(self, height, well, barrier):
        super(KP_potential, self).__init__(height)
        self.well = well
        self.barrier = barrier
        self.__span = well + barrier

    def set_property(self, **args):
        super(KP_potential, self).set_property(args)
        if 'well' in args:
            self.well = args['well']
        if 'barrier' in args:
            self.barrier = args['barrier']
        self.__span = self.well + self.barrier
        return self

    def func(self, x):
        nom = 2 * pi * x / self.__span
        saw = self.__span * (sawtooth(nom) + 1) / 2
        bp = box_potential(self.height, self.well, self.barrier)
        return bp.func(saw)


class us_KP_potential(KP_potential):

    def func(self, x):
        flp = super(us_KP_potential, self).func(-x)
        rtn = step_potential(1, 0).func(x) * flp
        return rtn
