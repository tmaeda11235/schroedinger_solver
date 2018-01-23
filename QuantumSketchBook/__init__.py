from QuantumSketchBook.context import Context  # noqa
from QuantumSketchBook.state import State, gaussian_state  # noqa
from QuantumSketchBook.potential import Potential, potential, free,  box, kp, step, vacuum_kp, kp_vacuum  # noqa
from QuantumSketchBook.hamiltonian import Hamiltonian  # noqa
from QuantumSketchBook.schroedinger import Schroedinger  # noqa


def plot(plotted, show=True, save=False, title="no_title", *args, **kwargs):
    return plotted.__plot__(show, save, title, *args, **kwargs)
