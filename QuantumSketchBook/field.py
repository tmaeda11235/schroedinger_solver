from QuantumSketchBook.quantized import Quantized
from scipy import array


class Field(Quantized):

    def __init__(self, arg, mesh=None):
        super().__init__(mesh=mesh)
        if hasattr(arg, "__iter__"):
            vec = array(arg)
            if not vec.size == self.mesh.x_num:
                raise ValueError("It must be equal to mesh.num for length of input iterable")
            self.vector = vec
        elif callable(arg):
            self.vector = arg(self.mesh.x_vector)
        else:
            raise TypeError("the first argument should be iterable or callable")


if __name__ == "__main__":
    import QuantumSketchBook as QSB
    with QSB.Context(0, 10, 1, 0, 10, 1):
        print(Field(range(10)).vector.__class__)
        print(Field(range(10)).mesh.__class__)
