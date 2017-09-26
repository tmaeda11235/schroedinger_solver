from QuantumSketchBook.quantized import Quantized
from scipy import ndarray


class Field(Quantized):

    def __init__(self, arg, mesh=None):
        super().__init__(mesh=mesh)
        if isinstance(arg, ndarray):
            if not arg.size == mesh.x_num:
                raise ValueError("ndarray.size must be equal to mesh.num")
            self.vector = arg
        elif callable(arg):
            self.vector = arg(self.mesh.x_vector)
        else:
            raise TypeError("arg should be ndarray or callable")
