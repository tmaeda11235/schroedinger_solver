from scipy import arange, array, zeros
from scipy.sparse import dia_matrix, csr_matrix, coo_matrix
from QuantumSketchBook.mesh import Mesh


class Laplasian:

    def __init__(self, mesh: Mesh):
        self.dx = mesh.dx
        self.x_num = mesh.x_num

    def _core_matrix(self) -> csr_matrix:
        det = 1 / (360 * self.dx ** 2)
        coeff = array([[4], [-54], [540], [-980], [540], [-54], [4]])
        std = det * coeff
        data = std.repeat(self.x_num + 1, axis=1)
        pad = arange(-3, 3 + 1)
        dia = dia_matrix((data, pad), shape=(self.x_num, self.x_num), dtype=complex)
        csr = dia.tocsr()
        return csr

    def matrix(self, boundary="free") -> csr_matrix:
        det = 1 / (360 * self.dx ** 2)
        csr = self._core_matrix()

        if boundary == "free":
            data = csr.data
            bound = array([-980, 1080, -108, 8, 540, -1034, 544, -54, 4, -54, 544]) * det
            data[:11] = bound
            data[-11:] = bound[::-1]
            matrix = csr_matrix((data, csr.indices, csr.indptr), dtype=complex)
            return matrix

        elif boundary == "fix":
            data = csr.data
            bound = array([-980, 0, 0, 0, 540, -926, 536, -54, 4, -54, 536]) * det
            data[:11] = bound
            data[-11:] = bound[::-1]
            matrix = csr_matrix((data, csr.indices, csr.indptr), dtype=complex)
            return matrix

        elif boundary == "period":
            n = self.x_num
            data = array([4, -54, 540,  4, -54,  4,  4, -54,  4, 540, -54,  4]) * det
            row = array([0, 0, 0, 1, 1, 2, n-3, n-2, n-2,  n-1,  n-1, n-1])
            col = array([n-3,  n-2,  n-1, n-2, n-1, n-1, 0, 0, 1, 0, 1, 2])
            coo = coo_matrix((data, (row, col)), shape=(n, n), dtype=complex)
            bound = coo.tocsr()
            matrix = csr + bound
            return matrix

        elif boundary == "absorb":
            data = csr.data
            bound = array([-980, 1080, -108, 8, 540, -1034, 544, -54, 4, -54, 544]) * det
            data[:11] = bound
            data[-11:] = bound[::-1]
            free = csr_matrix((data, csr.indices, csr.indptr), dtype=complex)
            data2 = zeros(self.x_num, dtype=complex)
            data2[-40:] = 2 ** -6 * (1j + 1) * arange(40) ** 2
            data2 = data2 + data2[::-1]
            data.transpose()
            dia = dia_matrix((data2, zeros(1)), shape=(self.x_num, self.x_num)).tocsr()
            return free + dia

        elif boundary == "poor":
            det = 1 / (self.dx ** 2)
            coeff = array([[1], [-2], [1]])
            std = det * coeff
            data = std.repeat(self.x_num + 1, axis=1)
            pad = arange(-1, 1 + 1)
            dia = dia_matrix((data, pad), shape=(self.x_num, self.x_num), dtype=complex)
            csr = dia.tocsr()
            return csr
