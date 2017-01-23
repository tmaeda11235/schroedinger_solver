from scipy.sparse import dia_matrix
from numpy import sign


class potential:
    """If you make this class. you should overwrite set_property() and val() method. """
    """val() method defines evalation of potenntial actual value. """
    """The height means strength of potential. """

    def __init__(self, height):
        self.height = height

    def set_property(self, **args):
        if 'height' in args:
            self.distance = args['height']
        return self

    def set_height(self, height):
        self.height = height
        return self

    def matrix(self, x):
        data = self.val(x)
        offset = [0]
        n = len(x)
        mat = dia_matrix((data, offset), shape=(n, n))
        return mat.tocsr()


class step_potential(potential):
    """This potential is rised up the right hand side. """
    """The distance means the position of cliff. """

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

    def val(self, x):
        potential = (sign(x - self.distance) + 1) / 2
        return potential


class box_potential(potential):

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

    def val(self, x):
        rizeup = step_potential(self.height, self.distance).val(x)
        falldown = step_potential(self.height, self.distance + self.barrier).val(x)
        return rizeup - falldown


class KP_potential(potential):

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

    def val(self, x):
        sow = map(__sow_wave(self._span).val, x)
        return box_potential(sow, self.well, self.barrier)


class __sow_wave(object):

    def __init__(self, span):
        self.span = span

    def val(self, x):
        if self.span < x:
            return self.val(x - self.span)
        elif x < 0:
            return self.val(x + self.span)
        else:
            return x
