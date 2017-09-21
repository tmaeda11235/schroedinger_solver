from scipy.sparse import dia_matrix
from scipy import ndarray, array
from schrpy.mesh import Mesh
from numbers import Real


class Potential:
    """Putting function or ndarray, you can make original potential.
    If you make this class. you should overwrite vector() method.
    It defines evaluation of potential actual value. """

    def __init__(self, mesh, arg):
        if not isinstance(mesh, Mesh):
            raise TypeError("mesh should be QSB.Mesh")
        self.mesh = mesh
        if isinstance(arg, ndarray):
            if not arg.size == mesh.x_num:
                raise ValueError("ndarray.size must be equal to mesh.num")
            self._vec = arg
        elif callable(arg):
            self._func = arg
            self._vec = self._func(self.mesh.x_vector)
        raise TypeError("arg should be ndarray or callable")

    def vector(self):
        return self._vec

    def matrix(self):
        offset = [0]
        n = self.mesh.x_num
        mat = dia_matrix((self.vector(), offset), shape=(n, n), dtype=complex)
        return mat.tocsr()

    def __add__(self, other):
        assert isinstance(other, self.__class__)
        assert self.mesh == other.mesh, "DIFFERENT MESH "
        return Potential(self.mesh, self.vector() + other.vector())

    def __mul__(self, other):
        assert isinstance(other, Real)
        return Potential(self.mesh, other * self.vector())

    def __sub__(self, other):
        assert self.mesh == other.mesh, "DIFFERENT MESH"
        return self.__add__(other.__mul__(-1))

    def __radd__(self, other):
        return self.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        return self.mesh == other.mesh and self.vector() == other.vector()


def potential(mesh, arg):
    return Potential(mesh, arg)


def step(mesh, height, distance):
    if not all(isinstance(x, Real) for x in (height, distance)):
        raise TypeError
    v = array([height if distance <= x else 0 for x in mesh.x_vector])
    return potential(mesh, v)


def box(mesh, height, distance, barrier):
    a = step(mesh, height, distance)
    b = step(mesh, height, distance + barrier)
    return a - b


def vacuum_kp(mesh, height, well, barrier):
    period = well + barrier
    cycle = (mesh.x_max / period).__ceil__()
    return sum(box(mesh, height, i * period, i * period + barrier) for i in range(cycle))


def kp_vacuum(mesh, height, well, barrier):
    period = well + barrier
    cycle = (mesh.x_min / period).__ceil__()
    return sum(box(mesh, height, -(i - 1) * period, -(i - 1) * period + barrier) for i in range(cycle))


def kp(mesh, height, well, barrier):
    v1 = vacuum_kp(mesh, height, well, barrier).vector()
    v2 = kp_vacuum(mesh, height, well, barrier).vector()
    return potential(mesh, v1 + v2)
