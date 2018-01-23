from QuantumSketchBook.quantized import Quantized
from scipy import array
from typing import TYPE_CHECKING, Optional
from matplotlib.pyplot import figure, axes
if TYPE_CHECKING:
    from QuantumSketchBook import Mesh


class Field(Quantized):

    def __init__(self, arg, mesh: Optional["Mesh"]=None):
        super().__init__(mesh=mesh)
        if hasattr(arg, "__iter__"):
            vec = array(tuple(arg))
            if not vec.size == self.mesh.x_num:
                raise ValueError("Length of input iterable must be equal to mesh.num")
            self.vector = vec
        elif callable(arg):
            self.vector = arg(self.mesh.x_vector)
        else:
            raise TypeError("the first argument should be iterable or callable")

    def __plot__(self, show, save, title, ylabel, values, *args, **kwargs):
        fig = figure()
        ax = axes()
        ax.plot(self.mesh.x_vector, values)
        ax.set_title(title)
        ax.set_xlabel("x")
        ax.set_ylabel(ylabel)
        fig.add_axes(ax)

        if save:
            fig.savefig(title + ".png")

        if show:
            fig.show()
        return fig


if __name__ == "__main__":
    import QuantumSketchBook as QSB
    from scipy import ndarray
    with QSB.Context(0, 10, 1, 0, 10, 1):
        assert Field(range(10)).vector.__class__ == ndarray
        assert Field(lambda x: x).vector.__class__ == ndarray
