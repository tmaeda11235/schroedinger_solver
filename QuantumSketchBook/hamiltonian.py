from QuantumSketchBook.laplasian import Laplasian
from QuantumSketchBook.schroedinger import Schroedinger


class Hamiltonian:

    def __init__(self, mesh, potential, mass=1, boundary="free"):
        self.mesh = mesh
        self.mass = mass
        lap = Laplasian(mesh).matrix(boundary=boundary)
        pot = potential.matrix()
        self.matrix = -1 / (2 * self.mass) * lap + pot

    def schroedinger(self, x0state):
        return Schroedinger(self, x0state)
