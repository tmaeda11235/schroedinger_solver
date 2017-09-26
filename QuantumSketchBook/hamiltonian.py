from QuantumSketchBook.laplasian import Laplasian
from QuantumSketchBook.schroedinger import Schroedinger
from QuantumSketchBook.quantized import Quantized


class Hamiltonian(Quantized):

    def __init__(self, potential, mass=1, boundary="free", mesh=None):
        super().__init__(mesh=mesh)
        self.mass = mass
        lap = Laplasian(mesh).matrix(boundary=boundary)
        pot = potential.matrix()
        self.matrix = -1 / (2 * self.mass) * lap + pot

    def schroedinger(self, x0state):
        return Schroedinger(self, x0state)
