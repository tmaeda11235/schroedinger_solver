from QuantumSketchBook.laplasian import Laplasian
from QuantumSketchBook.schroedinger import Schroedinger


class Hamiltonian:

    def __init__(self, mesh, potential, mass=1, boundary="free"):
        self.mesh = mesh

        lap = Laplasian(mesh).matrix(boundary=boundary)
        pot = potential.matrix()
        self.matrix = -1 / (2 * mass) * lap + pot

    def matrix(self):
        return self.matrix

    def schroedinger(self, x0state):
        return Schroedinger(self, x0state)
