from scipy import arange, array
from scipy.sparse import dia_matrix, csr_matrix


class Laplasian:

    def __init__(self, mesh):
        self.dx = mesh.dx
        self.x_num = mesh.x_num

    def matrix(self):
        # noinspection PyTypeChecker
        det = array(1 / (360 * self.dx ** 2))
        coeff = array([[4], [-54], [540], [-980], [540], [-54], [4]])
        std = det * coeff
        data = std.repeat(self.x_num + 1, axis=1)
        pad = arange(-3, 4)
        dia = dia_matrix((data, pad), shape=(self.x_num, self.x_num))
        csr = dia.tocsr()
        fix = csr.data
        bound = array([-440, 486, -50, 4, 486, -976, 540, -54, 4, -50]) * det
        fix[:10] = bound
        fix[-10:] = bound[::-1]
        fixed = csr_matrix((fix, csr.indices, csr.indptr), dtype=complex)
        return fixed
