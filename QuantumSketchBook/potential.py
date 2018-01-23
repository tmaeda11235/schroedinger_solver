from QuantumSketchBook.field import Field
from QuantumSketchBook.context import MeshContext
from scipy.sparse import dia_matrix
from scipy import array
from numbers import Real
from math import ceil, floor


class Potential(Field):
    """Putting function or ndarray, you can make original potential.
    If you make this class. you should overwrite vector() method.
    It defines evaluation of potential actual value. """

    def matrix(self):
        offset = [0]
        n = self.mesh.x_num
        mat = dia_matrix((self.vector, offset), shape=(n, n), dtype=complex)
        return mat.tocsr()

    def __add__(self, other):
        if not self.mesh == other.mesh:
            raise ValueError("meshes on {} and {} are not the same. ")
        return Potential(self.vector + other.vector, mesh=self.mesh)

    def __mul__(self, other):
        if not isinstance(other, Real):
            raise TypeError("unsupported operand type(s) for *:'Potential' and '{}'".format(type(other)))
        return Potential(other * self.vector, mesh=self.mesh)

    def __sub__(self, other):
        return self.__add__(other.__mul__(-1))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        return self.mesh == other.mesh and self.vector == other.vector

    def __plot__(self, show, save, title, *args, **kwargs):
        return super().__plot__(show, save, title, "V", self.vector)


def potential(arg):
    return Potential(arg)


def free():
    return potential(lambda x: 0)


def step(height: Real, distance: Real):
    if not all(isinstance(x, Real) for x in (height, distance)):
        raise TypeError
    v = array([height if distance <= x else 0 for x in MeshContext.get_mesh().x_vector])
    return potential(v)


def box(height: Real, distance: Real, barrier: Real):
    if 0 >= barrier:
        raise ValueError("barrier should be positive. ")
    near = step(height, distance)
    far = step(height, distance + barrier)
    return near - far


def vacuum_kp(height, well, barrier):
    x_max = MeshContext.get_mesh().x_max
    period = well + barrier
    cycle = ceil(x_max / period) if x_max > 0 else 1
    gen = (box(height, i * period, barrier) for i in range(cycle))
    return sum(gen, free())


def kp_vacuum(height, well, barrier):
    x_min = MeshContext.get_mesh().x_min
    period = well + barrier
    cycle = -floor(x_min / period) if x_min < 0 else 1
    gen = (box(height, -(i + 1) * period, barrier) for i in range(cycle))
    return sum(gen, free())


def kp(height, well, barrier):
    v1 = vacuum_kp(height, well, barrier)
    v2 = kp_vacuum(height, well, barrier)
    return v1 + v2


if __name__ == "__main__":
    import QuantumSketchBook as QSB
    with QSB.Context(0, 10, 1, 0, 10, 1) as mesh:
        test1 = step(3, 1).vector
        test2 = step(2, 2).vector
        test3 = vacuum_kp(1, 1, 1).vector
        assert all(a == 0 for i, a in enumerate(test1) if i < 1)
        assert all(a == 3 for i, a in enumerate(test1) if i >= 1)
        assert all(b == 0 for i, b in enumerate(test2) if i < 2)
        assert all(b == 2 for i, b in enumerate(test2) if i >= 2)
        assert all(c == 0 for i, c in enumerate(test3) if i % 2 == 1)
        assert all(c == 1 for i, c in enumerate(test3) if i % 2 == 0)
        QSB.plot(step(3, 1), False, True)
