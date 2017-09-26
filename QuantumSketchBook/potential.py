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
            raise ValueError("DIFFERENT MESH !")
        return Potential(self.mesh, self.vector + other.vector)

    def __mul__(self, other):
        if not isinstance(other, Real):
            raise TypeError("unsupported operand type(s) for *:'Potential' and '{}'".format(type(other)))
        return Potential(self.mesh, other * self.vector)

    def __sub__(self, other):
        return self.__add__(other.__mul__(-1))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        return self.mesh == other.mesh and self.vector() == other.vector


def potential(arg):
    mesh = MeshContext.get_mesh()
    return Potential(mesh, arg)


def free():
    return potential(lambda x: 0)


def step(height: Real, distance: Real):
    if not all(isinstance(x, Real) for x in (height, distance)):
        raise TypeError
    v = array([height if distance <= x else 0 for x in MeshContext.get_mesh().x_vector])
    return potential(v)


def box(height: Real, distance: Real, barrier: Real):
    if not barrier > 0:
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
    a = step(3, 1)
    b = step(2, 2)
    kp(1, 1, 1)
