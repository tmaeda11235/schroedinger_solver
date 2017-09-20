from scipy.sparse import dia_matrix
from scipy import ndarray, array
from schrpy.mesh import Mesh
from numbers import Real


class __Potential:
    """If you make this class. you should overwrite vector() method. It defines evaluation of potential
    actual value. """
    def __init__(self, mesh):
        assert isinstance(mesh, Mesh)
        self.mesh = mesh
        self._vec = None

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


class Potential(__Potential):
    """Putting function or ndarray, you can make original potential. """
    def __init__(self, mesh, arg):
        super().__init__(mesh)
        if isinstance(arg, ndarray):
            assert arg.size == mesh.x_num, "ndarray.size must be equal to mesh.num"
            self._vec = arg
        elif callable(arg):
            self._func = arg
            self._vec = self._func(self.mesh.x_vector)
        raise AssertionError("arg should be ndarray or callable")


class Usual:
    @staticmethod
    def step(mesh, height, distance):
        assert all(isinstance(x, Real) for x in (height, distance))
        v = array([height if distance <= x else 0 for x in mesh.x_vector])
        return Potential(mesh, v)

    @staticmethod
    def box(mesh, height, distance, barrier):
        a = Usual.step(mesh, height, distance)
        b = Usual.step(mesh, height, distance + barrier)
        return a - b

    @staticmethod
    def vacuum_kp(mesh, height, well, barrier):
        period = well + barrier
        cycle = (mesh.x_max / period).__ceil__()
        return sum(Usual.box(mesh, height, i * period, i * period + barrier) for i in range(cycle))

    @staticmethod
    def kp_vacuum(mesh, height, well, barrier):
        period = well + barrier
        cycle = (mesh.x_min / period).__ceil__()
        return sum(Usual.box(mesh, height, -(i-1) * period, -(i-1) * period + barrier) for i in range(cycle))

    @staticmethod
    def kp(mesh, height, well, barrier):
        v1 = Usual.vacuum_kp(mesh, height, well, barrier).vector()
        v2 = Usual.kp_vacuum(mesh, height, well, barrier).vector()
        return Potential(mesh, v1+v2)
