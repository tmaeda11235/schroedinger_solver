from QuantumSketchBook.context import Context  # noqa
from QuantumSketchBook.state import State, gaussian_state  # noqa
from QuantumSketchBook.potential import Potential, potential, free,  box, kp, step, vacuum_kp, kp_vacuum  # noqa
from QuantumSketchBook.hamiltonian import Hamiltonian  # noqa
from QuantumSketchBook.schroedinger import Schroedinger  # noqa


def plot(plotted, title="no_title", show=True, save=False, *args, **kwargs):
    fig = plotted.__plot__(title, *args, **kwargs)
    if save:
        fig.savefig(title + ".png")
    if show:
        fig.show()
    return fig
