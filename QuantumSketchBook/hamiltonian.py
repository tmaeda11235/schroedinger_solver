from QuantumSketchBook.laplasian import Laplasian
from QuantumSketchBook.quantized import Quantized


class Hamiltonian(Quantized):

    def __init__(self, potential, mass=1, boundary="free", mesh=None):
        super().__init__(mesh=mesh)
        self.mass = mass
        self.potential = potential
        lap = Laplasian(self.mesh).matrix(boundary=boundary)
        pot = potential.matrix()
        self.matrix = -1 / (2 * self.mass) * lap + pot
