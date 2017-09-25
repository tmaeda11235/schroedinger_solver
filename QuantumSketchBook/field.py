from QuantumSketchBook.mesh import Mesh
from scipy import ndarray


class Field:

    def __init__(self, mesh: Mesh, arg):
        if not isinstance(mesh, Mesh):
            raise TypeError("mesh should be QSB.Mesh")
        self.mesh = mesh

        if isinstance(arg, ndarray):
            if not arg.size == mesh.x_num:
                raise ValueError("ndarray.size must be equal to mesh.num")
            self.vector = arg
        elif callable(arg):
            self.vector = arg(self.mesh.x_vector)
        else:
            raise TypeError("arg should be ndarray or callable")
